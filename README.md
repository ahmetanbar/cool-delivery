# Cool Delivery - Capacitated Traveling Salesman Problem with Pickup and Delivery (CTSPPD) Solvers

This repository contains three solvers for the CTSPPD implemented in Python. Each solver is designed to find an optimal
route for a vehicle to visit pickup and delivery events with specific constraints.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Data Format](#data-format)
- [Problem Statement](#problem-statement)
- [Objective Function](#objective-function)
- [Solvers](#solvers)
- [Data Generation](#data-generation)
- [License](#license)

## Installation

To install the package, you can use the following command:

```bash
pip install cool-delivery@git+https://github.com/ahmetanbar/cool-delivery
```

or you can clone the repository and install the package with the following command:

```bash
git clone https://github.com/ahmetanbar/cool-delivery.git
cd cool-delivery
pip install .
```

## Usage

You can use the solvers by importing them from the package. Here is an example of how to use the solvers:

```python
from cool_delivery.solvers import CTSPWithBranchAndBoundSolver, CTSPWithNearestNeighborSolver, CTSPWithMaximumDeliveryAndSinglePickupSolver

solver = CTSPWithMaximumDeliveryAndSinglePickupSolver()
solver.load_data(data_dict)
solution = solver.get_solution()
```

or you can use the solvers with the following command:

```bash
python -m cool_delivery.__main__.py solve maximize_delivery_with_single_pickup input_5p_5d.json output_5p_5d.json
```

or

```bash
cool_delivery solve maximize_delivery_with_single_pickup input_5p_5d.json output_5p_5d.json
```

Please check the `help` command for more information about the usage of the solvers.

```bash
cool_delivery --help
```

## Data Format

The solvers use a dictionary to represent the problem. The dictionary should have the following
keys:

### Input Data

```
{
    "depot": {
        "x": 0,
        "y": 0,
        "location_index": 0
    },
    "vehicle": {
      "capacity": 25
    },
    "events": [
        {
            "id": 1,
            "x": 1,
            "y": 1,
            "location_index": 1,
            "type": "pickup",
            "capacity": 25
        },
        {
            "id": 2,
            "x": 2,
            "y": 2,
            "location_index": 2,
            "type": "delivery",
            "capacity": 25
        }
    ],
    "distance_matrix": [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]
}
```

### Output Data

```
{
    {
  "cost": 6,
  "events": [
    {
      "id": 0,
      "x": 0,
      "y": 0,
      "location_index": 0,
      "capacity": 20,
      "type": "depot_start"
    },
    {
      "id": 1,
      "x": 14,
      "y": 30,
      "location_index": 1,
      "capacity": 20,
      "type": "delivery"
    },
    {
      "id": 2,
      "x": 39,
      "y": 68,
      "location_index": 2,
      "capacity": 37,
      "type": "pickup"
    },
    {
      "id": 0,
      "x": 0,
      "y": 0,
      "location_index": 0,
      "capacity": 37,
      "type": "depot_end"
    }
  ]
}
```

## Problem Statement:

The Capacitated Traveling Salesman Problem with Pickup and Delivery (CTSPPD) is a variant of the Traveling Salesman
Problem (TSP) that involves a vehicle with a limited capacity to visit pickup and delivery points. The vehicle must
start and end its route at the depot.

There are two cases for the problem:

1. Vehicle visits all delivery and pickup points, which is the more common case. It means that vehicle capacity is
   enough to carry all delivery loads at once and to carry all pickup loads at once when returning to the depot.
2. Vehicle visits limited delivery and pickup points, which is the more specific case. It means that vehicle capacity is
   not enough to carry all delivery loads at once.

## Objective Function:

For the first case, the objective is to minimize the total distance traveled.

For the second case, it is really custom case but the objective is to maximize the number of delivery points visited
with a single pickup point. Also, the second objective is to minimize the total distance traveled.

## Solvers:

### Case 1: Vehicle visits all delivery and pickup points - Optimizes the total distance traveled

#### 1. Branch and Bound Solver

This solver utilizes a modified Branch and Bound algorithm to find the optimal route for the vehicle. It calculates
bounds using the distance matrix and vehicle capacity.

It provides the optimal solution for the problem. It is the most accurate solver but it is not efficient for large-scale
problems. It is recommended to use this solver for small-scale problems.

#### 2. Nearest Neighbor Solver

This solver employs the Nearest Neighbor algorithm to find the optimal route for the vehicle to visit all pickup and
delivery events.

It provides a good solution for the problem, not an optimal one. It is efficient for large-scale problems. It is
recommended to use this solver for large-scale problems.

### Case 2: Vehicle visits limited delivery and pickup points - Maximizes the number of delivery points visited with a single pickup point

#### 3. Maximum Delivery and Single Pickup Solver

This solver prioritizes finding delivery groups with maximum size along with a single pickup event.
It employs a combination of heuristics.

1. First, it identifies maximum delivery group combinations.
2. And then, it combines these groups for each single pickup
   point.
3. It optimizes the routes using the nearest neighbor algorithm.
4. If the maximum delivery count is not larger than a threshold, it employs
   the branch and bound algorithm to find the global optimum for the first N solution with minimum distance found in
   previous step. The best one is selected as the final solution.
5. If the maximum delivery count is larger than a threshold, the solution with minimum distance found in 3. step is
   selected as the final solution.

## Data Generation

You can use the data generation script to generate random data for the problem. You can use the following command to
generate data:

```bash
python -m cool_delivery.__main__.py generate 5 5 input_5p_5d.json
```

or

```bash
cool_delivery generate 5 5 input_5p_5d.json
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Authors

- Ahmet Anbar