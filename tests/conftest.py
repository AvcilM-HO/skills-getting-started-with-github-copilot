import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

_BASELINE_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    app_module.activities = copy.deepcopy(_BASELINE_ACTIVITIES)
    yield
    app_module.activities = copy.deepcopy(_BASELINE_ACTIVITIES)


@pytest.fixture
def client():
    return TestClient(app_module.app)
