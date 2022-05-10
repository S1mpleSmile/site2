from shop import app, db
from flask import render_template, redirect, url_for, flash, request
from shop.models import Product, User
from shop.forms import RegistrationForm, LoginForm, BuyForm, SellForm, EditForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/shop", methods=['GET', 'POST'])
@login_required
def shop_page():
    buy_form = BuyForm()
    sell_form = SellForm()

    if request.method == 'POST':
        purchased_product = request.form.get('purchased_product')
        purchased_product_obj = Product.query.filter_by(name=purchased_product).first()
        if purchased_product_obj:
            if current_user.can_buy(purchased_product_obj):
                purchased_product_obj.buy(current_user)
                flash(f"You bought { purchased_product_obj.name } for { purchased_product_obj.price }₽.",
                      category='success')
            else:
                flash(f'Your budget is not enough to make this purchase {purchased_product_obj.name}.',
                      category='danger')

        sold_product = request.form.get('sold_product')
        sold_product_obj = Product.query.filter_by(name=sold_product).first()
        if sold_product_obj:
            if current_user.can_sell(sold_product_obj):
                sold_product_obj.sell(current_user)
                flash(f"You sold { sold_product_obj.name } for { sold_product_obj.price }₽.",
                      category='success')
            else:
                flash(f'You can not sell {sold_product_obj.name}.',
                      category='danger')

        return redirect(url_for('shop_page'))

    if request.method == "GET":
        products = Product.query.filter_by(owner=None)
        owned_products = Product.query.filter_by(owner=current_user.id)

        return render_template("shop.html", products=products, buy_form=buy_form,
                               owned_products=owned_products, sell_form=sell_form)


@app.route("/registration", methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()

    if form.validate_on_submit():
        create_user = User(username=form.username.data,
                           email=form.email.data,
                           password=form.password.data)

        db.session.add(create_user)
        db.session.commit()

        login_user(create_user)
        flash(f'Registration completed successfully. You are logged in as {create_user.username}.', category='success')

        return redirect(url_for('shop_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(f'Registration error: {error}', category='danger')

    return render_template("registration.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempt_user = User.query.filter_by(username=form.username.data).first()

        if attempt_user and attempt_user.correct_password(
           attempt_password=form.password.data):
            login_user(attempt_user)
            flash(f'You are logged in as {attempt_user.username}', category='success')

            return redirect(url_for('shop_page'))
        else:
            flash('The username or password does not match. Try again.', category="danger")

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f"You are logged out of your account", category='info')

    return redirect(url_for("home_page"))


@app.route('/change_profile', methods=['GET', 'POST'])
@login_required
def user_page():
    form = EditForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.', category='success')
        return redirect(url_for('shop_page'))
    else:
        cond1 = current_user.username == form.username.data
        cond2 = current_user.email == form.email.data

        if cond1 or cond2:
            if cond1 and cond2:
                flash('The entered name is the current name. No changes have been made.', category='info')
                flash('The entered email is the current email. No changes have been made.', category='info')
            elif cond1:
                flash('The entered name is the current name. No changes have been made.', category='info')
            else:
                flash('The entered email is the current email. No changes have been made.', category='info')
        elif form.errors != {}:
            for error in form.errors.values():
                flash(f'Registration error: {error}', category='danger')

    return render_template('change_profile.html', title='Change Profile', form=form)

#@app.route('cart')
#def list():
    #return render_template('cart.html')

