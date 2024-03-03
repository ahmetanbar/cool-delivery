import itertools
from dataclasses import dataclass
from typing import List
from queue import PriorityQueue

from src.models.event import Event
from src.models.route import Route
from src.solvers.BaseSolver.solver import BaseSolver
from src.solvers.CTSPWithNearestNeighbor.solver import Solver as TSPWithNearestNeighborSolver
from src.solvers.CTSPWithBranchAndBound.solver import Solver as TSPWithBranchAndBoundSolver


@dataclass
class Solver(BaseSolver):
    """
    Solver for the Capacitated Traveling Salesman Problem with Maximum Delivery and Single Pickup.
    """
    MAXIMUM_EVENT_SIZE_TO_FIND_GLOBAL_OPTIMUM = 9
    MAXIMUM_TRY_COUNT_WITH_NEAREST_NEIGHBOR_SOLUTIONS = 10

    def solve(self):
        pickups = self.get_pickups()
        deliveries = self.get_deliveries()

        delivery_groups = self.find_delivery_groups_with_maximum_size(deliveries)
        max_delivery_group_size = len(delivery_groups[0]) if delivery_groups else 0
        print(f'Count of combinations of delivery groups with maximum size: {len(delivery_groups)}.')
        print(f'Max delivery group size: {max_delivery_group_size}.')

        priority_queue = PriorityQueue()
        for delivery_group in delivery_groups:
            for pickup in pickups:
                events = list(delivery_group) + [pickup]

                route: Route = TSPWithNearestNeighborSolver(depot=self.depot, events=events, vehicle=self.vehicle,
                                                            distance_matrix=self.distance_matrix).solve()

                priority_queue.put(route)

        can_find_global_optimum = self.can_find_global_optimum(max_delivery_group_size + 1)

        best_route = Route(events=[], total_cost=float('inf'))
        if can_find_global_optimum:

            try_count = 0
            while not priority_queue.empty() and try_count < self.MAXIMUM_TRY_COUNT_WITH_NEAREST_NEIGHBOR_SOLUTIONS:
                try_count += 1

                route_to_find_global_optimum: Route = priority_queue.get()

                if route_to_find_global_optimum < best_route:
                    best_route.total_cost = route_to_find_global_optimum.total_cost
                    best_route.events = route_to_find_global_optimum.events

                events = [event for event in route_to_find_global_optimum.events if not event.is_depot]
                route = TSPWithBranchAndBoundSolver(depot=self.depot, events=events,
                                                    vehicle=self.vehicle, distance_matrix=self.distance_matrix,
                                                    best_cost=best_route.total_cost
                                                    ).solve()
                if route < best_route:
                    best_route.total_cost = route_to_find_global_optimum.total_cost
                    best_route.events = route_to_find_global_optimum.events

        else:
            best_route = priority_queue.get()

        print(best_route)
        return best_route

    def get_deliveries(self) -> List[Event]:
        return [event for event in self.events if event.is_delivery]

    def get_pickups(self) -> List[Event]:
        return [event for event in self.events if event.is_pickup]

    def find_delivery_groups_with_maximum_size(self, deliveries: List[Event]) -> List[List[Event]]:
        max_groups = []
        max_count = 0

        for r in range(len(deliveries), 0, -1):  # Start from larger combinations
            delivery_combinations = itertools.combinations(deliveries, r)

            for group in delivery_combinations:
                group_capacity = sum([d.capacity for d in group])

                if group_capacity <= self.vehicle.capacity and len(group) >= max_count:
                    if len(group) > max_count:
                        max_groups = [group]
                        max_count = len(group)
                    else:
                        max_groups.append(group)

            if r <= max_count:
                break
        return max_groups

    @classmethod
    def can_find_global_optimum(cls, event_count: int) -> bool:
        return event_count <= cls.MAXIMUM_EVENT_SIZE_TO_FIND_GLOBAL_OPTIMUM
