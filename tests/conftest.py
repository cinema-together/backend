import os

import pytest
from starlette.testclient import TestClient

import app
from settings import get_settings, BaseSettings


def get_settings_override():
    return BaseSettings(testing=True)


@pytest.fixture(scope='module')
def test_app():
    """Фикстура приложения для тестов."""
    app.app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app.app) as test_client:
        yield test_client
