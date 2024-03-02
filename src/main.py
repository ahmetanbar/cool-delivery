import time
import cProfile

import matplotlib.pyplot as plt

from src.solvers.TSPWithBranchAndBound.solver import Solver as TSPSolver
from src.solvers.TSPWithNearestNeighbor.solver import Solver as TSPWithNearestNeighborSolver
from src.utils.data_generator import DataGenerator
from src.utils.distance_matrix_generator import DistanceMatrixGenerator


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


def main():
    depot, deliveries, pickups, vehicle = DataGenerator(pickup_count=3, delivery_count=8,
                                                        generate_random_data=False).generate_tsp_instance()
    events = deliveries + pickups

    distance_matrix = DistanceMatrixGenerator.generate_distance_matrix([depot] + events)

    start_time = time.time()
    profiler = cProfile.Profile()
    profiler.enable()

    solver = TSPWithNearestNeighborSolver(depot=depot, events=events, vehicle=vehicle, distance_matrix=distance_matrix)
    optimal_route = solver.solve()

    profiler.disable()

    profiler.print_stats(sort='cumulative')

    elapsed_time = time.time() - start_time

    visualize_coordinates(optimal_route.events)

    print(elapsed_time)

    # print(optimal_route)


if __name__ == '__main__':
    main()
