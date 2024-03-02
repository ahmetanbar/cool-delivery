from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List

import numpy as np

from src.models.delivery import Delivery
from src.models.depot import Depot
from src.models.event import Event
from src.solvers.TSPWithBranchAndBound.models.node import Node
from src.models.pickup import Pickup
from src.models.route import Route
from src.models.vehicle import Vehicle


@dataclass
class Solver:
    """
    Traveling Salesman Problem solver using Branch and Bound algorithm.
    The algorithm is used to solve the TSP for the given distance matrix and events.
    Events are the pickup and delivery events. The algorithm is used to find the optimal route for the vehicle to visit all the events.

    A route is a path that starts and ends at the depot.

    It doesn't use original Branch and Bound algorithm. It uses a modified version of the algorithm.
    Bounds are calculated using the distance matrix and the capacity of the vehicle.
    """
    depot: Depot
    events: List[Event]  # pickup and deliveries
    vehicle: Vehicle
    distance_matrix: np.ndarray

    depot_to_delivery: Depot = field(init=False)
    depot_to_return: Depot = field(init=False)
    optimal_route: Route = field(init=False)
    deepest_level: int = field(init=False)
    best_cost: float = field(init=False)
    priority_queue: PriorityQueue = field(init=False)

    def __post_init__(self):
        # Initialize depot events.
        self.initialize_depot_events()

        # Initialize the solver variables.
        self.optimal_route = Route(events=[], total_cost=float('inf'))
        self.deepest_level = len(self.events)
        self.best_cost = float('inf')
        self.priority_queue = PriorityQueue()

    def initialize_depot_events(self):
        total_delivery_capacity = sum([event.capacity for event in self.events if isinstance(event, Delivery)])
        self.depot_to_delivery = Depot(id=self.depot.id, x=self.depot.x, y=self.depot.y, capacity=total_delivery_capacity)

        total_pickup_capacity = sum([event.capacity for event in self.events if isinstance(event, Pickup)])
        self.depot_to_return = Depot(id=self.depot.id, x=self.depot.x, y=self.depot.y, capacity=total_pickup_capacity, is_return=True)

        if self.depot_to_delivery.capacity > self.vehicle.capacity or self.depot_to_return.capacity > self.vehicle.capacity:
            raise ValueError("Delivery capacity exceeds vehicle capacity.")

    def solve(self) -> Route:
        start_node = Node(capacity=self.vehicle.capacity)
        _ = start_node.add_event(self.depot_to_delivery)
        self.priority_queue.put(start_node)

        while not self.priority_queue.empty():
            most_promising_node: Node = self.priority_queue.get()

            if most_promising_node.bound < self.best_cost:
                most_promising_node.level += 1
                remaining_events = set(self.events).difference(most_promising_node.path)
                for remaining_event in remaining_events:
                    self.iterate_remaining_event(most_promising_node, remaining_event, remaining_events)

        print(self.optimal_route)
        return self.optimal_route

    def bound(self, node: Node):
        bound_without_returning = node.bound_without_returning + self.distance_matrix[node.path[-2].id][node.path[-1].id]
        bound = bound_without_returning + self.distance_matrix[node.path[-1].id][self.depot_to_return.id]
        return bound, bound_without_returning

    def iterate_remaining_event(self, most_promising_node, remaining_event, remaining_events):
        """
        Iterate the remaining events and put the node to the queue if the bound is less than the best cost.
        If the node is reached to the leaf node, then check if the route is optimal and set the optimal route if it is.
        """
        node_to_iterate = Node(level=most_promising_node.level,
                               capacity=most_promising_node.capacity,
                               bound_without_returning=most_promising_node.bound_without_returning,
                               path=most_promising_node.path[:])

        is_added = node_to_iterate.add_event(remaining_event)
        if not is_added:
            return

        node_to_iterate.bound, node_to_iterate.bound_without_returning = self.bound(node_to_iterate)

        if self.is_node_reach_to_leaf_node(node_to_iterate):
            left_events = remaining_events - {remaining_event}
            leaf_event = left_events.pop()

            is_added = node_to_iterate.add_event(leaf_event)
            if not is_added:
                return

            self.check_and_set_optimal_route_if_route_is_optimal(node_to_iterate)

        else:
            self.compare_and_put_node_to_queue(node_to_iterate)

        return

    def compare_and_put_node_to_queue(self, node: Node):
        if node.bound < self.best_cost:
            self.priority_queue.put(node)

    def check_and_set_optimal_route_if_route_is_optimal(self, node: Node):
        node.bound, node.bound_without_returning = self.bound(node)
        route_distance = node.bound
        if route_distance < self.best_cost:
            self.best_cost = route_distance
            self.optimal_route = Route(events=node.path + [self.depot_to_return], total_cost=route_distance)

    def is_node_reach_to_leaf_node(self, node: Node):
        return node.level == (self.deepest_level - 1)
