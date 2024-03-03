from dataclasses import dataclass, field
import random
from typing import List, Dict, Tuple

from src.models.delivery import Delivery
from src.models.depot import Depot
from src.models.pickup import Pickup
from src.models.vehicle import Vehicle
from src.data.homberger_c1_2_1 import data as data_instance


@dataclass
class DataSample:
    x: int
    y: int
    capacity: int


@dataclass
class EventsGenerator:
    depot_x: int = 0
    depot_y: int = 0
    pickup_count: int = 10
    delivery_count: int = 10
    generate_random_data: bool = False

    data_source: Dict = field(init=False)
    coordinates_and_capacity_data: List[List[int]] = field(init=False)
    vehicle_capacity_data: int = field(init=False)

    def __post_init__(self):
        self.data_source = data_instance
        self.coordinates_and_capacity_data = self.data_source.get("coordinates_and_capacity", [])
        self.vehicle_capacity_data = self.data_source.get("vehicle_capacity", 0)

        if len(self.coordinates_and_capacity_data) < self.pickup_count + self.delivery_count:
            raise ValueError("Not enough data to generate the requested number of pickup and delivery events")

    def generate_tsp_instance(self) -> Tuple[Depot, List[Delivery], List[Pickup], Vehicle]:
        pickup_data = self.get_samples_from_data_instance(self.pickup_count)
        delivery_data = self.get_samples_from_data_instance(self.delivery_count)

        depot, deliveries, pickups = self.build_pickup_delivery_and_depot_instances(pickup_data, delivery_data)

        deliveries_capacity = sum([delivery.capacity for delivery in deliveries])
        pickups_capacity = sum([pickup.capacity for pickup in pickups])
        vehicle = self.build_vehicle_instance(deliveries_capacity, pickups_capacity)

        return depot, deliveries, pickups, vehicle

    def build_vehicle_instance(self, deliveries_capacity: int, pickups_capacity: int) -> Vehicle:
        vehicle_capacity = max(deliveries_capacity, self.vehicle_capacity_data, pickups_capacity)
        vehicle = Vehicle(capacity=vehicle_capacity)
        return vehicle

    def get_samples_from_data_instance(self, count: int) -> List[DataSample]:
        if self.generate_random_data:
            samples = random.sample(self.coordinates_and_capacity_data, count)
        else:
            samples = self.coordinates_and_capacity_data[:count]
            self.coordinates_and_capacity_data = self.coordinates_and_capacity_data[count:]

        return [DataSample(x=x, y=y, capacity=capacity) for x, y, capacity in samples]

    def build_pickup_delivery_and_depot_instances(self, pickup_data: List[DataSample],
                                                  delivery_data: List[DataSample]) -> Tuple[Depot, List[Delivery], List[Pickup]]:
        index_counter = 0

        depot = Depot(id=0, x=self.depot_x, y=self.depot_y)
        index_counter += 1

        deliveries = [Delivery(id=i, x=sample.x, y=sample.y, capacity=sample.capacity) for i, sample in
                      enumerate(delivery_data, start=index_counter)]
        index_counter += len(delivery_data)

        pickups = [Pickup(id=i, x=sample.x, y=sample.y, capacity=sample.capacity) for i, sample in
                   enumerate(pickup_data, start=index_counter)]

        return depot, deliveries, pickups
