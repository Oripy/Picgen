# -*- coding: utf-8 -*-
"""
Methods to display half-solved grids and clues of a problem
"""

def display_nonogram(grid):
    """ Output the HTML code to display a nonogram problem """
    height_col_counts = 0
    for col_count in grid.col_counts:
        height_col_counts = max(height_col_counts, len(col_count))
    
    width_row_counts = 0
    for row_count in grid.row_counts:
        width_row_counts = max(width_row_counts, len(row_count))
    
#    out = '<div class="outline">'
    out = '<input id="table" type="hidden" disabled=True size=100 value="{}" />'.format(encode_table(grid.get_grid()))

    for line_nbr in xrange(height_col_counts-1, -1, -1):
        line = '<div class="picture">'
        for _ in xrange(width_row_counts):
            line += '<div class="empty">&nbsp;</div>'
        for col_count in grid.col_counts:
            if len(col_count) > line_nbr:
                line += '<div class="clues">'
                line += str(col_count[-line_nbr-1])
            else:
                line += '<div class="empty">'
                line += "&nbsp;"
            line += '</div>'
        line += '</div>'
        out += line
    
    for row_nbr in xrange(grid.height):
        line = '<div class="picture">'
        for col_nbr in xrange(width_row_counts-1, -1, -1):
            if len(grid.row_counts[row_nbr]) > col_nbr:
                line += '<div class="clues">'
                line += str(grid.row_counts[row_nbr][-col_nbr-1])
            else:
                line += '<div class="empty">'
                line += '&nbsp;'
            line += '</div>'
        for col_nbr in xrange(grid.width):
            if grid.get_value(col_nbr, row_nbr) == None:
                image = "unknow.png"
            elif grid.get_value(col_nbr, row_nbr) == True:
                image = "black.png"
            else:
                image = "white.png"
#            line += """<a href="/?row={row}&col={col}">
#                        <img class="case" src="images/{image}" />
#                    </a>
#                    """.format(row=row_nbr, col=col_nbr, image=image)
            line += """<a href="#" id=linkcell{row}{col} onclick="doChangeCell({row}, {col})">
                    <img class="case" id=cell{row}{col} src="images/{image}" />
                    </a>
                    """.format(row=row_nbr, col=col_nbr, image=image)
        line += '</div>'
        out += line
    
#    out += '</div><br />'
    out += '<br />&nbsp;<br />'
    
    return out
    
def encode_table(table):
    out = ''
    for row_nbr in xrange(len(table)):
        for col_nbr in xrange(len(table[0])):
            if table[row_nbr][col_nbr] == None:
                out += '2'
            elif table[row_nbr][col_nbr] == True:
                out += '1'
            else:
                out += '0'
    return out