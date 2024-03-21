import itertools
from typing import List
from queue import PriorityQueue

from loguru import logger

from cool_delivery.models import Event, Route
from cool_delivery.solvers import BaseSolver, CTSPWithNearestNeighborSolver, CTSPWithBranchAndBoundSolver


class Solver(BaseSolver):
    """
    Capacitated Traveling Salesman Problem with Maximum Delivery and Single Pickup solver.
    The algorithm is used to find the optimal route for the vehicle to visit maximum delivery events and a single pickup event.
    The route is a path that starts and ends at the depot.

    First priority is to find the delivery groups with maximum size with a single pickup event. Secondly, it tries to optimize the route.

    It first finds the delivery group combinations with maximum size.
    Then, it tries to find the optimal route for each delivery group with the nearest neighbor algorithm.

    If the event count is less than or equal to the maximum event size to find the global optimum,
    it tries to find the global optimum by using the branch and bound algorithm.
    """
    MAXIMUM_EVENT_SIZE_TO_FIND_GLOBAL_OPTIMUM = 10
    MAXIMUM_TRY_COUNT_WITH_NEAREST_NEIGHBOR_SOLUTIONS = 10

    def solve(self):
        logger.debug("Solving with Maximum Delivery and Single Pickup problem.")

        pickups = self.get_pickups()
        deliveries = self.get_deliveries()

        delivery_groups = self.find_delivery_groups_with_maximum_size(deliveries)
        max_delivery_group_size = len(delivery_groups[0]) if delivery_groups else 0
        logger.debug(f'Count of combinations of delivery groups with maximum size: {len(delivery_groups)}.')
        logger.debug(f'Max delivery group size: {max_delivery_group_size}.')

        delivery_groups_with_single_pickup = self.combine_delivery_groups_with_single_pickup(delivery_groups, pickups)

        nearest_solutions_in_queue = self.get_nearest_neighbor_solutions_in_queue(delivery_groups_with_single_pickup)

        can_find_global_optimum = self.can_find_global_optimum(max_delivery_group_size + 1)

        best_route = Route(events=[], total_cost=float('inf'))
        if can_find_global_optimum:
            self.find_best_solution_with_branch_and_bound(best_route, nearest_solutions_in_queue)
        else:
            best_route = nearest_solutions_in_queue.get()

        self.optimum_route = best_route
        logger.debug(best_route)

    def find_best_solution_with_branch_and_bound(self, best_route: Route, priority_queue: PriorityQueue):
        """Finds best solution with branch and bound algorithm.
        It uses first self.MAXIMUM_TRY_COUNT_WITH_NEAREST_NEIGHBOR_SOLUTIONS solutions from the priority queue.
        It solves the TSP for each solution with the branch and bound algorithm. According to solutions, it updates best route.
        """
        try_count = 0
        while not priority_queue.empty() and try_count < self.MAXIMUM_TRY_COUNT_WITH_NEAREST_NEIGHBOR_SOLUTIONS:
            try_count += 1

            route_to_find_global_optimum: Route = priority_queue.get()

            if route_to_find_global_optimum < best_route:
                best_route.total_cost = route_to_find_global_optimum.total_cost
                best_route.events = route_to_find_global_optimum.events

            events = [event for event in route_to_find_global_optimum.events if not (event.is_depot_start or event.is_depot_end)]

            solver = CTSPWithBranchAndBoundSolver(depot=self.depot, events=events,
                                                  vehicle=self.vehicle, distance_matrix=self.distance_matrix,
                                                  best_cost=best_route.total_cost)
            solver.solve()
            route = solver.get_solution(as_object=True)

            if route < best_route:
                best_route.total_cost = route.total_cost
                best_route.events = route.events

    def combine_delivery_groups_with_single_pickup(self, delivery_groups: List[List[Event]], pickups: List[Event]) -> List[List[Event]]:
        delivery_groups_with_single_pickup = []
        for delivery_group in delivery_groups:
            if not pickups:
                delivery_groups_with_single_pickup.append(delivery_group)
                continue
            for pickup in pickups:
                delivery_groups_with_single_pickup.append(delivery_group + [pickup])

        return delivery_groups_with_single_pickup

    def get_nearest_neighbor_solutions_in_queue(self, delivery_groups_with_single_pickup: List[List[Event]]) -> PriorityQueue:
        priority_queue = PriorityQueue()
        for deliveries_with_single_pickup in delivery_groups_with_single_pickup:
            route = self.get_solution_by_nearest_neighbor_solution(deliveries_with_single_pickup)
            priority_queue.put(route)
        return priority_queue

    def get_solution_by_nearest_neighbor_solution(self, events):
        solver = CTSPWithNearestNeighborSolver(depot=self.depot, events=events, vehicle=self.vehicle,
                                               distance_matrix=self.distance_matrix)
        solver.solve()
        route = solver.get_solution(as_object=True)
        return route

    def get_deliveries(self) -> List[Event]:
        return [event for event in self.events if event.is_delivery]

    def get_pickups(self) -> List[Event]:
        return [event for event in self.events if event.is_pickup]

    def find_delivery_groups_with_maximum_size(self, deliveries: List[Event]) -> List[List[Event]]:
        delivery_group = self.find_delivery_group_with_maximum_size(deliveries)

        return [delivery_group]

    def find_delivery_group_with_maximum_size(self, deliveries):
        deliveries.sort(key=lambda x: x.capacity)

        delivery_group = []
        remaining_capacity = self.vehicle.capacity

        for delivery in deliveries:
            if delivery.capacity <= remaining_capacity:
                delivery_group.append(delivery)
                remaining_capacity -= delivery.capacity
            else:
                break

        return delivery_group

    @classmethod
    def can_find_global_optimum(cls, event_count: int) -> bool:
        return event_count <= cls.MAXIMUM_EVENT_SIZE_TO_FIND_GLOBAL_OPTIMUM
