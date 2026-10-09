from httpx import AsyncClient


async def test_register_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/register/",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
            "password2": "password123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access" in data
    assert "refresh" in data


async def test_register_dissmatch_passwords(client: AsyncClient):
    response = await client.post(
        "/api/v1/register/",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
            "password2": "password456",
        },
    )
    assert response.status_code == 422


async def test_register_duplicate(client: AsyncClient, test_user):
    response = await client.post(
        "/api/v1/register/",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "password123",
            "password2": "password123",
        },
    )
    assert response.status_code == 400


async def test_login_success(client: AsyncClient, test_user):
    response = await client.post(
        "/api/v1/login/",
        json={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access" in response.json()


async def test_login_wrong_password(client: AsyncClient, test_user):
    response = await client.post(
        "/api/v1/login/",
        json={"username": "testuser", "password": "wrong"},
    )
    assert response.status_code == 401


async def test_me_authorized(client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/me/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


async def test_create_author_unauthorized(client: AsyncClient):
    """Без токена — 401."""
    response = await client.post(
        "/api/v1/authors/",
        json={"name": "Иван Иванов"},
    )
    assert response.status_code == 401


async def test_create_author_forbidden(client: AsyncClient, auth_headers):
    """С токеном обычного юзера — 403."""
    response = await client.post(
        "/api/v1/authors/",
        json={"name": "Иван Иванов"},
        headers=auth_headers,
    )
    assert response.status_code == 403


async def test_make_me_admin(client: AsyncClient, auth_headers):
    response = await client.post("/api/v1/make-me-admin/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["is_admin"] is True
