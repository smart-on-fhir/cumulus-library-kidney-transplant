from unittest import mock
import pytest


@pytest.fixture()
def database():
    return mock.Mock(name="database")
