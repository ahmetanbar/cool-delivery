from enum import StrEnum

from cool_delivery.solvers import (CTSPWithBranchAndBoundSolver,
                                   CTSPWithNearestNeighborSolver,
                                   CTSPWithMaximumDeliveryAndSinglePickupSolver)


class SolverConstant:
    class Name(StrEnum):
        BRANCH_AND_BOUND = "branch_and_bound"
        NEAREST_NEIGHBOR = "nearest_neighbor"
        MAXIMIZE_DELIVERY_WITH_SINGLE_PICKUP = "maximize_delivery_with_single_pickup"

    STR_TO_CLASS = {
        Name.BRANCH_AND_BOUND: CTSPWithBranchAndBoundSolver,
        Name.NEAREST_NEIGHBOR: CTSPWithNearestNeighborSolver,
        Name.MAXIMIZE_DELIVERY_WITH_SINGLE_PICKUP: CTSPWithMaximumDeliveryAndSinglePickupSolver,
    }
