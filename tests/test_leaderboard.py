def test_add_score(client):
    # -------------------------
    # Register admin
    # -------------------------
    client.post(
        "/api/auth/register",
        json={
            "name": "Admin",
            "email": "admin@gmail.com",
            "password": "admin123",
            "role": "admin"
        }
    )

    # Login admin
    login_resp = client.post(
        "/api/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin123"
        }
    )

    admin_id = login_resp.json["user_id"]
    admin_role = login_resp.json["role"]

    admin_headers = {
        "X-User-Id": str(admin_id),
        "X-User-Role": admin_role
    }

    # -------------------------
    # Create course
    # -------------------------
    client.post(
        "/api/admin/courses",
        headers=admin_headers,
        json={
            "name": "Test Course",
            "location": "India",
            "total_holes": 18
        }
    )

    # Add hole
    client.post(
        "/api/admin/courses/1/holes",
        headers=admin_headers,
        json={
            "hole_number": 1,
            "par": 4
        }
    )

    # -------------------------
    # Create tournament (IMPORTANT)
    # -------------------------
    client.post(
        "/api/tournaments",
        headers=admin_headers,
        json={
            "name": "Test Tournament",
            "course_id": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-05",
            "status": "ongoing"
        }
    )

    # -------------------------
    # Register player
    # -------------------------
    client.post(
        "/api/auth/register",
        json={
            "name": "Player",
            "email": "player@gmail.com",
            "password": "player123",
            "role": "player"
        }
    )

    # Login player
    login_resp = client.post(
        "/api/auth/login",
        json={
            "email": "player@gmail.com",
            "password": "player123"
        }
    )

    player_id = login_resp.json["user_id"]
    player_role = login_resp.json["role"]

    player_headers = {
        "X-User-Id": str(player_id),
        "X-User-Role": player_role
    }

    # -------------------------
    # Add score
    # -------------------------
    response = client.post(
        "/api/scores/tournaments/1/holes/1",
        headers=player_headers,
        json={
            "strokes": 5
        }
    )

    assert response.status_code == 200
    assert "Score" in response.json["message"]


def test_leaderboard(client):
    # Register admin
    client.post(
        "/api/auth/register",
        json={
            "name": "Admin",
            "email": "admin_lb@gmail.com",
            "password": "admin123",
            "role": "admin"
        }
    )

    # Login admin
    admin_login = client.post(
        "/api/auth/login",
        json={
            "email": "admin_lb@gmail.com",
            "password": "admin123"
        }
    )

    admin_id = admin_login.json["user_id"]
    admin_role = admin_login.json["role"]

    admin_headers = {
        "X-User-Id": str(admin_id),
        "X-User-Role": admin_role
    }

    # Create golf course
    client.post(
        "/api/admin/courses",
        headers=admin_headers,
        json={
            "name": "Leaderboard Course",
            "location": "France",
            "total_holes": 18
        }
    )

    # Add hole
    client.post(
        "/api/admin/courses/1/holes",
        headers=admin_headers,
        json={
            "hole_number": 1,
            "par": 4
        }
    )

    # Create tournament
    client.post(
        "/api/tournaments",
        headers=admin_headers,
        json={
            "name": "Leaderboard Tournament",
            "course_id": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-05",
            "status": "ongoing"
        }
    )

    # Register player
    client.post(
        "/api/auth/register",
        json={
            "name": "Player One",
            "email": "player_lb@gmail.com",
            "password": "player123",
            "role": "player"
        }
    )

    # Login player
    player_login = client.post(
        "/api/auth/login",
        json={
            "email": "player_lb@gmail.com",
            "password": "player123"
        }
    )

    player_id = player_login.json["user_id"]
    player_role = player_login.json["role"]

    player_headers = {
        "X-User-Id": str(player_id),
        "X-User-Role": player_role
    }

    # Add score
    client.post(
        "/api/scores/tournaments/1/holes/1",
        headers=player_headers,
        json={
            "strokes": 4
        }
    )

    # Get leaderboard
    response = client.get(
        "/api/leaderboard/tournaments/1"
    )

    assert response.status_code == 200
    assert "leaderboard" in response.json
    assert len(response.json["leaderboard"]) > 0
