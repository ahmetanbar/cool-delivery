from dataclasses import dataclass
from typing import List

from scipy.spatial.distance import cdist
import numpy as np

from src.models.event import Event


@dataclass
class DistanceMatrixGenerator:

    @staticmethod
    def generate_distance_matrix(events: List[Event]) -> np.ndarray:
        coordinates = np.array([[event.x, event.y] for event in events])
        distance_matrix = cdist(coordinates, coordinates, 'euclidean')
        return distance_matrix
