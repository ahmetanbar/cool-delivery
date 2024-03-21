from copy import deepcopy
from cool_delivery.solvers import CTSPWithMaximumDeliveryAndSinglePickupSolver
from .mock_data import Data


def test_solve(ctsp_maximum_delivery_and_single_pickup):
    ctsp_maximum_delivery_and_single_pickup.solve()
    solution = ctsp_maximum_delivery_and_single_pickup.get_solution(as_object=True)
    assert len(solution.events)
    assert solution.total_cost == 23  # 5 + 8 + 5 = 23


def test_solve_with_pickup(ctsp_maximum_delivery_and_single_pickup, pickup_event):
    pickup_event.id, pickup_event.location_index = 2, 2
    ctsp_maximum_delivery_and_single_pickup.events[-1] = pickup_event
    ctsp_maximum_delivery_and_single_pickup.solve()
    solution = ctsp_maximum_delivery_and_single_pickup.get_solution(as_object=True)
    assert len(solution.events)
    assert solution.total_cost == 23  # 5 + 8 + 5 = 23


def test_solve_big_size_all_delivery():
    solver = CTSPWithMaximumDeliveryAndSinglePickupSolver()
    solver.load_data(Data.input_with_5_delivery_5_pickup)
    solver.solve()
    solution = solver.get_solution()
    assert len(solution["events"]) == len(Data.output_with_5_delivery_5_pickup["events"])
    assert [event["location_index"] for event in solution["events"]] == [event["location_index"] for event in
                                                                         Data.output_with_5_delivery_5_pickup["events"]]
    assert solution["cost"] == Data.output_with_5_delivery_5_pickup["cost"]


def test_combine_delivery_groups_with_single_pickup(ctsp_maximum_delivery_and_single_pickup, delivery_event, pickup_event):
    delivery_groups = [[delivery_event], [delivery_event]]
    pickups = [pickup_event]
    result = ctsp_maximum_delivery_and_single_pickup.combine_delivery_groups_with_single_pickup(delivery_groups, pickups)
    assert len(result) == 2
    assert result[0] == [delivery_event, pickup_event]
    assert result[1] == [delivery_event, pickup_event]


def test_get_nearest_neighbor_solutions_in_queue(ctsp_maximum_delivery_and_single_pickup):
    delivery_groups_with_single_pickup = [ctsp_maximum_delivery_and_single_pickup.events, ctsp_maximum_delivery_and_single_pickup.events]
    priority_queue = ctsp_maximum_delivery_and_single_pickup.get_nearest_neighbor_solutions_in_queue(
        delivery_groups_with_single_pickup)
    assert priority_queue.qsize() == 2
    assert priority_queue.get().total_cost == 23
    assert priority_queue.get().total_cost == 23


def test_get_solution_by_nearest_neighbor_solution(ctsp_maximum_delivery_and_single_pickup):
    route = ctsp_maximum_delivery_and_single_pickup.get_solution_by_nearest_neighbor_solution(
        ctsp_maximum_delivery_and_single_pickup.events)
    assert route.total_cost == 23  # 5 + 8 + 5 = 23


def test_get_deliveries(ctsp_maximum_delivery_and_single_pickup, delivery_event, pickup_event):
    events = [delivery_event, pickup_event, delivery_event, pickup_event, pickup_event]
    ctsp_maximum_delivery_and_single_pickup.events = events
    assert len(ctsp_maximum_delivery_and_single_pickup.get_deliveries()) == 2


def test_get_pickups(ctsp_maximum_delivery_and_single_pickup, delivery_event, pickup_event):
    events = [delivery_event, pickup_event, delivery_event, pickup_event, pickup_event]
    ctsp_maximum_delivery_and_single_pickup.events = events
    assert len(ctsp_maximum_delivery_and_single_pickup.get_pickups()) == 3


def test_find_delivery_groups_with_maximum_size(ctsp_maximum_delivery_and_single_pickup, delivery_event):
    deliveries = [delivery_event, delivery_event, delivery_event, delivery_event, delivery_event]
    delivery_groups_with_maximum_size = ctsp_maximum_delivery_and_single_pickup.find_delivery_groups_with_maximum_size(deliveries)
    assert len(delivery_groups_with_maximum_size) == 1
    assert len(delivery_groups_with_maximum_size[0]) == 5

    delivery_event_big_size = deepcopy(delivery_event)
    delivery_event_big_size.capacity = 1000
    deliveries = [delivery_event_big_size, delivery_event, delivery_event, delivery_event, delivery_event, delivery_event]
    delivery_groups_with_maximum_size = ctsp_maximum_delivery_and_single_pickup.find_delivery_groups_with_maximum_size(deliveries)
    assert len(delivery_groups_with_maximum_size) == 1
    assert len(delivery_groups_with_maximum_size[0]) == 5

def test_find_delivery_group_with_maximum_size(ctsp_maximum_delivery_and_single_pickup, delivery_event):
    deliveries = [delivery_event, delivery_event, delivery_event, delivery_event, delivery_event]
    delivery_groups_with_maximum_size = ctsp_maximum_delivery_and_single_pickup.find_delivery_group_with_maximum_size(deliveries)
    assert len(delivery_groups_with_maximum_size) == 5

    delivery_event_big_size = deepcopy(delivery_event)
    delivery_event_big_size.capacity = 1000
    deliveries = [delivery_event_big_size, delivery_event, delivery_event, delivery_event, delivery_event, delivery_event]
    delivery_groups_with_maximum_size = ctsp_maximum_delivery_and_single_pickup.find_delivery_group_with_maximum_size(deliveries)
    assert len(delivery_groups_with_maximum_size) == 5


def test_can_find_global_optimum(ctsp_maximum_delivery_and_single_pickup):
    assert ctsp_maximum_delivery_and_single_pickup.can_find_global_optimum(5) == True
    assert ctsp_maximum_delivery_and_single_pickup.can_find_global_optimum(10) == True
    assert ctsp_maximum_delivery_and_single_pickup.can_find_global_optimum(13) == False
