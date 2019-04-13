from flask import Flask, render_template, redirect, request, session, jsonify, make_response
from forms import LoginForm, RegistryForm
from db import DB, UserModel, CartsModel, ProductModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stationery'
db = DB()
product_model = ProductModel(db.get_connection())
user_model = UserModel(db.get_connection())
carts_model = CartsModel(db.get_connection())


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    product = product_model.get_all()
    return render_template('index.html', username=session['username'],
                           product=product, title='Store', registered=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    exists = user_model.exists(user_name, password)
    if request.method == 'GET':
        return render_template('login.html', title='Signing in', form=form)
    elif request.method == 'POST':
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        else:
            return render_template('login.html', title='Signing in',
                                   form=form, invalid=True)
        return redirect("/index")


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/registry', methods=['GET', 'POST'])
def registry():
    form = RegistryForm()
    user_name = form.username.data
    password = form.password.data
    confirm_password = form.confirm_password.data
    exists = user_model.user_exists(user_name)
    if request.method == 'GET':
        return render_template('registry.html', title='Signing up', form=form)
    else:
        if exists[0]:
            return render_template('registry.html', title='Signing up', form=form,
                                   exists=True)
        else:
            if password != confirm_password:
                return render_template('registry.html', title='Signing up', form=form,
                                       invalid=True)
            else:
                user_model.insert(user_name, password)
                exists = user_model.user_exists(user_name)
                session['username'] = user_name
                session['user_id'] = exists[1]
                return redirect('/index')


@app.route("/carts")
def carts():
    carts = carts_model.get(session['user_id'])
    return render_template('carts.html', username=session['username'],
                           carts=carts, product=None, registered=True)


@app.route("/add_basket/<int:product_id>")
def add_basket(product_id, c=1):
    item = product_model.get(product_id)
    if product_model.check_reserv(product_id):
        product_model.change_reserv(product_id, 1)
        carts_model.change_reserv(product_id, 1, session['user_id'])
        if not carts_model.exists(session['user_id'], product_id):
            carts_model.insert(session['user_id'], product_id, item[1], c, item[3], c * item[3])
            return redirect("/carts")
        return redirect("/carts")
    return redirect('/index')


@app.route("/delete_from_carts/<int:cart_id>", methods=['GET'])
def delete_from_basket(cart_id):
    product_id = carts_model.get_by_id(cart_id)
    product_id = product_id[0][2]
    product_model.change_reserv(product_id, -1)
    carts_model.delete_from_carts(cart_id)
    return redirect("/carts")


@app.route('/buy')
def buy():
    n = carts_model.get(session['user_id'])
    for i in n:
        product_model.buy(i[2], i[4])
        product_model.reserv(i[2])
    carts_model.delete(session['user_id'])
    return render_template('buy.html', username=session['username'])


if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=True)
