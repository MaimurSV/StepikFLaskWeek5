from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    picture = db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("meal-categories.id"), nullable=False)
    categories = db.relationship("MealCategory", back_populates="meals")


class MealCategory(db.Model):
    __tablename__ = "meal-categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    meals = db.relationship('Meal', back_populates='categories')


