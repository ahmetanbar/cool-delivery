from dataclasses import dataclass, asdict
import random
from typing import List, Tuple
import json

from scipy.spatial.distance import cdist
import numpy as np

from src.constants.event import EventConstant
from src.models.depot import Depot
from src.models.event import Event
from src.models.vehicle import Vehicle


@dataclass
class DataSample:
    x: int
    y: int
    capacity: int


@dataclass
class DataGenerator:
    """
    Generates a random instance of the Capacitated Traveling Salesman Problem.
    """

    MIN_COORDINATE, MAX_COORDINATE = 0, 100
    MIN_CAPACITY, MAX_CAPACITY = 10, 50

    depot_x: int = 0
    depot_y: int = 0
    pickup_count: int = 10
    delivery_count: int = 10
    output_file: str = "../data/inputs/input.json"

    def generate(self):
        pickup_data = self.generate_samples(self.pickup_count)
        delivery_data = self.generate_samples(self.delivery_count)

        depot, events = self.build_events_and_depot(pickup_data, delivery_data)

        deliveries_capacity = sum([event.capacity for event in events if event.is_delivery])
        pickups_capacity = sum([event.capacity for event in events if event.is_pickup])
        vehicle = self.build_vehicle_instance(deliveries_capacity, pickups_capacity)

        distance_matrix = self.generate_distance_matrix(depot, events)

        self.save_to_file(depot, vehicle, events, distance_matrix)

    def build_vehicle_instance(self, deliveries_capacity: int, pickups_capacity: int) -> Vehicle:
        vehicle_capacity = max(deliveries_capacity, pickups_capacity)
        vehicle = Vehicle(capacity=vehicle_capacity)
        return vehicle

    def generate_random_coordinates(self, num_coordinates):
        coordinates = []
        for _ in range(num_coordinates):
            x = random.randint(self.MIN_COORDINATE, self.MAX_COORDINATE)
            y = random.randint(self.MIN_COORDINATE, self.MAX_COORDINATE)
            coordinates.append((x, y))
        return coordinates

    def generate_random_capacities(self, num_capacities):
        capacities = []
        for _ in range(num_capacities):
            capacity = random.randint(self.MIN_CAPACITY, self.MAX_CAPACITY)
            capacities.append(capacity)
        return capacities

    def generate_samples(self, count: int) -> List[DataSample]:
        coordinates = self.generate_random_coordinates(count)
        capacities = self.generate_random_capacities(count)
        return [DataSample(x=x, y=y, capacity=capacity) for (x, y), capacity in zip(coordinates, capacities)]

    def build_events_and_depot(self, pickup_data: List[DataSample], delivery_data: List[DataSample]) -> Tuple[Depot, List[Event]]:
        index_counter = 0

        depot = Depot(x=self.depot_x, y=self.depot_y, location_index=index_counter)
        index_counter += 1

        deliveries = [Event(id=i, location_index=i, x=sample.x, y=sample.y, capacity=sample.capacity, type=EventConstant.EventType.DELIVERY)
                      for i, sample in enumerate(delivery_data, start=index_counter)]
        index_counter += len(delivery_data)

        pickups = [Event(id=i, location_index=i, x=sample.x, y=sample.y, capacity=sample.capacity, type=EventConstant.EventType.PICKUP)
                   for i, sample in enumerate(pickup_data, start=index_counter)]

        events = deliveries + pickups
        return depot, events

    @staticmethod
    def generate_distance_matrix(depot: Depot, events: List[Event]) -> np.ndarray:
        coordinates = np.array([[depot.x, depot.y]] + [[event.x, event.y] for event in events])
        distance_matrix = cdist(coordinates, coordinates, 'euclidean')
        distance_matrix = distance_matrix.astype(int)
        return distance_matrix

    def save_to_file(self, depot: Depot, vehicle: Vehicle, events, distance_matrix):
        data = {
            "depot": asdict(depot),
            "vehicle": asdict(vehicle),
            "events": [asdict(event) for event in events],
            "distance_matrix": distance_matrix.tolist()
        }
        with open(self.output_file, 'w') as file:
            json.dump(data, file, indent=2)
