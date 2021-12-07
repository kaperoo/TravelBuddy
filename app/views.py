import secrets, os
from PIL import Image
from flask import render_template, flash, redirect, request, url_for
from werkzeug.wrappers import ResponseStreamMixin
from app import app, db, models, admin, bcrypt
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm

from flask_admin.contrib.sqla import ModelView 
from flask_login import login_user, current_user, logout_user, login_required
from .models import User, Country
import json

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

    imageFile = url_for('static', filename='flags/' + c.name + '.png')
    #   render the country page
    return render_template('country.html',
                            title=c.name,
                            c=c,
                            imageFile=imageFile)

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

def savePicture(formPicture):
    randomHex = secrets.token_hex(8)
    _, fExt = os.path.splitext(formPicture.filename)
    pictureName = randomHex + fExt
    picturePath = os.path.join(app.root_path, 'static/profilepics', pictureName)
    
    outputSize = (250, 250)
    i = Image.open(formPicture)

    width, height = i.size
    # crop the image to the center square
    if width > height:
        i = i.crop(((width-height)/2, 0, (width+height)/2, height))
    elif height > width:
        i = i.crop((0, (height-width)/2, width, (height+width)/2))

    i.thumbnail(outputSize)
    i.save(picturePath)
    
    if current_user.profilePicture != 'default.jpg':
        prevPicture = os.path.join(app.root_path, 'static/profilepics', current_user.profilePicture)
        if os.path.exists(prevPicture):
            os.remove(prevPicture)

    return pictureName    

#   A page where the user can update their profile
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()
    passForm = ChangePasswordForm()

    #   if the update profile form is submitted
    if form.validate_on_submit():
        if form.picture.data:
            pictureFile = savePicture(form.picture.data)
            current_user.profilePicture = pictureFile

        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect('/account')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email
    
    #   Password change
    if passForm.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, passForm.oldPassword.data):
            if passForm.newPassword.data == passForm.confirmPassword.data:
                hashed_password = bcrypt.generate_password_hash(passForm.newPassword.data).decode('utf-8')
                current_user.password = hashed_password
                db.session.commit()
                flash('Your password has been updated!', 'success')
                return redirect('/account')
            else:
                flash('The passwords do not match!', 'danger')
        else:
            flash('The old password is incorrect!', 'danger')

    imageFile = url_for('static', filename='profilepics/' + current_user.profilePicture)
    return render_template('account.html',
                           title='Your Account',
                           imageFile=imageFile,
                           form=form,
                           passForm=passForm)

#   A users profile page
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):

    u = User.query.filter_by(username=username).first()

    if u == current_user:
        return redirect('/account')

    imageFile = url_for('static', filename='profilepics/' + u.profilePicture)
    #   render the profile page
    return render_template('profile.html',
                            title=u.username,
                            u=u,
                            imageFile=imageFile)

@app.route('/respond', methods=['POST'])
def respond():
    # Parse the JSON data included in the request
    data = json.loads(request.data)
    response = data.get('response')
    ctry = data.get('country')

    currCountry = Country.query.filter_by(name=ctry).first()

    if current_user.is_authenticated:
        if response == 'v1' and currCountry in current_user.visitedCountries:
            current_user.visitedCountries.remove(currCountry)
        elif response == 'v2' and currCountry not in current_user.visitedCountries:
            current_user.visitedCountries.append(currCountry)
        elif response == 'b1' and currCountry in current_user.bucketList:
            current_user.bucketList.remove(currCountry)
        elif response == 'b2' and currCountry not in current_user.bucketList:
            current_user.bucketList.append(currCountry)
        elif response == 'l1' and current_user in currCountry.citizens:
            currCountry.citizens.remove(current_user)
        elif response == 'l2' and current_user not in currCountry.citizens:
            currCountry.citizens.append(current_user)

        db.session.commit()

    return json.dumps({'status': 'OK', 'response': response, 'ctry':ctry, 'username':current_user.username})

@app.route('/ctryrmv', methods=['POST'])
def ctryrmv():
    # Parse the JSON data included in the request
    data = json.loads(request.data)
    response = data.get('response')
    col = data.get('list')

    country = Country.query.filter_by(name=response).first()

    if current_user.is_authenticated:
        if col == 'vs' and country in current_user.visitedCountries:
            current_user.visitedCountries.remove(Country.query.filter_by(name=response).first())
        elif col == 'bs' and country in current_user.bucketList:
            current_user.bucketList.remove(Country.query.filter_by(name=response).first())
        elif col == 'ls' and current_user in country.citizens:
            Country.query.filter_by(name=response).first().citizens.remove(current_user)

        db.session.commit()

    return json.dumps({'status': 'OK', 'response': response, 'col':col})