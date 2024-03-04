def test_capacity_effect_to_vehicle(depot_start_event, depot_end_event, pickup_event, delivery_event):
    assert depot_start_event.capacity_effect_to_vehicle == -10
    assert depot_end_event.capacity_effect_to_vehicle == 10
    assert delivery_event.capacity_effect_to_vehicle == 10
    assert pickup_event.capacity_effect_to_vehicle == -10
