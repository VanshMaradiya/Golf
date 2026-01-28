def test_user_register(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@gmail.com",
            "password": "123456",
            "role": "player"
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_user_login(client):
    # Register user first
    client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "testlogin@gmail.com",
            "password": "123456",
            "role": "player"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "testlogin@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "user_id" in response.json
    assert "role" in response.json

