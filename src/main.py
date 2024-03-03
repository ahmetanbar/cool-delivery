import time
import cProfile

import matplotlib.pyplot as plt
from loguru import logger

from src.solvers.CTSPWithBranchAndBound.solver import Solver as TSPSolver
from src.solvers.CTSPWithNearestNeighbor.solver import Solver as TSPWithNearestNeighborSolver
from src.solvers.CTSPWithMaximumDeliveryAndSinglePickup.solver import Solver as CTSPSolver
from src.data_generators.events_generator import EventsGenerator
from src.data_generators.distance_matrix_generator import DistanceMatrixGenerator


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


def wrapper_to_profile(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()

        # profiler = cProfile.Profile()
        # profiler.enable()

        result = func(*args, **kwargs)

        # profiler.disable()
        # profiler.print_stats(sort='cumulative')

        elapsed_time = time.time() - start_time
        logger.debug(f"Elapsed time: {elapsed_time}")
        return result

    return wrapper


def main():
    depot, deliveries, pickups, vehicle = EventsGenerator(pickup_count=10, delivery_count=10,
                                                          generate_random_data=False).generate_tsp_instance()
    vehicle.capacity = 150
    events = deliveries + pickups

    distance_matrix = DistanceMatrixGenerator.generate_distance_matrix([depot] + events)

    start_time = time.time()

    solver = CTSPSolver(depot=depot, events=events, vehicle=vehicle, distance_matrix=distance_matrix)
    optimal_route = solver.solve()

    logger.debug(optimal_route)

    elapsed_time = time.time() - start_time

    visualize_coordinates(optimal_route.events)

    logger.debug(f"Elapsed time: {elapsed_time}")


if __name__ == '__main__':
    main()
