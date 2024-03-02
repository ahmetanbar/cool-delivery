from dataclasses import dataclass
from typing import List

import numpy as np

from src.models.depot import Depot
from src.models.event import Event
from src.models.vehicle import Vehicle


@dataclass
class Solver:
    """
    Solver for the Capacitated Traveling Salesman Problem with Maximum Delivery and Single Pickup.
    """
    depot: Depot
    events: List[Event]  # pickup and deliveries
    vehicle: Vehicle
    distance_matrix: np.ndarray
