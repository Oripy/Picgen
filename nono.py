# -*- coding: utf-8 -*-

#import cgi
#import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import db

import os
from google.appengine.ext.webapp import template
from django.utils import simplejson

from nonogram.nonogram_creator import next_valid_number
from nonogram.picgen import number_to_table, number_to_name, name_to_number
import nonogram.solver as solver 

from display_problems import display_nonogram, display_img

ZOOM = 30
WIDTH = 5
HEIGHT = 5

import pickle

class GenericListProperty(db.Property):
    """ Class that allows storing python objects """
    data_type = db.Blob

    def validate(self, value):
        if type(value) is not list:
            raise db.BadValueError("Property {} must be a list, not {}.".format(self.name, type(value)), value)
        return value

    def get_value_for_datastore(self, model_instance):
        return db.Blob(pickle.dumps(getattr(model_instance,self.name)))

    def make_value_from_datastore(self, value):
        return pickle.loads(value)

class Grid_db(db.Model):
    """Models an individual grid entry with the user, name, state and date."""
    user = db.UserProperty()
    name = db.StringProperty()
    state = db.IntegerProperty()
    grid_type = db.StringProperty()
    grid_table = GenericListProperty(default=[])
    date = db.DateTimeProperty(auto_now_add=True)

def grid_key(grid_name=None):
    """ Constructs a datastore key for a Grid entity with grid_name."""
    return db.Key.from_path('Grid', grid_name or 'default_grid')

class RPCHandler(webapp2.RequestHandler):
    """ Allows the functions defined in the RPCMethods class to be RPCed."""
#    def __init__(self):
#        webapp2.RequestHandler.__init__(self)
#        self.methods = RPCMethods()

    def post(self):
        args = simplejson.loads(self.request.body)
        func, args = args[0], args[1:]
       
        if func[0] == '_':
            self.error(403) # access denied
            return
        
        func = getattr(self, func)
        if not func:
            self.error(404) # file not found
            return

        result = func(*args)
        self.response.out.write(simplejson.dumps(result))


#class RPCMethods:
#    """ Defines the methods that can be RPCed.
#    NOTE: Do not allow remote callers access to private/protected "_*" methods.
#    """
    def changeCell(self, row_nbr, col_nbr, table, name):
        """ returns the new representation of the table """
        col_nbr = int(col_nbr)
        row_nbr = int(row_nbr)
        
        # Get the current state of the clicked cell
        state = int(table[WIDTH * row_nbr + col_nbr])

        # Change it to new value
        state -= 1
        if state < 0:
            state = 2
        
        # Add the new state to the table
        position = WIDTH * row_nbr + col_nbr
        if position == 0:
            table = str(state) + table[1:]
        elif position == WIDTH * (WIDTH - 1) + (HEIGHT - 1):
            table = table[:-1] + str(state)
        else:
            table = table[:position] + str(state) + table[position+1:]
        
        # Check if the grid is solved
        bin_number = str(bin(name_to_number(name)))
        bin_number = bin_number[2:] # Remove the leading '0b'"
        bin_number = '0'*((WIDTH * HEIGHT)-len(bin_number)) + bin_number
        solved = True
        for position in xrange(WIDTH * HEIGHT):
            if table[position] == '1' and bin_number[position] != '1':
                solved = False
                break
            elif table[position] != '1' and bin_number[position] == '1':
                solved = False
                break
        
        if solved:
            table = table.replace('2', '0')
            table += '1'
            # Get value from DB
            grid = self._get_db_entry(name)
            result = grid.get()
            if result:
                result.grid_table = self._decode_table(table)
                result.state = 1
                result.put()
        else:
            table += '0'
        
        return table
    
    def saveState(self, table, name):
        if len(table) != WIDTH * HEIGHT:
            return "Failed"

        table = self._decode_table(table)
        
        # Get value from DB
        grid = self._get_db_entry(name)

        result = grid.get()
        if result:        
            result.grid_table = table
            result.put()

        return "Saved"
    
    def _decode_table(self, table):
        table_out = [[None]*WIDTH for _ in range(HEIGHT)]
        for row_nbr in xrange(HEIGHT):
            for col_nbr in xrange(WIDTH):
                if table[WIDTH * row_nbr + col_nbr] == '0':
                    table_out[row_nbr][col_nbr] = False
                elif table[WIDTH * row_nbr + col_nbr] == '1':
                    table_out[row_nbr][col_nbr] = True
        return table_out

    def _get_db_entry(self, name):
        userlogin = users.get_current_user()
        if not userlogin:
            # Redirect to the login page
            self.redirect(users.create_login_url(self.request.uri))
        
        return db.GqlQuery("SELECT * FROM Grid_db "
                           "WHERE name = :name_nonogram AND "
                           "user = :user AND "
                           "state = 0 AND "
                           "ANCESTOR IS :ancestor",
                           user = userlogin,
                           name_nonogram = name,
                           ancestor = grid_key())

