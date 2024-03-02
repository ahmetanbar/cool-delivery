import time
import cProfile

from src.solvers.tsp import TSPSolver
from src.utils.data_generator import DataGenerator
from src.utils.distance_matrix_generator import DistanceMatrixGenerator


def main():
    depot, deliveries, pickups, vehicle = DataGenerator(pickup_count=1, delivery_count=8, generate_random_data=False).generate_tsp_instance()
    events = deliveries + pickups

    distance_matrix = DistanceMatrixGenerator.generate_distance_matrix([depot] + events)

    start_time = time.time()
    profiler = cProfile.Profile()
    profiler.enable()
    for i in range(1000):
        solver = TSPSolver(depot=depot, events=events, vehicle=vehicle, distance_matrix=distance_matrix)
        optimal_route = solver.solve()

    profiler.disable()

    # Print the total time
    profiler.print_stats(sort='cumulative')

    elapsed_time = time.time() - start_time
    # solution = cProfile.runctx('solver.solve()', globals(), locals(), sort='cumulative')

    print(elapsed_time)

    # print(optimal_route)


if __name__ == '__main__':
    main()
