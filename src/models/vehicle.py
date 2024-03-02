from dataclasses import dataclass


@dataclass
class Vehicle:
    capacity: int = 0
    current_load: int = 0
