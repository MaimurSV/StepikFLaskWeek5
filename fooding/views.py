import random
from datetime import datetime
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from fooding.models import Meal, MealCategory, User, Order
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
            user_id = session["user_id"]
            name = form.name.data
            address = form.name.data
            email = form.email.data
            phone = form.phone.data
            sum = session["sum"]
            order = Order(order_date=datetime.now(), status="new", address=address, email=email, phone=phone, sum=sum,
                         user_id=user_id)
            meal = Meal.query.filter(Meal.id.in_(session["cart"])).all()
            order.meals.extend(meal)
            db.session.add(order)
            db.session.commit()
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
    if "is_auth" in session.keys():
        if session["is_auth"]:
            orders = Order.query.filter_by(user_id=session["user_id"])
        else:
            return redirect("/login/")
    return render_template("account.html")


# ------------------------------------------------------
# Страница авторизации
@app.route("/login/", methods=["GET", "POST"])
def login_route():
    if "is_auth" in session.keys():
        if session["is_auth"]:
            return redirect("/account/")
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session["is_auth"] = True
                session["user_id"] = user.id
                if "error" in session.keys():
                    session.pop("error")
                return redirect("/account/")
            elif not user:
                session["error"] = "Пользователь не найден!"
            elif not check_password_hash(user.password, password):
                session["error"] = "Введенный Вами пароль неверен!"
    return render_template("login.html", form=form)


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
                user = User(email=email, password=generate_password_hash(password))
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
    session.clear()
    return redirect("/login/")


# ------------------------------------------------------
# Страница подтверждения отправки заказа
@app.route("/ordered/")
def ordered_route():
    return render_template("ordered.html")
