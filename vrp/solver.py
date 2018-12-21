#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


def print_solution(data, routing, assignment):
    """Print routes on console."""
    total_dist = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {0}:\n'.format(vehicle_id)
        route_dist = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = routing.IndexToNode(index)
            next_node_index = routing.IndexToNode(assignment.Value(routing.NextVar(index)))
            route_dist += distance(
                data["locations"][node_index],
                data["locations"][next_node_index])
            route_load += data["demands"][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            index = assignment.Value(routing.NextVar(index))

        node_index = routing.IndexToNode(index)
        total_dist += route_dist
        plan_output += ' {0} Load({1})\n'.format(node_index, route_load)
        plan_output += 'Distance of the route: {0}m\n'.format(route_dist)
        plan_output += 'Load of the route: {0}\n'.format(route_load)
        print(plan_output)
    print('Total Distance of all routes: {0}m'.format(total_dist))


def distance(customer1, customer2):
    return math.sqrt((customer1[0] - customer2[0])**2 + (customer1[1] - customer2[1])**2)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    data = {}
    data['locations'] = {}
    data['demands'] = {}
    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    data['num_locations'] = customer_count
    data['num_vehicles'] = vehicle_count
    data["depot"] = 0
    data['vehicle_capacities'] = [vehicle_capacity]*vehicle_count
    
    customers = []
    for i in range(customer_count):
        line = lines[i]
        parts = line.split()
        data['locations'][i] = (float(parts[1]), float(parts[2]))
        data['demands'][i] = int(parts[0])

    #the depot is always the first customer in the input
    depot = 0

    def create_distance_callback(data):
        """Creates callback to return distance between points."""
        _distances = {}

        for from_node in range(data["num_locations"]):
            _distances[from_node] = {}
            for to_node in range(data["num_locations"]):
                if from_node == to_node:
                    _distances[from_node][to_node] = 0
                else:
                    _distances[from_node][to_node] = (
                        distance(data["locations"][from_node],
                                 data["locations"][to_node]))

        def distance_callback(from_node, to_node):
            """Returns the manhattan distance between the two nodes"""
            return _distances[from_node][to_node]

        return distance_callback

    def create_demand_callback(data):
        """Creates callback to get demands at each location."""

        def demand_callback(from_node, to_node):
            return data["demands"][from_node]

        return demand_callback

    def add_distance_dimension(routing, distance_callback):
        """Add Global Span constraint"""
        distance = 'Distance'
        maximum_distance = 3000  # Maximum distance per vehicle.
        routing.AddDimension(
            distance_callback,
            0,  # null slack
            maximum_distance,
            True,  # start cumul to zero
            distance)
        distance_dimension = routing.GetDimensionOrDie(distance)
        # Try to minimize the max distance among vehicles.
        distance_dimension.SetGlobalSpanCostCoefficient(100)

    def add_capacity_constraints(routing, data, demand_callback):
        """Adds capacity constraint"""
        capacity = "Capacity"
        routing.AddDimensionWithVehicleCapacity(
            demand_callback,
            0,  # null capacity slack
            data["vehicle_capacities"],  # vehicle maximum capacities
            True,  # start cumul to zero
            capacity)




    """Entry point of the program"""
    # Create Routing Model
    routing = pywrapcp.RoutingModel(
        data["num_locations"],
        data["num_vehicles"],
        data["depot"])
    # Define weight of each edge
    distance_callback = create_distance_callback(data)
    routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)
    # Add Capacity constraint
    demand_callback = create_demand_callback(data)
    add_capacity_constraints(routing, data, demand_callback)
    # Setting first solution heuristic (cheapest addition).
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    print_solution(data, routing, assignment)
    print('that was it')

    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []
    
    remaining_customers = set(customers)
    remaining_customers.remove(depot)
    
    for v in range(0, vehicle_count):
        # print "Start Vehicle: ",v
        vehicle_tours.append([])
        capacity_remaining = vehicle_capacity
        while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            order = sorted(remaining_customers, key=lambda customer: -customer.demand)
            for customer in order:
                if capacity_remaining >= customer.demand:
                    capacity_remaining -= customer.demand
                    vehicle_tours[v].append(customer)
                    # print '   add', ci, capacity_remaining
                    used.add(customer)
            remaining_customers -= used

    # checks that the number of customers served is correct
    assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += distance(depot,vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += distance(vehicle_tour[i],vehicle_tour[i+1])
            obj += distance(vehicle_tour[-1],depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    return outputData


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

