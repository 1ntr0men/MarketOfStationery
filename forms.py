from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import IntegerField


class LoginForm(FlaskForm):
    username = StringField('Логин')
    password = PasswordField('Пароль')
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class RegistryForm(FlaskForm):
    username = StringField('Логин')
    password = PasswordField('Пароль')
    confirm_password = PasswordField('Потвердите пароль')
    submit = SubmitField('Зарегистрироваться')


class AddProductForm(FlaskForm):
    name = StringField('Название')
    count = IntegerField('Количество')
    price = StringField('Стоимость (руб)')
    submit = SubmitField('Добавить')
