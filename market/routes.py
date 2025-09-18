from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages, request
from market import app
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellingForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['Get', 'POST'])
@login_required
def market_page():
    purchase_form=PurchaseForm()
    selling_form=SellingForm()
    #if purchase_form.validate_on_submit():
    #    print(request.form.get('purchased_item'))
    if request.method=="POST":
        #purchase 
        purchased_item=request.form.get('purchased_item')
        p_item_object=Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                
                p_item_object.owner=current_user.id
                current_user.budget -= p_item_object.price
                db.session.commit()
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}", category='success')
            else:
                flash("Unfortunately, you don't have enough money", category='danger')
        
        #selling
        sold_item=request.form.get('sold_item')
        s_item_object=Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                
                s_item_object.owner=None
                current_user.budget += s_item_object.price
                db.session.commit()
                flash(f"Congratulations! You sold {s_item_object.name} for {s_item_object.price}", category='success')
            else:
                flash("Unfortunately, you don't have this item", category='danger')
        
        return redirect(url_for('market_page'))
    if request.method=="GET":
        items=Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items,purchase_form=purchase_form, selling_form=selling_form, owned_items=owned_items)

@app.route("/register", methods=['Get', 'POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Register successfully! Now you are logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors !={}:  
        #if there are no errors from validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Username and password are not match! Please try agian', category='danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for("home_page"))
