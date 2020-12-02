from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


orders_and_meals_table = db.Table('orders_and_meals',
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')),
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')))


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    picture = db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("meal-categories.id"), nullable=False)
    categories = db.relationship("MealCategory", back_populates="meals")
    orders = db.relationship(
        "Order", secondary=orders_and_meals_table, back_populates="meals"
    )


class MealCategory(db.Model):
    __tablename__ = "meal-categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    meals = db.relationship('Meal', back_populates='categories')


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    meals = db.relationship(
        "Meal", secondary=orders_and_meals_table, back_populates="orders"
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    users = db.relationship("User", back_populates="orders")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    orders = db.relationship("Order", back_populates="users")



