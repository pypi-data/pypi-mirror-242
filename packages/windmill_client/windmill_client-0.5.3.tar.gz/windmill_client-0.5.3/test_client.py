import os

import pytest
from windmill_client import Windmill


@pytest.fixture(scope="session")
def client():
    return Windmill()


def test_user(client):
    assert client.user
