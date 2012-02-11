# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 11:34:30 2012

@author: pmaurier
"""
from __future__ import print_function

VERBOSE = False
vprint = lambda *a, **k: None
def set_verbose(verbose):
    """ Redefine the vprint function for verbose output """
    if verbose:
        global vprint
        global VERBOSE
        VERBOSE = True
        vprint = print if verbose else lambda *a, **k: None

#from time import time
from copy import copy, deepcopy

class Grid:
    """ Grid that describe the game state """
    def __init__(self, width, height, col_counts, row_counts):
        self.width = width
        self.height = height
        self.col_counts = col_counts     
        self.row_counts = row_counts
        self._rows = [[None]*width for _ in range(height)]
        self._cols = [[None]*height for _ in range(width)]
        
    def get_value(self, col_nbr, row_nbr):
        """ returns the value at given coordinates """
        return self._rows[row_nbr][col_nbr]
        
    def get_row(self, row_nbr):
        """ returns the given row """
        return copy(self._rows[row_nbr])
    
    def get_col(self, col_nbr):
        """ returns the given column """
        return copy(self._cols[col_nbr])
        
    def get_rows(self):
        """ returns all rows """
        return self._rows
    
    def get_cols(self):
        """ returns all columns """
        return self._cols
        
    def get_grid(self):
        """ returns the whole grid (equivalent to get_rows) """
#        return deepcopy(self._rows)
        return self._rows
        
    def set_value(self, col_nbr, row_nbr, value):
        """ set the value at given coordinates """
        self._rows[row_nbr][col_nbr] = value
        self._cols[col_nbr][row_nbr] = value
        return True
    
    def set_block(self, col_nbr, row_nbr):
        """ set True at given coordinates """
        return self.set_value(col_nbr, row_nbr, True)
        
    def set_space(self, col_nbr, row_nbr):
        """ set False at given coordinates """
        return self.set_value(col_nbr, row_nbr, False)
    
    def set_row(self, row_nbr, row):
        """ replace the row at given height by given row """
        for col_nbr in xrange(self.width):
            self.set_value(col_nbr, row_nbr, row[col_nbr])
        return self._rows[row_nbr]
    
    def set_col(self, col_nbr, row):
        """ replace the column at given width by given row """
        for row_nbr in xrange(self.height):
            self.set_value(col_nbr, row_nbr, row[row_nbr])
        return self._cols[col_nbr]
             
    def is_complete(self):
        """ return True if the whole grid is completed """
        for rows in self._rows:
            for item in rows:
                if item == None:
                    return False
        return True

def solve(grid):
    """ Return a grid with the solution 
    """    
    grid = deepcopy(grid)
    
    # Réordonner par ordre du plus long test
    # (n'est efficace que si l'on ne fait pas toute les permutations...)
#    col_weights = [(x, weight_row(grid.col_counts[x])) 
#                    for x in xrange(grid.width)]
#    col_weights.sort(key=lambda tup: tup[1], reverse=True)
#    
#    row_weights = [(y, weight_row(grid.row_counts[y]))
#                    for y in xrange(grid.height)]
#    row_weights.sort(key=lambda tup: tup[1], reverse=True)
    
#    # Pas d'ordre particulier (ordre de lecture normal gauche/droite haut/bas)
#    col_weights = [[i] for i in xrange(grid.width)]
#    row_weights = [[i] for i in xrange(grid.height)]

    # Simple_Boxes
    for col_nbr in xrange(grid.width):
        grid.set_col(col_nbr, simple_boxes(grid.col_counts[col_nbr],
                                           grid.get_col(col_nbr)))
    for row_nbr in xrange(grid.height):
        grid.set_row(row_nbr, simple_boxes(grid.row_counts[row_nbr],
                                           grid.get_row(row_nbr)))
    if VERBOSE:
        print_grid(grid)
    
    while True:
        # Simple_Spaces
        modif = 0
        for col_nbr in xrange(grid.width):
            oldcol = grid.get_col(col_nbr)
            newcol = simple_spaces(grid.col_counts[col_nbr], oldcol)
            if oldcol != newcol:
                vprint("-simple_spaces-")
                vprint(grid.col_counts[col_nbr])
                print_row(oldcol)
                print_row(newcol)
                grid.set_col(col_nbr, newcol)
                modif += 1
        for row_nbr in xrange(grid.height):
            oldrow = grid.get_row(row_nbr)
            newrow = simple_spaces(grid.row_counts[row_nbr], oldrow)
            if oldrow != newrow:
                vprint("-simple_spaces-")
                vprint(grid.row_counts[row_nbr])
                print_row(oldrow)
                print_row(newrow)
                modif += 1
                grid.set_row(row_nbr, newrow)

        # Forcing
        for col_nbr in xrange(grid.width):
            oldcol = grid.get_col(col_nbr)
            newcol = forcing(grid.col_counts[col_nbr], oldcol)
            if oldcol != newcol:
                vprint("-forcing-")
                vprint(grid.col_counts[col_nbr])
                print_row(oldcol)
                print_row(newcol)
                grid.set_col(col_nbr, newcol)
                modif += 1
        for row_nbr in xrange(grid.height):
            oldrow = grid.get_row(row_nbr)
            newrow = forcing(grid.row_counts[row_nbr], oldrow)
            if oldrow != newrow:
                vprint("-forcing-")
                vprint(grid.row_counts[row_nbr])
                print_row(oldrow)
                print_row(newrow)
                modif += 1
                grid.set_row(row_nbr, newrow)
        
        # Glue
        for col_nbr in xrange(grid.width):
            oldcol = grid.get_col(col_nbr)
            newcol = glue(grid.col_counts[col_nbr], oldcol)
            if oldcol != newcol:
                vprint("-glue-")
                vprint(grid.col_counts[col_nbr])
                print_row(oldcol)
                print_row(newcol)
                grid.set_col(col_nbr, newcol)
                grid.set_col(col_nbr, newcol)
                modif += 1
            oldcol.reverse()
            counts_rev = copy(grid.col_counts[col_nbr])
            counts_rev.reverse()
            newcol = glue(counts_rev, oldcol)
            if oldcol != newcol:
                vprint("-glue-reverse-")
                vprint(counts_rev)
                print_row(oldcol)
                print_row(newcol)
                grid.set_col(col_nbr, newcol)
                newcol.reverse()
                grid.set_col(col_nbr, newcol)
                modif += 1
        for row_nbr in xrange(grid.height):
            oldrow = grid.get_row(row_nbr)
            newrow = glue(grid.row_counts[row_nbr], oldrow)
            if oldrow != newrow:
                vprint("-glue-")
                vprint(grid.row_counts[row_nbr])
                print_row(oldrow)
                print_row(newrow)
                grid.set_row(row_nbr, newrow)
                modif += 1
            oldrow.reverse()
            counts_rev = copy(grid.row_counts[row_nbr])
            counts_rev.reverse()
            newrow = glue(counts_rev, oldrow)
            if oldrow != newrow:
                vprint("-glue-reverse-")
                vprint(counts_rev)
                print_row(oldrow)
                print_row(newrow)
                newrow.reverse()
                grid.set_row(row_nbr, newrow)
                modif += 1
        if modif == 0:
            break
        else:
            if VERBOSE:
                print_grid(grid)
    
    # Pre-process permutations
    col_permutations = []
    for col_nbr in xrange(grid.width):
        col_permutations.append(get_permutations(grid.col_counts[col_nbr],
                                                 grid.get_col(col_nbr)))
    row_permutations = []
    for row_nbr in xrange(grid.height):
        row_permutations.append(get_permutations(grid.row_counts[row_nbr],
                                                 grid.get_row(row_nbr)))

    col_list = range(grid.width)
    row_list = range(grid.height)    
    # Final solving
    while True:
        modif = 0
        for col_nbr in col_list:
            col_old = grid.get_col(col_nbr)
            col_permutations[col_nbr], col_new = solve_row(
                col_permutations[col_nbr], col_old)
            grid.set_col(col_nbr, col_new)
            if not (None in col_new):
                col_list.remove(col_nbr)
            if col_old != col_new:
                modif += 1        
        for row_nbr in row_list:
            row_old = grid.get_row(row_nbr)
            row_permutations[row_nbr], row_new = solve_row(
                row_permutations[row_nbr], row_old)
            grid.set_row(row_nbr, row_new)
            if not (None in row_new):
                row_list.remove(row_nbr)
            if row_old != row_new: 
                modif += 1
                
        if modif == 0:
            break
        
    return grid
    
def weight_row(counts):
    """ Return the "weight" of the row
    the weight is the size of the counts with space between them
    weight_row([3,2,4]) => [###.##.####] => 11
    """
    return max(sum(counts)+len(counts)-1, 0)

def get_common(row1, row2):
    """ Find common elements in two rows
    row1    [1 1 1 1 0 2 2 2 0 0]
    row2    [0 0 1 1 1 1 0 2 2 2]
                 | |       |
    row_out [_ _ 1 1 _ _ _ 2 _ _] """
    
    length = len(row1)
    row_out = [None]*length
    for position in xrange(length):
        if row1[position] == row2[position]:
            row_out[position] = row1[position]
    return row_out
    
def fit(row, length, position):
    """ Returns True if a serie of "length" blocks fits in "row" at "position"
    """
    len_row = len(row)
    # Convert if negative position given
    if position < 0:
        position = len_row + position - length + 1
    
    # If the blocks serie tested is longer than the row
    if len_row < position+length:
        return False

    if position+length != len_row:
        # If there is a block just after the blocks series tested
        if row[position+length] == True:
            return False
    
    # Test each postions on the blocks serie
    for i in xrange(length):
        if row[position+i] == False:
            return False
    return True

def convert(row):
    """ Convert a numbered list in a True/False/None list
        [0, 0, None, 1, 1, -1, 2, 2, None, None]
        
        [False, False, None, True, True, False, True, True, None, None]
    """
    length = len(row)
    row_out = [None]*length
    for i in xrange(length):
        if row[i] != None:
            if (row[i] > 0) or (row[i] == True):
                row_out[i] = True
            elif (row[i] <= 0) or (row[i] == False):
                row_out[i] = False
    return row_out

def recover(oldrow, newrow):
    """ Look for information from oldrow that may have been lost in newrow
        oldrow:  [None,  True, None, False]
        newrow:  [False, None, None, None]
        
        row_out: [False, True, None, False]
    """
    length = len(oldrow)
    row_out = [None]*length
    for i in xrange(length):
        if oldrow[i] == True:
            row_out[i] = True
        elif oldrow[i] == False:
            row_out[i] = False
        else:
            row_out[i] = newrow[i]
    return row_out

def reverse(row):
    """ reverse a numbered row 
        [-2 2 2 2 -1 -1 -1 1 1]
       print 
        [ 0 1 1 1 -1 -1 -1 2 2]
    """    
    len_counts = max(row)
    row_out = []
    for item in row:
        if item > 0:
            row_out.append((item - len_counts - 1) * -1)
        else:
            row_out.append((item + len_counts) * -1)
            
    row_out.reverse()
    return row_out
    
def simple_boxes(row_counts, row):
    """ Push solutions in both sides and look for common "Blocks"
     4,3 [_ _ _ _ _ _ _ _ _ _]
    
         [# # # # . # # # . .]
         [. . # # # # . # # #]
              | |       |
         [_ _ # # _ _ _ # _ _]  """
         
    nbr = len(row_counts)
    length = len(row)
    
    # Maximum number of space at the begining of the row
    blankspace = length-sum(row_counts)-nbr+1
    
    row1 = [0]*length
    row2 = [0]*length
    row_out = [None]*length

    num = 0 # Current row_count number
    for i in xrange(nbr):
        for j in xrange(row_counts[i]):
            row1[num] = i+1
            row2[num+blankspace] = i+1
            num += 1
        if i != nbr-1:
            row1[num] = 0
            row2[num+blankspace] = 0
            num += 1
    
    row_out = get_common(row1, row2)

    # Include the results in the given row
    for i in xrange(length):
        if row_out[i] != 0 and row_out[i] != None:
            # Add a block
            row_out[i] = True
        else:
            # Keep previous data
            row_out[i] = row[i]
    return row_out

def simple_spaces(row_counts, row):
    """ Write a solution in both ways then look for common "Spaces"
     3,1 [_ _ _ # _ _ _ _ # _]
    
         [. . . # # # . . # .]
         [. # # # . . . . # .]
          |     |     | | | |
         [. _ _ # _ _ . . # .] """

    length = len(row)
    nbr = len(row_counts)
    if nbr == 0:
        # No clue, so there are only spaces in the row
        return [False]*length
    elif not (None in row):
        # Row is already solved, nothing to change
        return row
    elif not (True in row):
        # No block already in the row, simple_spaces cannot improve the result
        return row
    else:
        row1 = read_simple_spaces(row_counts, row)
        
        if row1 != False:  
            row_counts_rev = copy(row_counts)
            row_counts_rev.reverse()
            row_rev = copy(row)
            row_rev.reverse()        
            row2 = read_simple_spaces(row_counts_rev, row_rev)

            if row2 != False:
                row2 = reverse(row2)
                row_out = get_common(row1, row2)
                row_out = convert(row_out)
                row_out = recover(row, row_out)
        
                return row_out
            return row
        return row

def read_simple_spaces(row_counts, row):
    """ Read a line in *only* one way, trying to put
        spaces where it can
        
        3,1 [_ _ _ # _ _  _  _ #  _]
        
            [0 0 0 1 1 1 -1 -1 2 -2] """
    length = len(row)
    nbr = len(row_counts)
    row_out = [None]*length
        
    # Number of block still to be written
    blocks = 0
    # If space, a space need to be written after the blocks
    space = False
    # Current row_count number
    cur_n = 0
    # List of spaces that may be replaced by blocks
    list_free_spaces = []
        
    for i in xrange(length):
        if (row[i] == True) and (blocks == 0) and (not space):
            # A new serie of block start here
            cur_n += 1
            if nbr < cur_n:
                continue
            blocks = row_counts[cur_n-1]
            space = True
            
        if (blocks == 0) and (space):
            # A space need to be added here
            if row[i] != True:
                space = False
                row_out[i] = -cur_n
            # If a block was in the input row
            elif row[i] == True and len(list_free_spaces) > 0:
                # Move previous block to the begining of the blocks serie...
                row_out[i-1] = -cur_n
                row_out[list_free_spaces[-1]] = cur_n
                # ...and start a new block serie
                cur_n += 1
                blocks = row_counts[cur_n-1]
            else:
                return False
            # Reset the list of free spaces as the previous blocks serie
            # has been successfully added
            list_free_spaces = []     

        if blocks != 0:
            # Add a block (numbered by the counter n)
            blocks -= 1
            row_out[i] = cur_n
        else:
            # A space is added (no forced space and no block left)
            row_out[i] = -cur_n
            list_free_spaces.append(i)

    if cur_n < nbr:            
        # Some row_counts haven't been written, something went wrong
        # this cancel the work done on this row
        return False
        
    if (blocks != 0):
        # Some blocks are outside the row ...
        if len(list_free_spaces) < blocks:
            # .... and this can't be sorted out
            return False
        else:
            for i in xrange(blocks):
                row_out[list_free_spaces[-1]] = cur_n
                list_free_spaces.pop(-1)
    return row_out

def forcing(row_counts, row):
    """ Look if some counts can only be placed in some spaces
        Also check if some unknown space is sure to be empty
     3,2 [_ _ _ _ . _ . _ _ _]
    
         [# # # . . . . # # .]
         [. # # # . . . . # #]
            | |   | | |   |
         [_ # # _ . . . _ # _]  """
    
    if not (None in row):
        # Row is already solved, nothing to change
        return row
    elif not (False in row):
        # No "space" in the row, "forcing" does not apply
        return row
    else:
        row1 = read_forcing(row_counts, row)
        
        if row1 != False:     
            row_counts_rev = copy(row_counts)
            row_counts_rev.reverse()
            row_rev = copy(row)
            row_rev.reverse()        
            row2 = read_forcing(row_counts_rev, row_rev)
            
            if row2 != False: 
                row2 = reverse(row2)
            
                row_out = get_common(row1, row2)
                row_out = convert(row_out)
                row_out = recover(row, row_out)
        
                return row_out
            return row
        return row
        
def read_forcing(row_counts, row):
    """ Read a line in *only* one way, trying to put
        row_counts blocks where it can
    
     3,2 [_ _ _ _   . _   . _ _  _]
    
         [1 1 1 -1 -1 -1 -1 2 2 -2] """
         
    length = len(row)
    nbr = len(row_counts)
    row_out = [None]*length
    pos = 0
    for i in xrange(nbr):
        while not fit(row, row_counts[i], pos):
            # Add a space
            if pos >= length:
                return False
            row_out[pos] = -i
            pos += 1
        for j in xrange(row_counts[i]):
            row_out[pos+j] = i+1
        if pos+row_counts[i] < length:
            # Add a space after the blocks serie
            row_out[pos+row_counts[i]] = -(i+1)
        pos += row_counts[i]+1
    for i in xrange(pos, length):
        # Add a space
        row_out[i] = -nbr
        
    return row_out

def glue(row_counts, row):
    """ Look at the first clue and add some blocks and/or spaces
        if it is close enough from the corner
     3,2 [_ . _ # _ _ _ _ _ _]
     
         [. . _ # # _ _ _ _ _] """
    length = len(row)
    if not (None in row):
        # Row is already solved, nothing to change
        return row
    elif len(row_counts) == 0:
        # No counts, so the line is full of "spaces"
        return [False]*length
    elif not (True in row):
        # No "block" in the row, "glue" does not apply
        return row
    else:
        row_out = copy(row)
        count = row_counts[0]
        for position in xrange(length):
            if fit(row, count, position):
                # Check if Glue can apply there
                if (True in row[position:position+count]):
                    # Check if we can fill everything with blocks
                    if ((length > position + count) and
                        (row[position + count] == False)):
                        adding_block = True
                    else:
                        adding_block = False
                    # Add Blocks
                    for local_pos in xrange(count):
                        if row_out[position + local_pos]:
                            adding_block = True
                        if adding_block:
                            row_out[position + local_pos] = True
                    # Add a space after if the blocks serie is complete
                    if row[position] and length > position + count:
                        row_out[position + count] = False                      
                        row_out = (row_out[0:position + count] + 
                           glue(row_counts[1:], row_out[position + count:]))
                return row_out
            else:
                # Blocks don't fit, so Add a space
                row_out[position] = False
        return row

def get_permutations(row_counts, row):
    """ returns all possible solutions of a row
    """
    length = len(row)
    if len(row_counts) == 0:
        return [[False]*length]

    permutations = []
    maxblankspaces = length - sum(row_counts) - len(row_counts) + 1
    for start in xrange(maxblankspaces + 1):
        permutation = []
        invalid = False 
        # Add spaces at the begining of the line
        for position in xrange(start):
            permutation.append(False)
            # If a space can't be put there, mark case as invalid
            if row[position] == True:
                invalid = True
        if invalid:
            continue
        
        # Add the first blocks serie
        for position in xrange(start, start + row_counts[0]):
            permutation.append(True)
            # If a block can't be put there, mark case as invalid
            if row[position] == False:
                invalid = True
        if invalid:
            continue
        
        # Add a space after the blocks serie
        position = start + row_counts[0]
        if position < length:
            permutation.append(False)
            # If a space can't be put there, mark case as invalid
            if row[position] == True:
                invalid = True
            position += 1
        if invalid:
            continue
        
        # If we have reached the end of the row, add the permutation to the list
        if position == length:
            permutations.append(permutation)
            continue
        
        # Restart the process on the sub-section of the line
        sub_start = position
        sub_rows = get_permutations(row_counts[1:len(row_counts)],
                                    row[sub_start:length])
        # Create as may permutations as there is permutations in the sub-section
        for sub_row in sub_rows:
            sub_permutation = copy(permutation)
            for position in xrange(sub_start, length):
                sub_permutation.append(sub_row[position-sub_start])
            permutations.append(sub_permutation)
    return permutations

def solve_row(permutations, row):
    """ Returns the list of permutations that matches the given row
    and also returns the row with all elements
    that are common to all those permutations
    """
    length = len(row)
    valid_permutations = []
    for permutation in permutations:
        valid = True
        for position in xrange(length):
            if row[position] != None and row[position] != permutation[position]:
                valid = False
        if valid:
            valid_permutations.append(permutation)
    
    nbr_perm = len(valid_permutations)
    if nbr_perm == 0:
        print("Aucune permutation valide trouvée")
        print("Ligne:")
        print_row(row)
        print("Permutations: "+str(permutations))

    new_row = copy(valid_permutations[0])
    for permutation in valid_permutations[1:nbr_perm]:
        for position in xrange(length):
            if new_row[position] != permutation[position]:
                new_row[position] = None
    return valid_permutations, new_row

def check_solution(grid):
    """ Check if the solution matches the counts
    """
    if not grid.is_complete():
        return False
    else:
        col_counts = []
        for col in grid.get_cols():
            col_counts.append([])
            count = 0
            for item in col:
                if item:
                    count += 1
                else:
                    if count != 0:
                        col_counts[-1].append(count)
                    count = 0
            if count != 0:
                col_counts[-1].append(count)
        
        row_counts = []
        for row in grid.get_rows():
            row_counts.append([])
            count = 0
            for item in row:
                if item:
                    count += 1
                else:
                    if count != 0:
                        row_counts[-1].append(count)
                    count = 0
            if count != 0:
                row_counts[-1].append(count)
                   
        return ((row_counts == grid.row_counts) and
                (col_counts == grid.col_counts))

def print_grid(grid):
    """ pretty print of the grid with counts
    """    
    # Size on the left space
    size_row_counts = 0
    for count in grid.row_counts:
        size_row_counts = max(size_row_counts, 
                              len(''.join([str(t)+' ' for t in count])))
    disp_row_counts = []
    empty = [' ' for t in xrange(size_row_counts)]
    
    # Display clues in columns
    height_col_counts = 0
    for col in grid.col_counts:
        height_col_counts = max(height_col_counts, len(col))
        
    width_col = 0
    for col in grid.col_counts:
        for count in col:
            width_col = max(width_col, len(str(count)))
    colempty = ''.join([' ' for t in xrange(width_col)])
    disp_col_counts = []        
    for line_nbr in xrange(height_col_counts):
        line = ''
        for j in grid.col_counts:
            try:
                count_str = str(j[-(line_nbr+1)])
            except:
                line += colempty+' '
            else:
                line += colempty[:-len(count_str)]+count_str+' '
        disp_col_counts.append(line)
    
    # Display the lines in the reverse order
    for line_nbr in xrange(height_col_counts-1, -1, -1):
        print(''.join(empty)+disp_col_counts[line_nbr])
        
    # Counts in lines
    for row_count in grid.row_counts:
        line = ''.join([str(t)+' ' for t in row_count])
        disp_row_counts.append(''.join(empty[:-len(line)])+line)

    # Display clues in line + lines
    for row_nbr in xrange(len(grid.get_rows())):
        line = disp_row_counts[row_nbr]
        for item in grid.get_row(row_nbr):
            if item == True:
                line += colempty[:-1]+'# '
            elif item == False:
                line += colempty[:-1]+'. '
            else:
                line += colempty[:-1]+'  '
        print(line)
    return True

def print_row(row):
    """ pretty print of one row
    """    
    out = "["
    for item in row:
        if item == True:
            out += "#"
        elif item == False:
            out += "."
        else:
            out += " "
    out += "]"
    vprint(out)
    return True

if __name__ == "__main__":
    set_verbose(True)
 
    def unit_test(function, row_counts, row_in, row_out):
        """ This execute a test on one specific function and 
            checks that the quality of the output is as expected
        """        
        print("---")
        print("Test "+str(function.__name__))       
        row2 = function(row_counts, row_in)        
        print(row_counts)
        print_row(row_in)
        print_row(row2)

        error = False
        suboptimal = False
        information_lost = False
        for i in xrange(len(row_in)):
            if row_out[i] != row2[i]:
                if row_out[i] == None:
                    error = True
                else:
                    suboptimal = True
            if (row_in[i] != row2[i]) and ((row_in[i] == False) or 
                                           (row_in[i] == True)):
                information_lost = True
        if information_lost:
            print("Warning: some input information have been lost")

        if error:                        
            print("Error: line should be:")
            print_row(row_out)
            return "Error"
        elif suboptimal:
            print('Warning: suboptimal, line could have been:')
            print_row(row_out)
            return "Suboptimal"
        else:
            print("OK")
            return "OK"
    list_unit_test = []
    list_unit_test.append(unit_test(simple_boxes, [6],
            [None]*10,
            [None, None, None, None, True, True, None, None, None, None]))
    list_unit_test.append(unit_test(simple_boxes, [2, 3],
            [None]*10,
            [None]*10))
    list_unit_test.append(unit_test(simple_boxes, [5, 1],
            [None, None, None, None, None, None, False, True, None, None],
            [None, None, None, True, True, None, False, True, None, None]))
    list_unit_test.append(unit_test(simple_spaces, [2, 3],
            [None, True, True, None, None, True, True, True, None, None],
            [False, True, True, False, False, True, True, True, False, False]))
    list_unit_test.append(unit_test(simple_spaces, [3, 1],
            [None, None, None, True, None, None, None, None, True,  None],
            [False, None, None, True, None, None, False, False, True,  False]))
    list_unit_test.append(unit_test(simple_spaces, [3, 2],
            [None, None, None, True, None, None, None, None, None,  True],
            [False, None, None, True, None, None, False, False, True,  True]))
    list_unit_test.append(unit_test(simple_spaces, [3, 2],
            [None, None, True, None, None, True, None, None, None, None],
            [None, True, True, None, None, True, None, False, False, False]))
    list_unit_test.append(unit_test(forcing, [3, 2],
            [None, None, None, None, False, None, False, None, None, None],
            [None, True, True, None, False, False, False, None, True, None]))
    list_unit_test.append(unit_test(forcing, [3, 1],
            [None, None, None, None, False, None, False, None, None, None],
            [None, True, True, None, False, None, False, None, None, None]))
    list_unit_test.append(unit_test(forcing, [2],
            [None, None, None, False, None, False, None, None, None, False],
            [None, None, None, False, None, False, None, None, None, False]))
    list_unit_test.append(unit_test(forcing, [2],
            [None, None, None, False, None, False, None, False, None, False],
            [None, True, None, False, False, False, False, False, False, False]))
    list_unit_test.append(unit_test(glue, [3, 1],
            [None, False, False, None, True, None, None, None, None, None],
            [False, False, False, None, True, True, None, None, None, None]))
    list_unit_test.append(unit_test(glue, [3, 1],
            [None, False, False, None, None, True, None, None, None, None],
            [False, False, False, None, None, True, None, None, None, None]))
    list_unit_test.append(unit_test(glue, [3, 1],
            [None, True, None, None, None, None, None, None, None, None],
            [None, True, True, None, None, None, None, None, None, None]))
    list_unit_test.append(unit_test(glue, [3, 1],
            [True, None, None, None, None, None, None, None, None, None],
            [True, True, True, False, None, None, None, None, None, None]))
    list_unit_test.append(unit_test(glue, [3, 1],
            [None, None, False, True, True, None, None, None, None, None],
            [False, False, False, True, True, True, False, None, None, None]))
    list_unit_test.append(unit_test(glue, [3, 1],
            [None, None, False, True, True, None, None, True, None, None],
            [False, False, False, True, True, True, False, True, False, False]))
    list_unit_test.append(unit_test(simple_spaces, [2, 1, 2],
            [None, True, None, None, None, None, None, None, True, None],
            [None, True, None, None, None, None, None, None, True, None]))
    list_unit_test.append(unit_test(simple_spaces, [4],
            [False, False, None, None, True, True, None, None, False, False],
            [False, False, None, None, True, True, None, None, False, False]))
    list_unit_test.append(unit_test(glue, [1, 3, 1],
            [True, False, None, True, True, False, None, None, None, None],
            [True, False, True, True, True, False, None, None, None, None]))
    list_unit_test.append(unit_test(simple_spaces, [3, 1],
            [None, None, None, None, True, True, None, None, None, None],
            [False, False, False, None, True, True, None, None, None, None]))
    print('---')
    print("{} OK, {} Suboptimal, {} Error, on {} Tests".format(
          list_unit_test.count("OK"), list_unit_test.count("Suboptimal"),
          list_unit_test.count("Error"), len(list_unit_test)))
