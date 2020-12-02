import random
from datetime import datetime
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from fooding.models import Meal, MealCategory, User, Order
from fooding.forms import OrderForm, RegistrationForm, LoginForm

from fooding import app, db


admin = Admin(app)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(MealCategory, db.session))

@app.template_filter("date_word")
def date_word(value):
    month_list = ["января", "февраля", "марта", "апреля", "мая", "июня",
                  "июля", "августа", "сентября", "октября", "ноября", "декабря"]

    month = month_list[int(datetime.strftime(value, "%m")) - 1]
    day = datetime.strftime(value, "%w")
    return day + " " + month


@app.template_filter("meal_word")
def meal_word(value):
    if value in [2, 3, 4]:
        return str(value) + " блюда"
    elif str(value)[len(str(value))-1]=="1":
        return str(value) + " блюдо"
    else:
        return str(value) + " блюд"
    

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
    cart = session.get("cart", [])
    sum = session.get("sum", 0)
    session["cart"] = cart
    session["sum"] = sum
    if request.method == "POST":
        if form.validate_on_submit() and sum != 0:
            user_id = session["user_id"]
            name = form.name.data
            address = form.name.data
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
                session["error"] = "Пользователь не найден!"
            elif not check_password_hash(user.password, password):
                session["error"] = "Введенный Вами пароль неверен!"
    return render_template("auth.html", form=form)


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
