from dataclasses import dataclass, field
from typing import List

import numpy as np

from src.models.delivery import Delivery
from src.models.depot import Depot
from src.models.event import Event
from src.models.pickup import Pickup
from src.models.route import Route
from src.models.vehicle import Vehicle
from abc import ABC, abstractmethod


@dataclass
class BaseSolver(ABC):
    """
    Base Solver for the Traveling Salesman Problem.
    """
    depot: Depot
    events: List[Event]  # pickup and deliveries
    vehicle: Vehicle
    distance_matrix: np.ndarray

    depot_to_delivery: Depot = field(init=False)
    depot_to_return: Depot = field(init=False)

    def __post_init__(self):
        # Initialize depot events.
        self.initialize_depot_events()

    def initialize_depot_events(self):
        total_delivery_capacity = sum([event.capacity for event in self.events if isinstance(event, Delivery)])
        self.depot_to_delivery = Depot(id=self.depot.id, x=self.depot.x, y=self.depot.y, capacity=total_delivery_capacity)

        total_pickup_capacity = sum([event.capacity for event in self.events if isinstance(event, Pickup)])
        self.depot_to_return = Depot(id=self.depot.id, x=self.depot.x, y=self.depot.y, capacity=total_pickup_capacity, is_return=True)

        if self.depot_to_delivery.capacity > self.vehicle.capacity or self.depot_to_return.capacity > self.vehicle.capacity:
            raise ValueError("Delivery capacity exceeds vehicle capacity.")

    @abstractmethod
    def solve(self) -> Route:
        ...
