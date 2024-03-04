from .mock_data import Data
import pytest

from cool_delivery.solvers import CTSPWithBranchAndBoundSolver


def test_solve(ctsp_with_branch_and_bound_solver):
    ctsp_with_branch_and_bound_solver.solve()
    solution = ctsp_with_branch_and_bound_solver.get_solution(as_object=True)
    assert len(solution.events)
    assert solution.total_cost == 23  # 5 + 8 + 5 = 23


def test_solve_big_size_all_delivery():
    solver = CTSPWithBranchAndBoundSolver()
    solver.load_data(Data.input_with_5_delivery_5_pickup)
    solver.solve()
    solution = solver.get_solution()
    assert len(solution["events"]) == len(Data.output_with_5_delivery_5_pickup["events"])
    assert [event["location_index"] for event in solution["events"]] == [event["location_index"] for event in
                                                                         Data.output_with_5_delivery_5_pickup["events"]]
    assert solution["cost"] == Data.output_with_5_delivery_5_pickup["cost"]


def test_start_to_queue(ctsp_with_branch_and_bound_solver):
    ctsp_with_branch_and_bound_solver.create_depot_events()
    ctsp_with_branch_and_bound_solver.start_to_queue()

    assert ctsp_with_branch_and_bound_solver.priority_queue.qsize() == 1
    node = ctsp_with_branch_and_bound_solver.priority_queue.get()
    assert node.path == [ctsp_with_branch_and_bound_solver.depot_to_delivery]
    assert node.capacity == 80  # 100 - 20


def test_bound(ctsp_with_branch_and_bound_solver, node):
    node.bound_without_returning = 5
    bound, bound_without_returning = ctsp_with_branch_and_bound_solver.bound(node)

    assert bound == 23  # 5 + 8
    assert bound_without_returning == 13  # 5 + 8


def test_compare_and_put_node_to_queue(ctsp_with_branch_and_bound_solver, node):
    ctsp_with_branch_and_bound_solver.best_cost = 20
    node.bound_without_returning = 5
    ctsp_with_branch_and_bound_solver.compare_and_put_node_to_queue(node)
    assert ctsp_with_branch_and_bound_solver.priority_queue.qsize() == 1

    node.bound_without_returning = 25
    ctsp_with_branch_and_bound_solver.compare_and_put_node_to_queue(node)
    assert ctsp_with_branch_and_bound_solver.priority_queue.qsize() == 2


def test_check_and_set_optimum_route_if_route_is_optimum(ctsp_with_branch_and_bound_solver, node):
    node.path = node.path[:-1]

    ctsp_with_branch_and_bound_solver.best_cost = 20
    node.bound_without_returning = 5
    ctsp_with_branch_and_bound_solver.check_and_set_optimum_route_if_route_is_optimum(node)
    assert ctsp_with_branch_and_bound_solver.optimum_route.total_cost == 10
    assert ctsp_with_branch_and_bound_solver.optimum_route.events == node.path + [ctsp_with_branch_and_bound_solver.depot_to_return]
    assert ctsp_with_branch_and_bound_solver.best_cost == 10

    ctsp_with_branch_and_bound_solver.optimum_route.total_cost = 10
    node.total_cost = 20
    ctsp_with_branch_and_bound_solver.check_and_set_optimum_route_if_route_is_optimum(node)
    assert ctsp_with_branch_and_bound_solver.optimum_route.total_cost == 10


def test_is_node_reach_to_leaf_node(ctsp_with_branch_and_bound_solver, node):
    ctsp_with_branch_and_bound_solver.deepest_level = 3
    node.level = 2

    assert ctsp_with_branch_and_bound_solver.is_node_reach_to_leaf_node(node)

    node.level = 3
    assert ctsp_with_branch_and_bound_solver.is_node_reach_to_leaf_node(node)


def test_handle_small_size_routes(ctsp_with_branch_and_bound_solver, delivery_event):
    ctsp_with_branch_and_bound_solver.events = []
    ctsp_with_branch_and_bound_solver.handle_small_size_routes()
    assert ctsp_with_branch_and_bound_solver.optimum_route.events == [ctsp_with_branch_and_bound_solver.depot_to_delivery,
                                                                      ctsp_with_branch_and_bound_solver.depot_to_return]
    assert ctsp_with_branch_and_bound_solver.optimum_route.total_cost == 0

    ctsp_with_branch_and_bound_solver.events = [delivery_event]
    ctsp_with_branch_and_bound_solver.handle_small_size_routes()
    assert ctsp_with_branch_and_bound_solver.optimum_route.events == [ctsp_with_branch_and_bound_solver.depot_to_delivery,
                                                                      delivery_event,
                                                                      ctsp_with_branch_and_bound_solver.depot_to_return]
    assert ctsp_with_branch_and_bound_solver.optimum_route.total_cost == 10


def test_create_depot_events(ctsp_with_branch_and_bound_solver, pickup_event, delivery_event):
    pickup_event.capacity = 10
    delivery_event.capacity = 40

    ctsp_with_branch_and_bound_solver.events = [pickup_event, delivery_event]
    ctsp_with_branch_and_bound_solver.vehicle.capacity = 51

    ctsp_with_branch_and_bound_solver.create_depot_events()
    assert ctsp_with_branch_and_bound_solver.depot_to_return.capacity == 10
    assert ctsp_with_branch_and_bound_solver.depot_to_delivery.capacity == 40

    pickup_event.capacity = 20
    delivery_event.capacity = 10

    ctsp_with_branch_and_bound_solver.events = [pickup_event, delivery_event]
    ctsp_with_branch_and_bound_solver.vehicle.capacity = 11

    with pytest.raises(ValueError):
        ctsp_with_branch_and_bound_solver.create_depot_events()
