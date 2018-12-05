#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


def build_distance_matrix(coordinates):
    distance_matrix =[]
    for point1 in coordinates:
        point1_distance_vector = []
        for point2 in coordinates:
            distance = length(point1, point2)
            point1_distance_vector.append(distance)
        distance_matrix.append(point1_distance_vector)
    return distance_matrix



# Distance callback
def create_distance_callback(dist_matrix):
  # Create a callback to calculate distances nodes

  def distance_callback(from_node, to_node):
    return int(dist_matrix[from_node][to_node])

  return distance_callback





Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))


    distance_matrix = build_distance_matrix(points)

    tsp_size = len(points)
    num_routes = 1
    starting_point = 0

    # Create routing model
    if tsp_size > 0:
        routing = pywrapcp.RoutingModel(tsp_size, num_routes, starting_point)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        # Create the distance callback.
        dist_callback = create_distance_callback(distance_matrix)
        routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        if assignment:
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
            route_number = 0
            index = routing.Start(route_number)  # Index of the variable for the starting node.
            route = ''
            while not routing.IsEnd(index):
                # Convert variable indices to node indices in the displayed route.
                route += str(routing.IndexToNode(index))
                index = assignment.Value(routing.NextVar(index))
            route += str(routing.IndexToNode(index))
        else:
            print('No solution found.')
    else:
        print ('Specify an instance greater than 0')


    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = route

    # calculate the length of the tour
    obj = str(assignment.ObjectiveValue())

    # prepare the solution in the specified output format
    output_data = obj + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

