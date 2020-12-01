import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired, Email
from fooding.config import MIN_PASSWORD_LENGTH


class OrderForm(FlaskForm):
    name = StringField("Ваше имя", validators=[InputRequired(message="Введите Ваше имя!"),
                                               Length(message="Имя не может быть меньше 3 символов!", min=3)])
    address = StringField("Ваш адрес", validators=[InputRequired(message="Введите Ваш адрес!"),
                                                   Length(message="Адрес не может быть меньше 5 символов!", min=5)])
    email = StringField("Электронная почта", validators=[InputRequired(message="Введите электронную почту!"),
                                                         Email(message="Введенный адрес электронной почты некорректен!")])
    phone = StringField("Ваше имя", validators=[InputRequired(message="Введите Ваше имя!"),
                                               Length(message="Имя не может быть меньше 3 символов!", min=3)])

