import pytest

from cool_delivery.models import Route


@pytest.fixture
def route(event):
    return Route(events=[event])
