import time
import cProfile

from src.solvers.TSPWithBranchAndBound.solver import Solver as TSPSolver
from src.utils.data_generator import DataGenerator
from src.utils.distance_matrix_generator import DistanceMatrixGenerator


def main():
    depot, deliveries, pickups, vehicle = DataGenerator(pickup_count=3, delivery_count=8,
                                                        generate_random_data=False).generate_tsp_instance()
    events = deliveries + pickups

    distance_matrix = DistanceMatrixGenerator.generate_distance_matrix([depot] + events)

    start_time = time.time()
    profiler = cProfile.Profile()
    profiler.enable()

    solver = TSPSolver(depot=depot, events=events, vehicle=vehicle, distance_matrix=distance_matrix)
    optimal_route = solver.solve()

    profiler.disable()

    profiler.print_stats(sort='cumulative')

    elapsed_time = time.time() - start_time

    print(elapsed_time)

    # print(optimal_route)


if __name__ == '__main__':
    main()
