from dataclasses import asdict
import json

from cool_delivery.models.route import Route


class OutputHelper:
    @staticmethod
    def save_to_file(route: Route, output_file: str, solver: str):
        data = {
            "solver": solver,
            "location_indexes": [event.location_index for event in route.events],
            "cost": int(route.total_cost),
            "events": [asdict(event) for event in route.events],
        }

        with open(output_file, 'w') as file:
            json.dump(data, file, indent=2)
