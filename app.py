from flask import Flask, jsonify, request

app = Flask(__name__)

# Demo-only in-memory data. Data resets when the process restarts.
inventory = {"keyboard": 20, "mouse": 30, "monitor": 10}
orders = []
next_order_id = 1


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/inventory")
def get_inventory():
    return jsonify(inventory), 200


@app.get("/orders")
def get_orders():
    return jsonify(orders), 200


@app.post("/orders")
def create_order():
    global next_order_id
    data = request.get_json(silent=True) or {}
    product = data.get("product")
    quantity = data.get("quantity")

    if not isinstance(product, str) or not product:
        return jsonify(error="product is required"), 400
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        return jsonify(error="quantity must be a positive integer"), 400
    if product not in inventory:
        return jsonify(error="product not found"), 404
    if inventory[product] < quantity:
        return jsonify(error="insufficient inventory"), 409

    inventory[product] -= quantity
    order = {
        "id": next_order_id,
        "product": product,
        "quantity": quantity,
        "status": "PLACED",
    }
    orders.append(order)
    next_order_id += 1
    return jsonify(order), 201


@app.put("/orders/<int:order_id>/status")
def update_order_status(order_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in {"PLACED", "PROCESSING", "SHIPPED", "CANCELLED"}:
        return jsonify(error="invalid status"), 400

    for order in orders:
        if order["id"] == order_id:
            order["status"] = status
            return jsonify(order), 200
    return jsonify(error="order not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
