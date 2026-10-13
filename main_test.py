import pytest from fastapi.testclient import TestClient

from app import app, items_db, ItemResponse

client = TestClient(app)

@pytest.fixture(autouse=True) def resetitemsdb(): """Reset test data before each test.""" itemsdb.clear() itemsdb.update({ 1: ItemResponse(id=1, name="Laptop", price=999.99), 2: ItemResponse(id=2, name="Mouse", price=25.50), })

def testhomeendpoint(): response = client.get("/")

	assert response.status_code == 200 assert response.json() == { "message": "Welcome to the Python API" }

def testhealthendpoint(): response = client.get("/health")

	assert response.status_code == 200 assert response.json() == {"status": "ok"}

def testgetallitemsendpoint(): response = client.get("/items")

	assert response.status_code == 200

data = response.json() assert len(data) == 2 assert data[0]["name"] == "Laptop" assert data[1]["name"] == "Mouse"

def testgetitembyid_endpoint(): response = client.get("/items/1")

	assert response.status_code == 200 assert response.json() == { "id": 1, "name": "Laptop", "price": 999.99, }

def testcreateitem_endpoint(): response = client.post( "/items", json={"name": "Keyboard", "price": 49.99}, )

	assert response.status_code == 201 assert response.json() == { "id": 3, "name": "Keyboard", "price": 49.99, }

def testgetmissingitemreturns_404(): response = client.get("/items/999")

	assert response.status_code == 404 assert response.json()["detail"] == "Item not found"

def testcreateitemrejectsinvalid_price(): response = client.post( "/items", json={"name": "Keyboard", "price": -10}, )

	assert response.status_code == 422