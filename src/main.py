import matplotlib.pyplot as plt
import typer
from loguru import logger

from src.constants.solver import SolverConstant
from src.data_helper.data_generator import DataGenerator
from src.data_helper.instance_generator import InstanceGenerator
from src.data_helper.output_helper import OutputHelper

app = typer.Typer()

OUTPUT_FOLDER = "src/data/outputs/"
INPUT_FOLDER = "src/data/inputs/"


def visualize_coordinates(events):
    coordinates = [(event.x, event.y) for event in events]
    x, y = zip(*coordinates)

    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, color='red', marker='o')

    for i in range(len(events)):
        plt.annotate(f"{events[i].id}", (x[i], y[i]), textcoords="offset points", xytext=(0, 5), ha='center')

    for i in range(len(events) - 1):
        plt.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color='blue', linestyle='-', linewidth=2)

    plt.title('TSP Coordinate Visualization')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()


def get_data_from_file(file_path):
    depot, vehicle, events, distance_matrix = InstanceGenerator(file_path).generate()
    return depot, vehicle, events, distance_matrix


@app.command()
def solve(solver: SolverConstant.Name, input_file: str, output_file: str, visualize: bool = False):
    input_file = INPUT_FOLDER + input_file
    output_file = OUTPUT_FOLDER + output_file

    solver_class = SolverConstant.STR_TO_CLASS.get(solver)

    depot, vehicle, events, distance_matrix = get_data_from_file(input_file)

    solver_instance = solver_class(depot=depot, events=events, vehicle=vehicle, distance_matrix=distance_matrix)
    optimal_route = solver_instance.solve()

    OutputHelper.save_to_file(route=optimal_route, output_file=output_file, solver=solver)

    logger.debug(optimal_route)

    if visualize:
        visualize_coordinates(optimal_route.events)


@app.command()
def generate(pickup_count: int, delivery_count: int, depot_x: int = 0, depot_y: int = 0, output_file="input.json"):
    output_file = "src/data/inputs/" + output_file
    DataGenerator(pickup_count=pickup_count, delivery_count=delivery_count, depot_x=depot_x, depot_y=depot_y,
                  output_file=output_file).generate()
    logger.debug(f"Data is generated and saved to {output_file}")


if __name__ == '__main__':
    app()
