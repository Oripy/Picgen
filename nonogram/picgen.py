# -*- coding: utf-8 -*-

import random

def rand_table(width, height):
    """ Create a random table given a dimension. """
    return [[random.randint(0,1) for _ in range(width)] for _ in range(height)]

def less_table(table):
    """ Output a table that is equivalent to given table
    (take the smallest number from the mirrored and/or reversed picture). """
    minNum = min(int(table_to_name(table)[0],36),
                 int(table_to_name(mirror(table))[0],36),
                 int(table_to_name(reverse(mirror(table)))[0],36),
                 int(table_to_name(reverse(table))[0],36))
    return name_to_table(base10toN(minNum,36), len(table), len(table[0]))
    
def number_possible(width, height):
    """ Returns the number of possible drawings given a dimension. """
    return 2**(width*height)

def number_less(width, height):
    """ Return the number of possible drawings given a dimension
        without mirrored and/or reversed doubles. """
    return number_possible(width, height)/4

# Conversions
def table_to_number(table):
    """ Convert a table to a list containing number and dimensions. """
    text = ""
    for i in table:
        for j in i:
            text += str(j)
    num = int(text,2)

    return [num, len(table), len(table[0])]    

def number_to_table(number, width, height):
    """ Convert a number and dimensions to a table. """
    size = width * height
    binary = str(bin(number))[2:]
    binaryStr = "".join(['0' for i in xrange(size-len(binary))])+binary
    
    table = []
    for i in xrange(width):
        table.append([])
        for j in xrange(height):
            table[i].append(int(binaryStr[i*height+j]))
    return table
    
def name_to_table(name, width, height):
    """ Convert a name and dimensions to a table. """
    return number_to_table(int(name,36), width, height)
    
def table_to_name(table):
    """ Convert a table to a list containing name and dimensions. """
    num, width, height = table_to_number(table)
    name = base10toN(num,36)
    return [name, width, height]
    
def name_to_number(name):
    """ Convert a name to a number """
    return int(name, 36)

def number_to_name(number):
    """ Convert a number to a name """
    return base10toN(number, 36)

# Tables transformations
def mirror(table):
    """ Create the mirror image of given table. """
    tableOut = []
    for j in xrange(len(table)):
        tableOut.append([])
        for i in xrange(len(table[0])):
            tableOut[j].append(table[-1*j-1][i])
    return tableOut

def reverse(table):
    """ Create the reversed image of given table. """
    tableOut = []
    for j in xrange(len(table)):
        tableOut.append([])
        for i in xrange(len(table[0])):
            if table[j][i]:
                tableOut[j].append(0)
            else:
                tableOut[j].append(1)
    return tableOut

# Pretty print of tables
def show_table(table):
    """ Print the drawing defined by the given table. """
    for i in table:
        text = ""
        for j in i:
            if j:
                text += "#"
            else:
                text += "."
        print text

def show_name(name, length, height):
    """ Print the drawing defined by the given name and dimensions. """
    show_table(name_to_table(name, length, height))

def show_number(number, length, height):
    """ Print the drawing defined by the given number and dimensions. """
    show_table(number_to_table(number, length, height))

# Tools
def base10toN(num,n):
    """ Change a  to a base-n number.
    Up to base-36 is supported without special notation. """
    num_rep={10:'a',
         11:'b',
         12:'c',
         13:'d',
         14:'e',
         15:'f',
         16:'g',
         17:'h',
         18:'i',
         19:'j',
         20:'k',
         21:'l',
         22:'m',
         23:'n',
         24:'o',
         25:'p',
         26:'q',
         27:'r',
         28:'s',
         29:'t',
         30:'u',
         31:'v',
         32:'w',
         33:'x',
         34:'y',
         35:'z'}
    new_num_string=''
    current=num
    while current!=0:
        remainder=current%n
        if 36>remainder>9:
            remainder_string=num_rep[remainder]
        elif remainder>=36:
            remainder_string='('+str(remainder)+')'
        else:
            remainder_string=str(remainder)
        new_num_string=remainder_string+new_num_string
        current=current/n
    return new_num_string

if __name__ == '__main__':

    height = 5
    width = 5
    
    table = less_table(rand_table(width, height))    
    # Tests de conversion
    show_name(*table_to_name(table))
    print "---"
    show_table(name_to_table(*table_to_name(table)))
    print "---"
    show_table(table)
    print "---"
    show_table(mirror(table))
    print str(table_to_name(table)[0])+".png"

