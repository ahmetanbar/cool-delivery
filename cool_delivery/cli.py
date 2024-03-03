import typer
from loguru import logger

from cool_delivery.constants.solver import SolverConstant
from cool_delivery.data_helper import DataGenerator, InstanceGenerator, OutputHelper, Visualizer


app = typer.Typer()

OUTPUT_FOLDER = "cool_delivery/data/outputs/"
INPUT_FOLDER = "cool_delivery/data/inputs/"


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
        Visualizer.visualize_coordinates(optimal_route.events)


@app.command()
def generate(pickup_count: int, delivery_count: int, depot_x: int = 0, depot_y: int = 0, output_file="input.json"):
    output_file = INPUT_FOLDER + output_file
    DataGenerator(pickup_count=pickup_count, delivery_count=delivery_count, depot_x=depot_x, depot_y=depot_y,
                  output_file=output_file).generate()
    logger.debug(f"Data is generated and saved to {output_file}")


if __name__ == '__main__':
    app()
