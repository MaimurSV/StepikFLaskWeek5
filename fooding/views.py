import random
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template
from fooding.models import Meal, MealCategory

from fooding import app, db


# ------------------------------------------------------
# Главная страница
@app.route("/")
def index_route():
    meals_category = MealCategory.query.all()
    meals = Meal.query.all()
    # Решение задачи со случайным отображением трех блюд с каждой категориии
    # Перемешиваем блюда, затем проходясь в цикле по категориям, проходимся в цикле по
    # блюдам, находим блюда
    # этой категории, если число найденных блюд достигло 3 и выше, удаляем эти блюда.
    # Повторно делаем запрос ко вем блюдам и опять их перемемешиваем (хотя это уже необязательно)
    random.shuffle(meals)
    for category in meals_category:
        i = 0
        for meal in meals:
            if meal.category_id == category.id:
                i += 1
                if i > 3:
                    Meal.query.filter_by(id=meal.id).delete()
    meals = Meal.query.all()
    random.shuffle(meals)
    return render_template("main.html", meals=meals, meals_category=meals_category)


# ------------------------------------------------------
# Корзина
@app.route("/addtocart/<int:id>/")
def addtocart_route(id):
    Meal.query.get_or_404(id)
    cart = session.get("cart", [])
    if id not in cart:
        cart.append(id)
        session["cart"] = cart
    return redirect("/cart/")


# ------------------------------------------------------
# Корзина
@app.route("/cart/")
def cart_route():
    meals = Meal.query.filter(Meal.id.in_(session["cart"])).all()
    return render_template("cart.html", meals=meals)


# ------------------------------------------------------
# Корзина (удаление блюда из корзины)
@app.route("/cart/delete/<int:id>/")
def cart_delete_route(id):
    if id in session["cart"]:
        cart = session.get("cart")
        cart.remove(id)
    session["cart"] = cart
    meals = Meal.query.filter(Meal.id.in_(session["cart"])).all()
    return render_template("cart.html", meals=meals)


# ------------------------------------------------------
# Страница личного кабинета
@app.route("/account/")
def account_route():
    return render_template("account.html")


# ------------------------------------------------------
# Страница авторизации
@app.route("/login/")
def login_route():
    return render_template("login.html")


# ------------------------------------------------------
# Страница регистрации
@app.route("/register/")
def register_route():
    return render_template("register.html")


# ------------------------------------------------------
# Страница выхода
@app.route("/logout/")
def logout_route():
    return render_template("logout.html")


# ------------------------------------------------------
# Страница подтверждения отправки заказа
@app.route("/ordered/")
def ordered_route():
    return render_template("ordered.html")
