import pytest

from cool_delivery.models import Vehicle


@pytest.fixture
def vehicle():
    return Vehicle(capacity=100)
