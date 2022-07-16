from app import main


def test_ping(test_app):
    # Given
    # test_app -> FastAPI fixture app

    # When
    response = test_app.get("/ping")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "environment": "dev",
        "testing": True,
        "ping": "pong!",
    }