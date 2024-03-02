import itertools
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List

import numpy as np

from src.models.delivery import Delivery
from src.models.depot import Depot
from src.models.event import Event
from src.models.node import Node
from src.models.pickup import Pickup
from src.models.route import Route
from src.models.vehicle import Vehicle


@dataclass
class TSPSolver:
    """
    Traveling Salesman Problem solver using Branch and Bound algorithm.
    The algorithm is used to solve the TSP for the given distance matrix and events.
    Events are the pickup and delivery events. The algorithm is used to find the optimal route for the vehicle to visit all the events.

    A route is a path that starts and ends at the depot.
    """
    depot: Depot
    events: List[Event]  # pickup and deliveries
    vehicle: Vehicle
    distance_matrix: np.ndarray

    depot_to_delivery: Depot = field(init=False)
    depot_to_return: Depot = field(init=False)
    optimal_route: Route = field(init=False)

    def __post_init__(self):
        total_delivery_capacity = sum([event.capacity for event in self.events if isinstance(event, Delivery)])
        self.depot_to_delivery = Depot(id=self.depot.id, x=self.depot.x, y=self.depot.y, capacity=total_delivery_capacity)

        total_pickup_capacity = sum([event.capacity for event in self.events if isinstance(event, Pickup)])
        self.depot_to_return = Depot(id=self.depot.id, x=self.depot.x, y=self.depot.y, capacity=total_pickup_capacity, is_return=True)

        if self.depot_to_delivery.capacity > self.vehicle.capacity:
            raise ValueError("Vehicle capacity is less than the total delivery capacity")

        self.count = 0

    def solve(self) -> Route:
        optimal_route = Route(events=[], total_distance=float('inf'))
        deepest_level = len(self.events)
        best_cost = float('inf')

        PQ = PriorityQueue()
        start_node = Node(level=0, path=[self.depot_to_delivery], bound=0)
        PQ.put(start_node)

        node_to_iterate = Node()
        while not PQ.empty():
            most_promising_node = PQ.get()

            if most_promising_node.bound < best_cost:
                node_to_iterate.level = most_promising_node.level + 1
                remaining_events = set(self.events) - set(most_promising_node.path)
                for i in remaining_events:
                    node_to_iterate.path = most_promising_node.path[:] + [i]
                    node_to_iterate.bound_without_returning = most_promising_node.bound_without_returning

                    if node_to_iterate.level == (deepest_level - 1):  # if all events are visited
                        l = remaining_events - {i}
                        node_to_iterate.path.append(l.pop())
                        node_to_iterate.path.append(self.depot_to_return)

                        route_distance = node_to_iterate.bound_without_returning + (
                                    self.distance_matrix[node_to_iterate.path[-4].id][node_to_iterate.path[-3].id]
                                    + self.distance_matrix[node_to_iterate.path[-3].id][node_to_iterate.path[-2].id]
                                    + self.distance_matrix[node_to_iterate.path[-2].id][node_to_iterate.path[-1].id])

                        is_route_feasible = self.is_permutation_feasible(node_to_iterate.path[:-1])

                        if (route_distance < best_cost) and is_route_feasible:
                            best_cost = route_distance
                            optimal_route = Route(events=node_to_iterate.path, total_distance=route_distance)

                    else:
                        is_path_contain_pickup = isinstance(node_to_iterate.path[-1], Pickup)

                        is_route_feasible = True
                        if is_path_contain_pickup:
                            is_route_feasible = self.is_permutation_feasible(node_to_iterate.path)

                        if is_route_feasible:
                            node_to_iterate.bound, node_to_iterate.bound_without_returning = self.bound(node_to_iterate)
                            if node_to_iterate.bound < best_cost:
                                PQ.put(node_to_iterate)

                    node_to_iterate = Node(level=node_to_iterate.level)

        print(optimal_route.total_distance, [event.id for event in optimal_route.events])
        return optimal_route

    def find_initial_route(self):
        route = Route()
        for permutation in itertools.permutations(self.events):
            p_list = list(permutation)
            is_feasible = self.is_permutation_feasible(p_list)
            if is_feasible:
                route.events = p_list
                break

        route.events.append(self.depot_to_return)
        route.total_distance = self.length(route.events)
        print('initialized', route.total_distance)
        return route

    def length(self, events: List[Event]) -> float:
        self.count += 1
        # distances = self.distance_matrix
        # event_ids = [event.id for event in events]
        # return np.sum(distances[event_ids[:-1], event_ids[1:]])
        return sum([self.distance_matrix[events[i].id][events[i + 1].id] for i in range(len(events) - 1)])

    def bound(self, node: Node):
        bound_without_returning = node.bound_without_returning + self.distance_matrix[node.path[-2].id][node.path[-1].id]
        bound = bound_without_returning + self.distance_matrix[node.path[-1].id][self.depot_to_return.id]
        return bound, bound_without_returning

    def is_permutation_feasible(self, events) -> bool:
        remaining_capacity = self.vehicle.capacity

        for event in events:
            if isinstance(event, Pickup):
                remaining_capacity -= event.capacity
                if remaining_capacity < 0:  # if the vehicle's capacity is exceeded with the current pickup
                    return False
                else:  # due to single pickup
                    return True
            elif isinstance(event, Delivery):
                remaining_capacity += event.capacity
            elif isinstance(event, Depot) and not event.is_return:
                remaining_capacity -= event.capacity
