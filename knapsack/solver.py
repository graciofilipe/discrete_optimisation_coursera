#!/usr/bin/python
# -*- coding: utf-8 -*-
from ortools.algorithms import pywrapknapsack_solver

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
            KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER,
        'test')

    values = []
    weights = []
    for line_idx in range(1, item_count+1):
        line = lines[line_idx]
        parts = line.split()
        #val we
        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    weights=[weights]

    solver.Init(values, weights, [capacity])

    solver.Solve()

    packed_items = [x for x in range(0, len(weights[0]))
                    if solver.BestSolutionContains(x)]

    bool_items = []
    for i in range(item_count):
        if i in packed_items:
            bool_items.append(1)
        else:
            bool_items.append(0)


    packed_weights = [weights[0][i] for i in packed_items]

    # prepare the solution in the specified output format
    output_data = str(sum(packed_weights)) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, bool_items))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

