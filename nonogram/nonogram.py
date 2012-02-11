# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 11:36:55 2012

@author: pmaurier
"""
from __future__ import print_function

from time import time
import cProfile, pstats
import argparse
import solver

def load_from_file(filename):
    """ Load a grid from a 2-lines file with the following format:
        4x4
        1.2/1.1/1/2/1/3/1.1/2
    """
    input_file = open(filename)
    # File format Simon Tatham-like (import only empty grids)
    lines = input_file.readlines()
    
    # Load grid size
    width, height = [int(i) for i in lines[0].split('x')]
    
    # Load col_counts and row_counts
    counts = lines[1].split('/')
    col_counts = []
    for col_nbr in xrange(width):
        col_counts.append([int(i) for i in counts[col_nbr].split('.')])
    row_counts = []
    for row_nbr in xrange(height):
        row_counts.append([int(i) for i in counts[width+row_nbr].split('.')])

    # The grid
    return solver.Grid(width, height, col_counts, row_counts)

def main():
    """ Main program    
    """
    parser = argparse.ArgumentParser(description='Solve nonograms.')
    parser.add_argument('filename', help='Filename of the grid input')
    parser.add_argument('-t', '--trials', type=int, default=-1,
                        help='Number of calculations')
    parser.add_argument('-p', '--profile', action='store_true',
                        help="""Profile one calculations 
                        (expect longer calculation time)""")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='set a verbose output')
    
    args = parser.parse_args()
    
    nbr = args.trials

    # Define a function for verbose output
    vprint = print if args.verbose else lambda *a, **k: None
    solver.set_verbose(args.verbose)    
    
    grid = load_from_file(args.filename)
    
    if args.profile:
        if nbr == -1:
            nbr = 0
        cProfile.runctx('solver.solve(grid)', globals(), locals(), 'stats.stat')
        stats = pstats.Stats('stats.stat')        
        stats.strip_dirs()
        stats.sort_stats("time")
        stats.print_stats()
    
    if nbr == -1:
        nbr = 1
    
    tot = []
    for _ in xrange(nbr):
        start = time()
        grid_sol = solver.solve(grid)
        timing = time()-start
        tot.append(timing)
        vprint("Total time: "+str(timing))
        vprint("---")

    if nbr > 0:
        if not solver.check_solution(grid_sol):
            print("Error, solution not found")
        print("Mean time on "+str(nbr)+
               " try: "+str(sum(tot)/nbr))
        print("Best: "+str(min(tot)))
        print("Worst: "+str(max(tot)))
        solver.print_grid(grid_sol)
        vprint(solver.check_solution(grid_sol)) 

if __name__ == "__main__":
    main()