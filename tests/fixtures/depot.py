import pytest

from cool_delivery.models import Depot


@pytest.fixture
def depot():
    return Depot(x=1, y=1, location_index=0)
