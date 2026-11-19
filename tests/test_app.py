
from app import app, inventory, orders


def setup_function():
    inventory.update({
        "keyboard": 20,
        "mouse": 30,
        "monitor": 10
    })
    orders.clear()


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200


def test_inventory():
    client = app.test_client()
    response = client.get("/inventory")
    assert response.status_code == 200


def test_create_order():
    client = app.test_client()
    response = client.post(
        "/orders",
        json={"product": "keyboard", "quantity": 2}
    )
    assert response.status_code == 201


def test_invalid_quantity():
    client = app.test_client()
    response = client.post(
        "/orders",
        json={"product": "keyboard", "quantity": 0}
    )
    assert response.status_code == 400
