#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Carleton Coffrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
def generage_set_coverage_vector(s, total_items):
    items = s.items
    set_coverage_vector = [0 for _ in range(total_items)]
    for item in items:
        set_coverage_vector[item]=1
    return set_coverage_vector


from collections import namedtuple
from ortools.sat.python import cp_model




Set = namedtuple("Set", ['index', 'cost', 'items'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, float(parts[0]), map(int, parts[1:])))

    cpmodel = cp_model.CpModel()
    set_list_binary = [cpmodel.NewIntVar(0, 1, 'set_{i}'.format(i=i)) for i in range(set_count)]
    total_cost = sum([int(s.cost)*set_list_binary[s.index] for s in sets])

    set_coverage_list = []
    for s in sets:
        set_coverage_vec = generage_set_coverage_vector(s, total_items=item_count)
        set_coverage_list.append(set_coverage_vec)

    for item in range(item_count):
        item_cover = 0
        for s in sets:
            item_cover += set_coverage_list[s.index][item]*set_list_binary[s.index]
        cpmodel.Add(item_cover>0)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 666.0

    cpmodel.Minimize(total_cost)

    print('about to solve')
    status = solver.Solve(cpmodel)
    print('status', status)
    print('cp_model.OPTIMAL', cp_model.OPTIMAL)
    print('solved')
    solution = [solver.Value(set_list_binary[i]) for i in range(set_count)]
    final_cost = solver.ObjectiveValue()
    print('obj value', final_cost)





    # prepare the solution in the specified output format
    output_data = str(final_cost) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')

