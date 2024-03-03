import json
from dataclasses import dataclass
from typing import List

import numpy as np

from src.models.depot import Depot
from src.models.event import Event
from src.models.vehicle import Vehicle


@dataclass
class Data:
    depot: Depot
    vehicle: Vehicle
    events: List[Event]
    distance_matrix: np.array


@dataclass
class InstanceGenerator:
    input_file: str

    def generate(self) -> (Depot, Vehicle, List[Event], np.array):
        json_data = self.read_from_file()

        depot, vehicle, events, distance_matrix = self.parse_json(json_data)

        return depot, vehicle, events, distance_matrix

    def read_from_file(self):
        file_name = self.input_file
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data

    def parse_json(self, json_data) -> (Depot, Vehicle, List[Event], np.array):
        data = Data(**json_data)

        depot = Depot(**json_data['depot'])
        vehicle = Vehicle(**json_data['vehicle'])
        events = [Event(**event) for event in json_data['events']]
        distance_matrix = np.array(json_data['distance_matrix'])

        return depot, vehicle, events, distance_matrix
