from copy import deepcopy

import pytest

def test_solve(ctsp_with_nearest_neighbor_solver):
    ctsp_with_nearest_neighbor_solver.solve()
    solution = ctsp_with_nearest_neighbor_solver.get_solution(as_object=True)
    assert len(solution.events)
    assert solution.total_cost == 10


def test_is_path_completed(ctsp_with_nearest_neighbor_solver, event):
    ctsp_with_nearest_neighbor_solver.full_path_length = 3
    ctsp_with_nearest_neighbor_solver.path_manager.path = [event, event]
    assert ctsp_with_nearest_neighbor_solver.is_path_completed()
    ctsp_with_nearest_neighbor_solver.path_manager.path = [event, event, event, event]
    assert ctsp_with_nearest_neighbor_solver.is_path_completed()


def test_find_next_event(ctsp_with_nearest_neighbor_solver, event):
    def mock_find_nearest_event(event, events):
        return event

    def mock_add_event(event):
        if event.id == 2:
            return False
        return True

    ctsp_with_nearest_neighbor_solver.find_nearest_event = mock_find_nearest_event
    ctsp_with_nearest_neighbor_solver.path_manager.add_event = mock_add_event

    ctsp_with_nearest_neighbor_solver.unvisited_events = {event}

    next_event = ctsp_with_nearest_neighbor_solver.find_next_event(event)
    assert next_event.id == 1
    assert len(ctsp_with_nearest_neighbor_solver.skipped_events) == 0
    assert len(ctsp_with_nearest_neighbor_solver.unvisited_events) == 0

    event.id = 2
    ctsp_with_nearest_neighbor_solver.unvisited_events = {event}
    next_event = ctsp_with_nearest_neighbor_solver.find_next_event(event)
    assert next_event == event
    assert len(ctsp_with_nearest_neighbor_solver.skipped_events) == 1
    assert event not in ctsp_with_nearest_neighbor_solver.unvisited_events


def test_skip_event(ctsp_with_nearest_neighbor_solver, event):
    ctsp_with_nearest_neighbor_solver.unvisited_events = {event}
    ctsp_with_nearest_neighbor_solver.skip_event(event)
    assert len(ctsp_with_nearest_neighbor_solver.skipped_events) == 1
    assert event not in ctsp_with_nearest_neighbor_solver.unvisited_events


def test_start_route(ctsp_with_nearest_neighbor_solver, event):
    ctsp_with_nearest_neighbor_solver.depot_to_delivery = event
    assert ctsp_with_nearest_neighbor_solver.start_route() == event


def test_finalize_route(ctsp_with_nearest_neighbor_solver, event):
    ctsp_with_nearest_neighbor_solver.depot_to_return = event
    ctsp_with_nearest_neighbor_solver.path_manager.path = [event, event]
    ctsp_with_nearest_neighbor_solver.finalize_route()
    assert ctsp_with_nearest_neighbor_solver.optimum_route.events == [event, event, event]


def test_calculate_route_distance(ctsp_with_nearest_neighbor_solver, event):
    event_1 = deepcopy(event)
    event_2 = deepcopy(event)

    event_1.location_index = 0
    event_2.location_index = 1

    ctsp_with_nearest_neighbor_solver.path_manager.path = [event_1, event_2]
    ctsp_with_nearest_neighbor_solver.distance_matrix = [[0, 1], [1, 0]]
    assert ctsp_with_nearest_neighbor_solver.calculate_route_distance() == 1


def test_find_nearest_event(ctsp_with_nearest_neighbor_solver, event):
    event_1 = deepcopy(event)
    event_2 = deepcopy(event)
    event_3 = deepcopy(event)

    event_1.location_index = 0
    event_2.location_index = 1
    event_3.location_index = 2

    ctsp_with_nearest_neighbor_solver.distance_matrix = [[0, 1, 4], [1, 0, 5], [4, 5, 0]]

    assert ctsp_with_nearest_neighbor_solver.find_nearest_event(event_1, {event_1, event_2, event_3}) == event_1
    assert ctsp_with_nearest_neighbor_solver.find_nearest_event(event_2, {event_1, event_2, event_3}) == event_2


def test_handle_skipped_event(ctsp_with_nearest_neighbor_solver, event):
    ctsp_with_nearest_neighbor_solver.unvisited_events = {event}
    ctsp_with_nearest_neighbor_solver.handle_skipped_event(event)
    assert len(ctsp_with_nearest_neighbor_solver.skipped_events) == 1
    assert event not in ctsp_with_nearest_neighbor_solver.unvisited_events


def test_create_depot_events(ctsp_with_nearest_neighbor_solver, pickup_event, delivery_event):
    pickup_event.capacity = 10
    delivery_event.capacity = 40

    ctsp_with_nearest_neighbor_solver.events = [pickup_event, delivery_event]
    ctsp_with_nearest_neighbor_solver.vehicle.capacity = 51

    ctsp_with_nearest_neighbor_solver.create_depot_events()
    assert ctsp_with_nearest_neighbor_solver.depot_to_return.capacity == 10
    assert ctsp_with_nearest_neighbor_solver.depot_to_delivery.capacity == 40

    pickup_event.capacity = 20
    delivery_event.capacity = 10

    ctsp_with_nearest_neighbor_solver.events = [pickup_event, delivery_event]
    ctsp_with_nearest_neighbor_solver.vehicle.capacity = 11

    with pytest.raises(ValueError):
        ctsp_with_nearest_neighbor_solver.create_depot_events()
