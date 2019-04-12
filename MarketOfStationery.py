from flask import Flask, render_template, redirect, request, session, jsonify, make_response
from forms import LoginForm, RegistryForm
from db import DB, UserModel, CartsModel, ProductModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stationery'
db = DB()


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    product = ProductModel(db.get_connection()).get_all()
    return render_template('index.html', username=session['username'],
                           product=product, title='Store', registered=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
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
    user_model = UserModel(db.get_connection())
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


@app.route("/carts/<user>")
def carts(user):
    carts = CartsModel(db.get_connection()).get_all()
    return render_template('carts.html', username=user,
                           carts=carts, product=None, registered=True)


@app.route("/carts/<user>/add_to_basket/<int:product_id>")
def add_basket(user, product_id):
    product_model = ProductModel(db.get_connection())
    item = product_model.get(product_id)
    carts_model = CartsModel(db.get_connection())
    carts_model.insert(user, product_id, item[1], item[2], item[3], item[2] * item[3])
    return redirect(f"/carts/{user}")


@app.route("/carts/<user>/delete_from_cart/<int:id>", methods=['GET'])
def delete_from_basket(user, id):
    carts = CartsModel(db.get_connection())
    carts.delete_from_carts(id)
    return redirect(f"/carts/{user}")


@app.route("/carts/<user>/buy")
def buy(user):
    carts = CartsModel(db.get_connection())
    carts.delete(user)
    return redirect(f'/carts/{user}')


if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=True)
