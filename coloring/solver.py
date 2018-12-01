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

    # build a solution with CP MODEL
    cpmodel = cp_model.CpModel()

    node_color_cp = [cpmodel.NewIntVar(0, node_count - 1, 'node_{}'.format(node))
              for node in range(node_count)]

    # make the edge constraints
    for edge in edges:
        ni = edge[0]
        nj = edge[1]
        # model.Add(node_color[ni]!=node_color[nj])
        cpmodel.Add(node_color_cp[ni] != node_color_cp[nj])

    sum_cols = sum(node_color_cp)
    cpmodel.Minimize(sum_cols)

    solver = cp_model.CpSolver()
    status = solver.Solve(cpmodel)
    solution_node_colors = [solver.Value(node_color_cp[i]) for i in range(node_count)]
    print(solution_node_colors)


    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution_node_colors))

    return output_data


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

