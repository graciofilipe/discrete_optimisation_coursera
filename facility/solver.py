#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from ortools.linear_solver import pywraplp
from ortools.constraint_solver import pywrapcp

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    demand_vector = [c.demand for c in customers]
    capacity_vector = [f.capacity for f in facilities]
    fixed_costs_vector = [f.setup_cost for f in facilities]
    distance_matrix = []
    for fac in facilities:
        fac_distances = [length(fac.location, cust.location) for cust in customers]
        distance_matrix.append(fac_distances)



    # build a solution
    solver = pywraplp.Solver('SolveIntegerProblem',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    solver.SetTimeLimit(66*1000)

    facility_to_customer = {}
    for fac in range(facility_count):
        for cust in range(customer_count):
            facility_to_customer[(fac, cust)] = solver.BoolVar(name='f{f}_c{c}'.format(f=fac, c=cust))

    facilities_open_bool = [solver.BoolVar(name='f{f}'.format(f=f)) for f in range(facility_count)]

    print('reconcile the facilities open')
    for fac in range(facility_count):
        solver.Add(facilities_open_bool[fac]*2*customer_count >= solver.Sum([facility_to_customer[(fac, cust)] \
                                           for cust in range(customer_count)]))

    print('every customer is served by one and only one facility')
    for cust in range(customer_count):
        solver.Add(1 == solver.Sum([facility_to_customer[(fac, cust)] \
                                           for fac in range(facility_count)]))


    # capacity constraints
    for fac in range(facility_count):
        solver.Add(capacity_vector[fac] >= solver.Sum(
            [demand_vector[cust]*facility_to_customer[(fac, cust)] for cust in range(customer_count)]))


    # fixed costs
    fixed_costs_tmp = []
    for fac in range(facility_count):
        fixed_costs_tmp.append(facilities_open_bool[fac]*fixed_costs_vector[fac])
    fixed_costs = solver.Sum(fixed_costs_tmp)

    # transportation costs
    distances = []
    for fac in range(facility_count):
        for cust in range(customer_count):
            distances.append(facility_to_customer[(fac, cust)]*distance_matrix[fac][cust])
    total_distance = solver.Sum(distances)


    # total objective function
    objective_var = solver.Sum([total_distance, fixed_costs])
    objective = solver.Minimize(objective_var)
    solver.Solve()
    obj = int(solver.Objective().Value())


    #for fac in range(facility_count):
    #    for cust in range(customer_count):
    #        x = int(facility_to_customer[(fac, cust)].SolutionValue())
    #        print('facility:', fac, 'customer', cust, '-', x)



    solution = [fac for cust in range(customer_count) for fac in range(facility_count)\
                if int(facility_to_customer[(fac, cust)].SolutionValue()) ==1]

    print('done!')
    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

