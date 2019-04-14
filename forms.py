from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import IntegerField, validators


class LoginForm(FlaskForm):
    username = StringField('Логин', [validators.DataRequired('Введите логин')])
    password = PasswordField('Пароль', [validators.DataRequired('Введите пароль')])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class RegistryForm(FlaskForm):
    username = StringField('Логин', [validators.DataRequired('Введите логин')])
    password = PasswordField('Пароль', [validators.DataRequired('Введите пароль')])
    confirm_password = PasswordField('Потвердить пароль', [validators.DataRequired('Подтвердите пароль')])
    submit = SubmitField('Зарегистрироваться')


class AddProductForm(FlaskForm):
    name = StringField('Название', [validators.DataRequired('Введите название товара')])
    count = IntegerField('Количество', [validators.DataRequired('Укажите количество товара'),
                                        validators.NumberRange(min=1)])
    price = IntegerField('Стоимость (руб)', [validators.DataRequired('Укажите цену товара'),
                                             validators.NumberRange(min=1)])
    submit = SubmitField('Добавить')


class CountForm(FlaskForm):
    count = IntegerField('Количество', [validators.DataRequired('Укажите количество товара'),
                                        validators.NumberRange(min=1)])
    submit = SubmitField('Добавить в корзину')
