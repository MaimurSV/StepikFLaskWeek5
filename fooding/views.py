import random
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from fooding.models import Meal, MealCategory, User
from fooding.forms import OrderForm, RegistrationForm, LoginForm

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
    meal = Meal.query.get_or_404(id)
    cart = session.get("cart", [])
    sum = session.get("sum", 0)
    if id not in cart:
        sum += meal.price
        cart.append(id)
    session["cart"] = cart
    session["sum"] = sum
    return redirect("/cart/")


# ------------------------------------------------------
# Корзина
@app.route("/cart/", methods=["GET", "POST"])
def cart_route():
    form = OrderForm()
    if request.method == "POST":
        if form.validate_on_submit():
            return render_template("ordered.html")
    meals = Meal.query.filter(Meal.id.in_(session["cart"])).all()
    return render_template("cart.html", form=form, meals=meals)


# ------------------------------------------------------
# Корзина (удаление блюда из корзины)
@app.route("/cart/delete/<int:id>/")
def cart_delete_route(id):
    cart = session.get("cart")
    sum = session.get("sum", 0)
    if id in session["cart"]:
        cart.remove(id)
        meal = Meal.query.get_or_404(id)
        sum -= meal.price
    session["cart"] = cart
    session["sum"] = sum
    meals = Meal.query.filter(Meal.id.in_(session["cart"])).all()
    return render_template("cart.html", meals=meals)


# ------------------------------------------------------
# Страница личного кабинета
@app.route("/account/")
def account_route():
    return render_template("account.html")


# ------------------------------------------------------
# Страница авторизации
@app.route("/login/", methods=["GET", "POST"])
def login_route():
    return render_template("login.html")


# ------------------------------------------------------
# Страница регистрации
@app.route("/register/", methods=["GET", "POST"])
def register_route():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if not User.query.filter_by(email=form.email.data).first():
                email = form.email.data
                password = form.password.data
                user = User(email=email, password=password)
                db.session.add(user)
                db.session.commit()
                session["is_auth"] = True
                session["user_id"] = user.id
                return redirect("/account/")
            else:
                return redirect("/login/")
    return render_template("register.html", form=form)


# ------------------------------------------------------
# Страница выхода
@app.route("/logout/")
def logout_route():
    session.clear
    return render_template("login.html")


# ------------------------------------------------------
# Страница подтверждения отправки заказа
@app.route("/ordered/")
def ordered_route():
    return render_template("ordered.html")
