from httpx import AsyncClient


async def test_list_books_public(client: AsyncClient):
    response = await client.get("/api/v1/books/")
    assert response.status_code == 200


async def test_create_book_as_admin(client: AsyncClient, admin_headers, db_session):
    from app.modules.catalog.models import Author, Category

    author = Author(name="Test Author")
    category = Category(name="Test Category")
    db_session.add_all([author, category])
    await db_session.commit()
    await db_session.refresh(author)
    await db_session.refresh(category)

    response = await client.post(
        "/api/v1/books/",
        json={
            "title": "Test Book",
            "author_id": author.id,
            "price": "19.99",
            "category_ids": [category.id],
        },
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"]["id"] == author.id
    assert len(data["categories"]) == 1


async def test_create_book_invalid_author(client: AsyncClient, admin_headers):
    response = await client.post(
        "/api/v1/books/",
        json={
            "title": "Test Book",
            "author_id": 999,
            "price": "19.99",
            "category_ids": [],
        },
        headers=admin_headers,
    )
    assert response.status_code == 400
    assert "Автор не найден" in response.json()["detail"]


async def test_create_book_forbidden(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/v1/books/",
        json={
            "title": "Test Book",
            "author_id": 1,
            "price": "19.99",
            "category_ids": [],
        },
        headers=auth_headers,
    )
    assert response.status_code == 403
