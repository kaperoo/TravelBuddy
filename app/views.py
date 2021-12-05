from flask import render_template, flash, redirect, request, url_for
from app import app, db, models, admin, bcrypt
from .forms import RegistrationForm, LoginForm

from datetime import datetime, timedelta, date
from flask_admin.contrib.sqla import ModelView 
from flask_login import login_user, current_user, logout_user, login_required
from .models import User, Country

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Country, db.session))

#   Main page/page with all assignments
@app.route('/', methods=['GET', 'POST'])
def index():

    # countries = Country.query.all()

    countries = Country.query.order_by(models.Country.name).all()

    #   render the main page
    return render_template('index.html',
                           title='Travel Buddy',
                           countries=countries)

#   Page of the country
@app.route('/country/<country>', methods=['GET', 'POST'])
def country(country):

    c = Country.query.filter_by(name=country).first()

    #   render the country page
    return render_template('country.html',
                            title=c.name,
                            c=c)

#   A page where the user can register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    #   create an instance of the form from forms.py file
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now sign in'.format(form.username.data), 'success')
        return redirect('/login')

    return render_template('register.html',
                           title='Register',
                           form=form)

#   A page where the user can login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    #   create an instance of the form from forms.py file
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect('/')
        else:    
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html',
                           title='Login',
                           form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/account')
@login_required
def account():
    return render_template('account.html',
                           title='Your Account')
