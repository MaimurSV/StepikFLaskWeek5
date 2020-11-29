from functools import wraps

from flask import abort, flash, session, redirect, request, render_template

from fooding import app, db


# ------------------------------------------------------
# Главная страница
@app.route("/")
def index_route():
    return render_template("main.html")


# ------------------------------------------------------
# Корзина
@app.route("/cart/")
def cart_route():
    return render_template("cart.html")


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
