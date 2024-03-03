from dataclasses import dataclass, field
from typing import List

import numpy as np

from src.constants.event import EventConstant
from src.models.depot import Depot
from src.models.event import Event
from src.models.route import Route
from src.models.vehicle import Vehicle
from abc import ABC, abstractmethod


@dataclass
class BaseSolver(ABC):
    """
    Base Solver for the Capacitated Traveling Salesman Problem.
    """
    depot: Depot
    events: List[Event]  # pickup and deliveries
    vehicle: Vehicle
    distance_matrix: np.ndarray

    depot_to_delivery: Event = field(init=False)
    depot_to_return: Event = field(init=False)

    def __post_init__(self):
        self.depot_to_delivery = Event(id=self.depot.location_index, location_index=self.depot.location_index, x=self.depot.x,
                                       y=self.depot.y, type=EventConstant.EventType.DEPOT_START)

        self.depot_to_return = Event(id=self.depot.location_index, location_index=self.depot.location_index, x=self.depot.x, y=self.depot.y,
                                     type=EventConstant.EventType.DEPOT_END)

    @abstractmethod
    def solve(self) -> Route:
        ...
