from httpx import AsyncClient


async def test_list_authors_public(client: AsyncClient):
    response = await client.get("/api/v1/authors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_author_as_admin(client: AsyncClient, admin_headers):
    response = await client.post(
        "/api/v1/authors/",
        json={"name": "Иван Иванов", "description": "Богослов"},
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Иван Иванов"
    assert "id" in data


async def test_create_author_as_user_forbidden(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/v1/authors/",
        json={"name": "Иван Иванов"},
        headers=auth_headers,
    )
    assert response.status_code == 403


async def test_create_author_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/v1/authors/",
        json={"name": "Иван Иванов"},
    )
    assert response.status_code == 401


async def test_get_author_not_found(client: AsyncClient):
    response = await client.get("/api/v1/authors/999/")
    assert response.status_code == 404


async def test_update_author(client: AsyncClient, admin_headers, db_session):
    from app.modules.catalog.models import Author

    author = Author(name="Old Name")
    db_session.add(author)
    await db_session.commit()
    await db_session.refresh(author)

    response = await client.patch(
        f"/api/v1/authors/{author.id}/",
        json={"name": "New Name"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


async def test_delete_author(client: AsyncClient, admin_headers, db_session):
    from app.modules.catalog.models import Author

    author = Author(name="To Delete")
    db_session.add(author)
    await db_session.commit()
    await db_session.refresh(author)

    response = await client.delete(
        f"/api/v1/authors/{author.id}/",
        headers=admin_headers,
    )
    assert response.status_code == 204
