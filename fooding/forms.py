import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired, Email, DataRequired, EqualTo, ValidationError
from fooding.config import MIN_PASSWORD_LENGTH


class OrderForm(FlaskForm):
    name = StringField("Ваше имя", validators=[InputRequired(message="Введите Ваше имя!"),
                                               Length(min=4, max=32,
                                                      message="Имя должно быть не менее 4 и не боле 32 символов")
                                               ])
    address = StringField("Ваш адрес", validators=[InputRequired(message="Введите Ваш адрес!"),
                                                   Length(message="Адрес не может быть меньше 5 символов!", min=5)])
    email = StringField("Электронная почта", validators=[InputRequired(message="Введите электронную почту!"),
                                                         Email(
                                                             message="Введенный адрес электронной почты некорректен!")])
    phone = StringField("Ваше телефон", validators=[InputRequired(message="Введите Ваше телефон!"),
                                                Length(message="Имя не может быть меньше 3 символов!", min=3)])


def password_check(form, field):
    msg = "Пароль должен содержать латинские сивмолы в верхнем и нижнем регистре и цифры!"
    patern1 = re.compile(r'[a-z]+')
    patern2 = re.compile(r'[A-Z]+')
    patern3 = re.compile(r'\d+')
    if (not patern1.search(field.data) or
            not patern2.search(field.data) or
            not patern3.search(field.data)):
        raise ValidationError(msg)


class LoginForm(FlaskForm):
    email = StringField("Имя:", validators=[InputRequired(message="Введите электронную почту!"),
                                            Email(message="Введенный адрес электронной почты некорректен!")])
    password = PasswordField("Пароль:", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    email = StringField(
        "Электронная почта",
        validators=[InputRequired(message="Введите электронную почту!"),
                    Email(message="Введенный адрес электронной почты некорректен!")]
    )
    password = PasswordField(
        "Пароль:",
        validators=[
            DataRequired(),
            Length(min=MIN_PASSWORD_LENGTH, message="Пароль должен быть не менее " + str(MIN_PASSWORD_LENGTH) + " символов"),
            EqualTo('confirm_password', message="Пароли не одинаковые"),
            password_check
        ]
    )
    confirm_password = PasswordField("Пароль ещё раз:")
