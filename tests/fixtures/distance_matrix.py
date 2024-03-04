import pytest


@pytest.fixture
def distance_matrix():
    return [
        [0, 5, 10, 15],
        [5, 0, 8, 12],
        [10, 8, 0, 7],
        [15, 12, 7, 0],
    ]