class MainPage(webapp2.RequestHandler):
    def get(self):
        userlogin = users.get_current_user()
        if not userlogin:
            # Redirect to the login page
            self.redirect(users.create_login_url(self.request.uri))
        else:
            # Get last unsolved Grid from user
            last_grid = db.GqlQuery("SELECT * FROM Grid_db "
                                    "WHERE user = :user AND "
                                    "state = 0 AND "
                                    "ANCESTOR IS :ancestor",
                                    user = userlogin,
                                    ancestor = grid_key())    
            result = last_grid.get()
            if result:
                # Get last unsolved grid
#                number = name_to_number(result.name)
                table = result.grid_table
                number = name_to_number(result.name)
            else:
                # Get last entry number
                previous = db.GqlQuery("SELECT * "
                                    "FROM Grid_db "
                                    "WHERE ANCESTOR IS :1 "
                                    "ORDER BY date DESC LIMIT 1",
                                    grid_key())
                result = previous.get()
                if result:
                    prev_number = name_to_number(result.name)
                else:
                    prev_number = 0
                
                # Get a new valid grid
                number, _  = next_valid_number(prev_number)
                table = [[None]*WIDTH for _ in range(HEIGHT)]
                
                
                # Add it to the database state unsolved
                new_grid = Grid_db(parent=grid_key())
                new_grid.user = userlogin
                new_grid.name = number_to_name(number)
                new_grid.state = 0
                new_grid.grid_type = "nonogram"               
                new_grid.grid_table = table
                new_grid.put()
            
            name = number_to_name(number)            
            
            col_counts, row_counts = solver.get_counts(number_to_table(number, WIDTH, HEIGHT))
            grid = solver.Grid(col_counts, row_counts, table)

            text_info = ""
            
#            if self.request.get('row'):
#                row = int(self.request.get('row'))
#                col = int(self.request.get('col'))
#            
#                if grid.get_value(col, row) == True:
#                    grid.set_value(col, row, False)
#                elif grid.get_value(col, row) == False:
#                    grid.set_value(col, row, None)
#                else:
#                    grid.set_value(col, row, True)
#                
#                if grid.is_complete():
#                    if solver.check_solution(grid):
#                        result.state = 1
#                        text_info = """ Grid complete ! Congratulation !<br />
#                                    <a href="/">Next</a> """
                
#                # Update the entry in database
#                result.grid_table = grid.get_grid()
#                result.put()
            
            # Display the problem
            nonogram = display_nonogram(grid)
            
            ##############"
            # Display recent results
            recentquery = db.GqlQuery("SELECT * "
                                    "FROM Grid_db "
                                    "WHERE user = :user AND "
                                    "state = 1 AND "
                                    "ANCESTOR IS :ancestor "
                                    "ORDER BY date DESC LIMIT 5",
                                    user = userlogin,
                                    ancestor = grid_key())
            recent = ''
            for item in recentquery:
                recent += display_img(item.grid_table)
                recent += '<br />&nbsp;<br />'
            
            # Set the Logout link
            url_logout = users.create_logout_url(self.request.uri)
            url_logout_text = 'Logout'
            
            # Set values that will be used in the template
            template_values = {
                'zoom': ZOOM,
                'height_row': ZOOM + 1,
                'width': WIDTH,
                'height': HEIGHT,
                'nonogram': nonogram,
                'nonogram_name': name,
                'url_logout': url_logout,
                'url_logout_text': url_logout_text,
                'text_info': text_info,
                'recent': recent
            }
            
            # Display the page from the template
            path = os.path.join(os.path.dirname(__file__), 'index.html')
            self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rpc', RPCHandler)], debug=True)
