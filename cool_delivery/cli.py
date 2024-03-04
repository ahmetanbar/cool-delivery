import json
from typing import Dict

import typer
from loguru import logger

from cool_delivery.constants.solver import SolverConstant
from cool_delivery.data_helper import DataGenerator, Visualizer

app = typer.Typer()


def read_from_file(input_file: str):
    with open(input_file, 'r') as file:
        data = json.load(file)
    return data


def save_to_file(route: Dict, output_file: str, solver: str):
    data = route
    data["solver"] = solver
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=2)


@app.command()
def solve(solver: SolverConstant.Name, input_file: str, output_file: str, visualize: bool = False):
    solver_class = SolverConstant.STR_TO_CLASS.get(solver)

    input_dict = read_from_file(input_file)

    solver_instance = solver_class()
    solver_instance.load_data(input_dict)
    solver_instance.solve()
    optimum_route = solver_instance.get_solution()

    save_to_file(route=optimum_route, output_file=output_file, solver=solver)

    logger.debug(optimum_route)

    optimum_route = solver_instance.get_solution(as_object=True)
    if visualize:
        Visualizer.visualize_coordinates(optimum_route.events)


@app.command()
def generate(pickup_count: int, delivery_count: int, depot_x: int = 0, depot_y: int = 0, output_file="input.json"):
    DataGenerator(pickup_count=pickup_count, delivery_count=delivery_count, depot_x=depot_x, depot_y=depot_y,
                  output_file=output_file).generate()
    logger.debug(f"Data is generated and saved to {output_file}")


if __name__ == '__main__':
    app()
