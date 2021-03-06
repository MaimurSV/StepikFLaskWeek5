import random
from datetime import datetime

from flask import abort, session, redirect, request, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash

from fooding import app, db
from fooding.forms import OrderForm, RegistrationForm, LoginForm
from fooding.models import Meal, MealCategory, User, Order


@app.template_filter("date_word")
def date_word(value):
    month_list = ["января", "февраля", "марта", "апреля", "мая", "июня",
                  "июля", "августа", "сентября", "октября", "ноября", "декабря"]

    month = month_list[int(datetime.strftime(value, "%m")) - 1]
    day = datetime.strftime(value, "%d").lstrip("0")
    return day + " " + month


@app.template_filter("meal_word")
def meal_word(value):
    if value in [2, 3, 4]:
        return str(value) + " блюда"
    elif str(value)[len(str(value)) - 1] == "1":
        return str(value) + " блюдо"
    else:
        return str(value) + " блюд"


# ------------------------------------------------------
# Главная страница
@app.route("/")
def index_route():
    meals_category = MealCategory.query.all()
    meals = []
    for row in MealCategory.query.join(MealCategory.meals):
        random.shuffle(row.meals)
        i = 0
        for meal in row.meals:
            meals.append(meal)
            i += 1
            if i >= 3:
                break
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
    cart = session.get("cart", [])
    sum = session.get("sum", 0)
    session["cart"] = cart
    session["sum"] = sum
    if request.method == "POST":
        if form.validate_on_submit() and sum != 0:
            user_id = session["user_id"]
            name = form.name.data
            address = form.address.data
            email = form.email.data
            phone = form.phone.data
            order = Order(order_date=datetime.now(), status="Заказ принят", address=address, email=email, phone=phone,
                          sum=sum, name=name,
                          user_id=user_id)
            meal = Meal.query.filter(Meal.id.in_(cart)).all()
            order.meals.extend(meal)
            db.session.add(order)
            db.session.commit()
            session.pop("cart")
            session.pop("sum")
            return render_template("ordered.html")
    meals = Meal.query.filter(Meal.id.in_(cart)).all()
    return render_template("cart.html", form=form, meals=meals)


# ------------------------------------------------------
# Корзина (удаление блюда из корзины)
@app.route("/cart/delete/<int:id>/")
def cart_delete_route(id):
    form = OrderForm()
    cart = session.get("cart", [])
    sum = session.get("sum", 0)
    if id in cart:
        cart.remove(id)
        meal = Meal.query.get_or_404(id)
        sum -= meal.price
    else:
        abort(404)
    session["cart"] = cart
    session["sum"] = sum
    meals = Meal.query.filter(Meal.id.in_(session["cart"])).all()
    return render_template("cart.html", form=form, meals=meals)


# ------------------------------------------------------
# Страница личного кабинета
@app.route("/account/")
def account_route():
    is_auth = session.get("is_auth", False)
    if is_auth:
        orders = Order.query.filter_by(user_id=session["user_id"]).order_by(Order.order_date.desc())
    else:
        return redirect("/auth/")
    return render_template("account.html", orders=orders)


# ------------------------------------------------------
# Страница авторизации
@app.route("/auth/", methods=["GET", "POST"])
def auth_route():
    is_auth = session.get("is_auth", False)
    if is_auth:
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
                flash("Пользователь не найден!")
            elif not check_password_hash(user.password, password):
                flash("Введенный Вами пароль неверен!")
    return render_template("auth.html", form=form)


# ------------------------------------------------------
# Страница регистрации
@app.route("/register/", methods=["GET", "POST"])
def register_route():
    is_auth = session.get("is_auth", False)
    if is_auth:
        return redirect("/account/")
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
                return redirect("/auth/")
    return render_template("register.html", form=form)


# ------------------------------------------------------
# Страница выхода
@app.route("/logout/")
def logout_route():
    session.clear()
    return redirect("/auth/")


# ------------------------------------------------------
# Страница подтверждения отправки заказа
@app.route("/ordered/")
def ordered_route():
    return render_template("ordered.html")
