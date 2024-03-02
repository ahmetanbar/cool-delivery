from dataclasses import dataclass

from src.models.event import Event


@dataclass
class Pickup(Event):
    def __hash__(self):
        # Add the hash for the Pickup class
        return hash((type(self), self.id))

    def __eq__(self, other):
        # Add the equality comparison for the Pickup class
        if isinstance(other, Pickup):
            return (type(self), self.id) == (type(other), other.id)
        return False