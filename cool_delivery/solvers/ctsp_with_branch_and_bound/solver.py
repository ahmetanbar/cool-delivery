from dataclasses import dataclass, field
from queue import PriorityQueue
from loguru import logger
from cool_delivery.solvers import BaseSolver
from .node import Node
from cool_delivery.models import Route


@dataclass
class Solver(BaseSolver):
    """
    Capacitated Traveling Salesman Problem solver using Branch and Bound algorithm.
    The algorithm is used to find the optimal route for the vehicle to visit all the events. Events are the pickup and delivery events.
    The route is a path that starts and ends at the depot.

    It doesn't use the original Branch and Bound algorithm. It uses a modified version of the algorithm.
    Bounds are calculated using the distance matrix and the capacity of the vehicle.

    Best cost parameter is used to be able to start with a defined best cost value when searching in bounds.
    """
    best_cost: float = float('inf')
    deepest_level: int = field(init=False)
    priority_queue: PriorityQueue = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.priority_queue = PriorityQueue()

    def solve(self):
        if len(self.events) <= 1:
            self.handle_small_size_routes()
            return

        self.deepest_level = len(self.events)

        self.start_to_queue()

        while not self.priority_queue.empty():
            most_promising_node: Node = self.priority_queue.get()

            if most_promising_node.bound < self.best_cost:
                self.expand_and_evaluate_node(most_promising_node)

        logger.debug(self.optimum_route)

    def start_to_queue(self):
        start_node = Node(capacity=self.vehicle.capacity)
        _ = start_node.add_event(self.depot_to_delivery)
        self.priority_queue.put(start_node)

    def expand_and_evaluate_node(self, node: Node):
        node.level += 1
        remaining_events = set(self.events).difference(node.path)

        for remaining_event in remaining_events:
            self.iterate_remaining_event(node, remaining_event, remaining_events)

    def iterate_remaining_event(self, parent_node, remaining_event, remaining_events):
        node_to_iterate = Node(
            level=parent_node.level,
            capacity=parent_node.capacity,
            bound_without_returning=parent_node.bound_without_returning,
            path=parent_node.path[:]
        )

        is_added = node_to_iterate.add_event(remaining_event)
        if not is_added:
            return

        node_to_iterate.bound, node_to_iterate.bound_without_returning = self.bound(node_to_iterate)

        if self.is_node_reach_to_leaf_node(node_to_iterate):
            left_events = remaining_events - {remaining_event}
            if left_events:
                leaf_event = left_events.pop()
                is_added = node_to_iterate.add_event(leaf_event)
                if not is_added:
                    return

            self.check_and_set_optimum_route_if_route_is_optimum(node_to_iterate)

        else:
            self.compare_and_put_node_to_queue(node_to_iterate)

    def bound(self, node: Node):
        bound_without_returning = node.bound_without_returning + self.distance_matrix[node.path[-2].location_index][
            node.path[-1].location_index]
        bound = bound_without_returning + self.distance_matrix[node.path[-1].location_index][self.depot_to_return.location_index]
        return bound, bound_without_returning

    def compare_and_put_node_to_queue(self, node: Node):
        if node.bound < self.best_cost:
            self.priority_queue.put(node)

    def check_and_set_optimum_route_if_route_is_optimum(self, node: Node):
        node.bound, node.bound_without_returning = self.bound(node)
        route_distance = node.bound

        if route_distance < self.best_cost:
            self.best_cost = route_distance
            self.optimum_route = Route(events=node.path + [self.depot_to_return], total_cost=route_distance)

    def is_node_reach_to_leaf_node(self, node: Node):
        return node.level >= (self.deepest_level - 1)

    def handle_small_size_routes(self):
        if len(self.events) == 0:
            self.optimum_route = Route(events=[self.depot_to_delivery, self.depot_to_return], total_cost=0)
        elif len(self.events) == 1:
            self.optimum_route = Route(events=[self.depot_to_delivery, self.events[0], self.depot_to_return],
                                       total_cost=float(self.distance_matrix[0][1] + self.distance_matrix[1][0]))

    def create_depot_events(self):
        super().create_depot_events()

        total_delivery_capacity = sum([event.capacity for event in self.events if event.is_delivery])
        self.depot_to_delivery.capacity = total_delivery_capacity

        total_pickup_capacity = sum([event.capacity for event in self.events if event.is_pickup])
        self.depot_to_return.capacity = total_pickup_capacity

        self.check_capacity_constraints()

    def check_capacity_constraints(self):
        if self.depot_to_delivery.capacity > self.vehicle.capacity or self.depot_to_return.capacity > self.vehicle.capacity:
            raise ValueError("Delivery or Pickup capacity exceeds vehicle capacity. Solution is not possible.")
