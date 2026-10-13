import pytest
from fastapi.testclient import TestClient

from app import app, items_db, ItemResponse

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_items_db():
    items_db.clear()
    items_db.update({
        1: ItemResponse(id=1, name="Laptop", price=999.99),
        2: ItemResponse(id=2, name="Mouse", price=25.50),
    })


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Python API"
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_all_items_endpoint():
    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_item_by_id_endpoint():
    response = client.get("/items/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
    }


def test_create_item_endpoint():
    response = client.post(
        "/items",
        json={"name": "Keyboard", "price": 49.99},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "name": "Keyboard",
        "price": 49.99,
    }


def test_get_missing_item_returns_404():
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_create_item_rejects_invalid_price():
    response = client.post(
        "/items",
        json={"name": "Keyboard", "price": -10},
    )

    assert response.status_code == 422