from cool_delivery.constants.event import EventConstant


def test_load_data(base_solver):
    solver = base_solver
    input_dict = {
        "depot": {"x": 0, "y": 0, "location_index": 0},
        "vehicle": {"capacity": 10},
        "events": [
            {"id": 1, "x": 1, "y": 1, "location_index": 1, "capacity": 10, "type": EventConstant.EventType.PICKUP},
            {"id": 2, "x": 2, "y": 2, "location_index": 2, "capacity": 10, "type": EventConstant.EventType.DELIVERY}
        ],
        "distance_matrix": [[0, 1, 2], [1, 0, 3], [2, 3, 0]],
    }
    solver.load_data(input_dict)

    assert (solver.depot.x, solver.depot.y) == (0, 0) and solver.depot.location_index == 0
    assert solver.vehicle.capacity == 10
    assert len(solver.events) == 2
    assert solver.distance_matrix.shape == (3, 3)
    assert solver.events[0].is_pickup and solver.events[1].is_delivery


def test_create_depot_events(base_solver, depot):
    solver = base_solver
    solver.depot = depot
    solver.create_depot_events()

    assert solver.depot_to_delivery.is_depot_start
    assert solver.depot_to_return.is_depot_end
    assert (solver.depot_to_delivery.x, solver.depot_to_delivery.y) == (depot.x, depot.y)


def test_get_solution(base_solver, route, event):
    solver = base_solver

    route.events = [event, event]
    route.total_cost = 10

    solver.optimum_route = route
    solution = solver.get_solution(as_object=False)

    expected_solution = {
        "cost": 10,
        "events": [
            {"id": event.id, "x": event.x, "y": event.y, "location_index": event.location_index, "capacity": event.capacity,
             "type": event.type},
            {"id": event.id, "x": event.x, "y": event.y, "location_index": event.location_index, "capacity": event.capacity,
             "type": event.type}
        ]
    }

    assert solution == expected_solution


def test_get_solution_as_object(base_solver, route, event):
    solver = base_solver

    route.events = [event, event]
    route.total_cost = 10

    solver.optimum_route = route
    solution = solver.get_solution(as_object=True)

    assert solution == route
