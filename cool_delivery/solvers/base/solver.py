from dataclasses import dataclass, field, asdict
from typing import List, Dict, Union

import numpy as np

from cool_delivery.constants.event import EventConstant
from cool_delivery.models import Depot, Event, Vehicle, Route
from abc import ABC, abstractmethod


@dataclass
class BaseSolver(ABC):
    """
    Base Solver for the Capacitated Traveling Salesman Problem.
    """
    depot: Depot = None
    events: List[Event] = None  # pickup and deliveries
    vehicle: Vehicle = None
    distance_matrix: np.ndarray = None

    optimum_route: Route = field(default_factory=Route)
    depot_to_delivery: Event = None
    depot_to_return: Event = None

    def __post_init__(self):
        if self.depot and self.events:
            self.create_depot_events()

    @abstractmethod
    def solve(self):  # pragma: no cover
        ...

    def load_data(self, input_dict: Dict):
        self.depot = Depot(**input_dict['depot'])
        self.vehicle = Vehicle(**input_dict['vehicle'])
        self.events = [Event(**event) for event in input_dict['events']]
        self.distance_matrix = np.array(input_dict['distance_matrix'])

        self.create_depot_events()

    def create_depot_events(self):
        self.depot_to_delivery = Event(id=self.depot.location_index, location_index=self.depot.location_index, x=self.depot.x,
                                       y=self.depot.y, type=EventConstant.EventType.DEPOT_START)

        self.depot_to_return = Event(id=self.depot.location_index, location_index=self.depot.location_index, x=self.depot.x, y=self.depot.y,
                                     type=EventConstant.EventType.DEPOT_END)

    def get_solution(self, as_object: bool = False) -> Union[Route, Dict]:
        if as_object:
            return self.optimum_route
        solution = {
            "cost": int(self.optimum_route.total_cost),
            "events": [asdict(event) for event in self.optimum_route.events],
        }
        return solution
