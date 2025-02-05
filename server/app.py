#!/usr/bin/env python3
from server.models import db, Restaurant, RestaurantPizza, Pizza  # Updated import
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# GET /restaurants
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])

# GET /restaurants/<int:id>
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = db.session.get(Restaurant, id)  # Updated for compatibility
    if restaurant:
        return jsonify(restaurant.to_dict())
    return jsonify({"error": "Restaurant not found"}), 404

# POST /restaurants
@app.route("/restaurants", methods=["POST"])
def create_restaurant():
    data = request.get_json()
    try:
        new_restaurant = Restaurant(**data)
        db.session.add(new_restaurant)
        db.session.commit()
        return jsonify(new_restaurant.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": str(e)}), 400

# DELETE /restaurants/<int:id>
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)  # Updated for compatibility
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    return jsonify({"error": "Restaurant not found"}), 404

# GET /pizzas
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas])

# GET /pizzas/<int:id>
@app.route("/pizzas/<int:id>", methods=["GET"])
def get_pizza(id):
    pizza = db.session.get(Pizza, id)  # Updated for compatibility
    if pizza:
        return jsonify(pizza.to_dict())
    return jsonify({"error": "Pizza not found"}), 404

# POST /pizzas
@app.route("/pizzas", methods=["POST"])
def create_pizza():
    data = request.get_json()
    try:
        new_pizza = Pizza(**data)
        db.session.add(new_pizza)
        db.session.commit()
        return jsonify(new_pizza.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": str(e)}), 400

# POST /restaurant_pizzas
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        new_restaurant_pizza = RestaurantPizza(**data)
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)