# Cool Delivery - Capacitated Traveling Salesman Problem with Pickup and Delivery (CTSPPD) Solvers

This repository contains three solvers for the CTSPPD implemented in Python. Each solver is designed to find an optimal
route for a vehicle to visit pickup and delivery events with specific constraints.

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