import pytest
from starlette.testclient import TestClient

import app
from settings import BaseSettings, get_settings


def get_settings_override():
    """Переписывает настройки приложения для тестирования."""
    return BaseSettings(testing=True)


@pytest.fixture(scope='module')
def test_app():
    """Фикстура приложения для тестов."""
    app.app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app.app) as test_client:
        yield test_client
