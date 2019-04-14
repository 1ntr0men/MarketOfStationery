from flask import Flask, render_template, redirect, request, session, jsonify, make_response
from forms import LoginForm, RegistryForm, AddProductForm, CountForm
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
    form = CountForm()
    product = product_model.get_all()
    return render_template('index.html', username=session['username'],
                           product=product, title='Store', registered=True,
                           admin=user_model.is_admin(session['username']), form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    exists = user_model.exists(user_name, password)
    if request.method == 'GET':
        return render_template('login.html', title='Signing in', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if exists[0]:
                session['username'] = user_name
                session['user_id'] = exists[1]
                return redirect("/index")
            else:
                return render_template('login.html', title='Signing in', form=form,
                                       invalid=True)
        return render_template('login.html', title='Signing in', form=form)


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
        if form.validate_on_submit():
            if exists[0]:
                return render_template('registry.html', title='Signing up', form=form,
                                       exists=True)
            elif password != confirm_password:
                return render_template('registry.html', title='Signing up', form=form,
                                       invalid=True)
            user_model.insert(user_name, password, 0)
            exists = user_model.user_exists(user_name)
            session['username'] = user_name
            session['user_id'] = exists[1]
            return redirect('/index')
        return render_template('registry.html', title='Signing up', form=form)


@app.route("/carts")
def carts():
    carts = carts_model.get(session['user_id'])
    total = 0
    for i in carts:
        total += i[6]
    return render_template('carts.html', username=session['username'],
                           carts=carts, product=None, registered=True,
                           admin=user_model.is_admin(session['username']),
                           total=total)


@app.route("/add_basket/<int:product_id>/<int:c>")
def add_basket(product_id, c):
    item = product_model.get(product_id)
    print(item)
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
    return render_template('buy.html', username=session['username'],
                           registered=True, admin=user_model.is_admin(session['username']))


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    name = form.name.data
    count = form.count.data
    price = form.price.data
    if request.method == 'GET':
        return render_template('add_product.html', title='Signing in', form=form,
                               registered=True, admin=user_model.is_admin(session['username']))
    else:
        if form.validate_on_submit():
            return redirect(f"/add_product/{name}&{count}&{price}")
        return render_template('add_product.html', title='Signing in', form=form,
                               registered=True, admin=user_model.is_admin(session['username']))


@app.route('/add_product/<data>')
def new_product(data):
    name, count, price = data.split('&')
    product_model.insert(name, count, price, 0)
    return redirect('/index')


@app.route("/delete/<product_id>")
def delete(product_id):
    product_model.delete(product_id)
    carts_model.delete_by_product(product_id)
    return redirect("/index")


@app.route('/new_basket/<product_id>', methods=['GET', 'POST'])
def new_basket(product_id):
    item = product_model.get(product_id)
    form = CountForm()
    if request.method == 'GET':
        return render_template('new_basket.html',
                               admin=user_model.is_admin(session['username']),
                               registered=True, form=form, item=item)
    else:
        count = item[2] - item[4]
        input_count = form.count.data
        if form.validate_on_submit():
            if input_count > count:
                return render_template('new_basket.html',
                                       admin=user_model.is_admin(session['username']),
                                       registered=True, form=form, item=item,
                                       invalid=True)
            return redirect(f'/add_basket/{item[0]}/{input_count}')
        return render_template('new_basket.html',
                               admin=user_model.is_admin(session['username']),
                               registered=True, form=form, item=item)


if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=True)
