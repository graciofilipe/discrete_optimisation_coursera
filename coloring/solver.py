#!/usr/bin/python
# -*- coding: utf-8 -*-

from ortools.sat.python import cp_model
import networkx as nx
from collections import Counter
from ortools.linear_solver import pywraplp





def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    print('\n')

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    print('node_cunt', node_count)
    print('edget cunt', edge_count)
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a solution with CP MODEL
    cpmodel = cp_model.CpModel()
    n_colors_used = cpmodel.NewIntVar(0, node_count, 'n_cols')
    node_color_cp = [cpmodel.NewIntVar(0, node, 'node_{}'.format(node))
              for node in range(node_count)]

    # make the edge constraints
    G = nx.Graph()
    for edge in edges:
        ni = edge[0]
        nj = edge[1]
        G.add_edge(ni, nj)
        cpmodel.Add(node_color_cp[ni]!=node_color_cp[nj])

    # every color has to be lower than n_colors
    for node_idx in range(node_count):
        cpmodel.Add(node_color_cp[node_idx] <= n_colors_used)



    #cliques = list(nx.algorithms.clique.find_cliques(G))
    #print('len_cliques', len(cliques))
    #clique_len = list(map(len, cliques))
    #max_len = max(clique_len)
    #print('max_len', max_len)
    #reduced_cliques = [clique for clique in cliques if len(clique)>=max_len-20]
    #print('len_reduced_cliques', len(reduced_cliques))
    #print('done with clique finding')
    #for clique in cliques:
    #    cpmodel.AddAllDifferent([node_color_cp[i] for i in clique])


    ## DEFine AUX VAR That IS NUMBER OF COLORS


    print('done adding constraints')
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 666.0


    obj_fun = n_colors_used
    cpmodel.Minimize(obj_fun)

    print('about to solve')
    status = solver.Solve(cpmodel)
    print('status', status)
    print('cp_model.OPTIMAL', cp_model.OPTIMAL)
    print('solved')
    solution_node_colors = [solver.Value(node_color_cp[i]) for i in range(node_count)]

    print('obj_fun', obj_fun)
    print('obj value', solver.ObjectiveValue())
    # prepare the solution in the specified output format
    output_data = str(solver.Value(n_colors_used)) + ' ' + str(0) + '\n'
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

