#!/usr/bin/python
# -*- coding: utf-8 -*-

from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp



def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a solution
    model = cp_model.CpModel()
    lp_solver = pywraplp.Solver('SolveIntegerProblem',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # initialise the variables
    node_color = [model.NewIntVar(0, node_count - 1, 'node_{}'.format(node))
              for node in range(node_count)]

    node_color_lp = [lp_solver.IntVar(0, node_count - 1, 'node_{}'.format(node))
                  for node in range(node_count)]

    # number of colors used
    color_bool_list = []
    for potential_color in range(node_count):
        color_exists = lp_solver.Sum([potential_color==node_color_lp[node] for node in range(node_count)]) >= 1
        color_bool_list.append(color_exists)

        

    n_colors = lp_solver.Sum(color_bool_list)

    lp_solver.Minimize(n_colors)


    # make the edge constraints
    for edge in edges:
        ni = edge[0]
        nj = edge[1]
        #model.Add(node_color[ni]!=node_color[nj])
        lp_solver.Add(node_color_lp[ni]!=node_color_lp[nj])

    result_status = lp_solver.Solve()

    for variable in node_color_lp:
        print('%s = %d' % (variable.name(), variable.solution_value()))


    # prepare the solution in the specified output format
    #output_data = str(node_count) + ' ' + str(0) + '\n'
    #output_data += ' '.join(map(str, solution))

    return 1


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

