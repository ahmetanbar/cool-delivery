from enum import StrEnum

from src.solvers.CTSPWithBranchAndBound.solver import Solver as CTSPWithBranchAndBoundSolver
from src.solvers.CTSPWithNearestNeighbor.solver import Solver as CTSPWithNearestNeighborSolver
from src.solvers.CTSPWithMaximumDeliveryAndSinglePickup.solver import Solver as CTSPSolver


class SolverConstant:
    class Name(StrEnum):
        BRANCH_AND_BOUND = "branch_and_bound"
        NEAREST_NEIGHBOR = "nearest_neighbor"
        MAXIMIZE_DELIVERY_WITH_SINGLE_PICKUP = "maximize_delivery_with_single_pickup"

    STR_TO_CLASS = {
        Name.BRANCH_AND_BOUND: CTSPWithBranchAndBoundSolver,
        Name.NEAREST_NEIGHBOR: CTSPWithNearestNeighborSolver,
        Name.MAXIMIZE_DELIVERY_WITH_SINGLE_PICKUP: CTSPSolver,
    }
