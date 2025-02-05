#!/usr/bin/env python3

from server.app import app  # Adjusted import
from server.models import db, Restaurant, Pizza, RestaurantPizza  # Adjusted import

with app.app_context():
    # Clear existing data
    print("Deleting existing data...")
    db.session.query(RestaurantPizza).delete()
    db.session.query(Pizza).delete()
    db.session.query(Restaurant).delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='address1')
    bistro = Restaurant(name="Sanjay's Pizza", address='address2')
    palace = Restaurant(name="Kiki's Pizza", address='address3')
    db.session.add_all([shack, bistro, palace])

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    db.session.add_all([cheese, pepperoni, california])

    print("Creating RestaurantPizza associations...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=5)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=10)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=15)
    db.session.add_all([pr1, pr2, pr3])

    db.session.commit()
    print("Seeding done!")