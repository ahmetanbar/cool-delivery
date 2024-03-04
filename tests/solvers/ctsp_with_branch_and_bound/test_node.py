import pytest


@pytest.mark.parametrize("events, expected_capacity",
                         [
                             ([("depot_start", 20), ("pickup", 50), ("delivery", 60)], 90),
                             ([("depot_start", 10)], 90),
                             ([("pickup", 50)], 50),
                             ([("delivery", 60)], 160),
                         ])
def test_add_event_successful(events, expected_capacity, path_manager, depot_start_event, pickup_event, delivery_event):
    path_manager.capacity = 100
    path_manager.path = []

    event_map = {
        "depot_start": depot_start_event,
        "pickup": pickup_event,
        "delivery": delivery_event
    }

    for event in events:
        target_event = event_map[event[0]]
        target_event.capacity = event[1]
        _ = path_manager.add_event(target_event)

    assert len(path_manager.path) == len(events)
    assert path_manager.capacity == expected_capacity


def test_add_event_unsuccessful(path_manager, depot_start_event):
    path_manager.capacity = 100
    path_manager.path = []

    depot_start_event.capacity = 110

    assert not path_manager.add_event(depot_start_event)
    assert len(path_manager.path) == 0
