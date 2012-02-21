# -*- coding: utf-8 -*-
"""
A module that introduce 
"""

import solver
import picgen
from random_gen import next_rand_LCG

def next_valid_number(previous):
    """ Find the next solvable grid """
    trials = 0
    number = previous
    while True:
        number = next_rand_LCG(number)
        table = picgen.number_to_table(number, 5, 5)
        col_counts, row_counts = solver.get_counts(table)
        grid = solver.Grid(col_counts, row_counts)
        grid = solver.solve(grid)
        if grid.is_complete():
            break
        else:
            trials += 1
    return number, trials

if __name__ == "__main__":
    list_nbr = []
    number = 0
    nbr_tests = 10

    for i in xrange(nbr_tests):
        number, nbr = next_valid_number(number)
        print("-{}-".format(picgen.number_to_name(number)))
        picgen.show_name(picgen.number_to_name(number), 5, 5)
        list_nbr.append(nbr)

    print("maximum: {}".format(max(list_nbr)))
    print("minimum: {}".format(min(list_nbr)))
    print("mean: {}".format(sum(list_nbr)/(nbr_tests*1.)))
