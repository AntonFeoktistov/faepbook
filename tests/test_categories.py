from httpx import AsyncClient


async def test_list_categories_public(client: AsyncClient):
    response = await client.get("/api/v1/categories/")
    assert response.status_code == 200


async def test_create_category_as_admin(client: AsyncClient, admin_headers):
    response = await client.post(
        "/api/v1/categories/",
        json={"name": "Православие"},
        headers=admin_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Православие"


async def test_create_category_forbidden(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/v1/categories/",
        json={"name": "Православие"},
        headers=auth_headers,
    )
    assert response.status_code == 403
