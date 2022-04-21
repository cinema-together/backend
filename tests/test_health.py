def test_health(test_app):
    """Тестирует эндпоинт /health."""

    response = test_app.get('/health')
    assert response.status_code == 200
    assert response.json() == {'environment': 'development', 'testing': True}
