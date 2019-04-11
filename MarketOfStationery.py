from flask import Flask, render_template, redirect, request, session, jsonify, make_response
from loginform import LoginForm
from db import DB, UserModel, CartsModel, ProductModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stationery'
db = DB()
users = UserModel(db.get_connection())
users.insert('kuku', 'qwerty')


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    product = ProductModel(db.get_connection()).get_all()
    return render_template('index.html', username=session['username'],
                           product=product)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
    exists = user_model.exists(user_name, password)
    if request.method == 'GET':
        return render_template('login.html', title='Авторизация', form=form)
    elif request.method == 'POST':
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index")


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route("/carts")
def carts():
    pass


if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=True)
