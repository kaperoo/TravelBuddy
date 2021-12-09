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
    try:
        countries = Country.query.order_by(models.Country.name).all()
    except Exception as e:
        app.logger.error("Route / failed to execute error= %s",e)
    #   render the main page
    return render_template('index.html',
                           title='Travel Buddy',
                           countries=countries)

#   Page of the country
@app.route('/country/<country>', methods=['GET', 'POST'])
def country(country):
    #   get the country from the database
    try:
        c = Country.query.filter_by(name=country).first()

        imageFile = url_for('static', filename='flags/' + c.name + '.png')
    except Exception as e:
        app.logger.error('Route /country failed to execute error= %s',e)
    
    #   render the country page
    return render_template('country.html',
                            title=c.name,
                            c=c,
                            imageFile=imageFile)

#   A page where the user can register
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if current_user.is_authenticated:
            return redirect('/')
        #   create an instance of the form from forms.py file
        form = RegistrationForm()

        #   if the form is valid
        if form.validate_on_submit():
            #   create a new user
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, name=form.name.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            # show the success message
            flash('Your account has been created! You can now sign in'.format(form.username.data), 'success')
            #   redirect to the login page and log the event
            app.logger.info('User {} has been created'.format(form.username.data))
            return redirect('/login')
    except Exception as e:
        #  log the error
        app.logger.error('Route /register failed to execute error= %s',e)

    #   render the register page
    return render_template('register.html',
                           title='Register',
                           form=form)

#   A page where the user can login
@app.route('/login', methods=['GET', 'POST'])
def login():

    try:
        if current_user.is_authenticated:
            return redirect('/')
        #   create an instance of the form from forms.py file
        form = LoginForm()

        if form.validate_on_submit():
            #   get the user from the database
            user = User.query.filter_by(email=form.email.data).first()

            #   check if the password is correct
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                #   log the user in
                login_user(user, remember=form.remember.data)
                # log the event
                app.logger.info('%s logged in', user.username)
                next_page = request.args.get('next')
                # show the success message
                flash('You have been logged in!', 'success')
                return redirect(next_page) if next_page else redirect('/')
            else:    
                # show the error message
                app.logger.info('%s (email) failed to login',form.email.data)
                flash('Login Unsuccessful. Please check email and password', 'danger')
    except Exception as e:
        #  log the error
        app.logger.error('Route "/login" failed to execute error="%s"',e)

    #   render the login page
    return render_template('login.html',
                           title='Login',
                           form=form)

@app.route('/logout')
@login_required
def logout():
    # logout the user
    app.logger.info('%s logged out', current_user.username)
    logout_user()
    # show the success message
    flash('You have been logged out!', 'success')
    return redirect('/')

def savePicture(formPicture):
    #   create a random string
    randomHex = secrets.token_hex(8)
    #   get the extension of the picture
    _, fExt = os.path.splitext(formPicture.filename)
    #   create a new name for the picture
    pictureName = randomHex + fExt
    #   create a path to the picture
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
    
    # remove the old picture
    if current_user.profilePicture != 'default.jpg':
        prevPicture = os.path.join(app.root_path, 'static/profilepics', current_user.profilePicture)
        if os.path.exists(prevPicture):
            os.remove(prevPicture)

    return pictureName    

#   A page where the user can update their profile
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    try:
        form = UpdateAccountForm()
        passForm = ChangePasswordForm()

        #   if the update profile form is submitted
        if form.validate_on_submit():
            if form.picture.data:
                pictureFile = savePicture(form.picture.data)
                current_user.profilePicture = pictureFile

            #   update the user's profile
            current_user.username = form.username.data
            current_user.name = form.name.data
            current_user.email = form.email.data
            db.session.commit()
            # log the event
            app.logger.info('%s updated their profile', current_user.username)
            # show the success message
            flash('Your account has been updated!', 'success')
            return redirect('/account')
        elif request.method == 'GET':
            #   populate the form with the current user's data
            form.username.data = current_user.username
            form.name.data = current_user.name
            form.email.data = current_user.email
        
        #   Password change
        if passForm.validate_on_submit():
            #   check if the old password is correct
            if bcrypt.check_password_hash(current_user.password, passForm.oldPassword.data):
                #   update the password
                if passForm.newPassword.data == passForm.confirmPassword.data:
                    hashed_password = bcrypt.generate_password_hash(passForm.newPassword.data).decode('utf-8')
                    current_user.password = hashed_password
                    db.session.commit()
                    # log the event
                    app.logger.info('%s changed their password', current_user.username)
                    # show the success message
                    flash('Your password has been updated!', 'success')
                    return redirect('/account')
                else:
                    # show the error message
                    flash('The passwords do not match!', 'danger')
            else:
                # show the error message
                flash('The old password is incorrect!', 'danger')

        # get the user's profile picture
        imageFile = url_for('static', filename='profilepics/' + current_user.profilePicture)
    except Exception as e:
        #  log the error
        app.logger.error('Route "/account" failed to execute error="%s"',e)
    
    #   render the account page
    return render_template('account.html',
                           title='Your Account',
                           imageFile=imageFile,
                           form=form,
                           passForm=passForm)

#   A users profile page
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):

    try:
        #   get the user from the database
        u = User.query.filter_by(username=username).first()

        if u == current_user:
            return redirect('/account')

        #   get the user's profile picture
        imageFile = url_for('static', filename='profilepics/' + u.profilePicture)
    except Exception as e:
        #  log the error
        app.logger.error('Route "/profile/<username>" failed to execute error="%s"',e)
    
    #   render the profile page
    return render_template('profile.html',
                            title=u.username,
                            u=u,
                            imageFile=imageFile)

@app.route('/respond', methods=['POST'])
def respond():

    try:
        # Parse the JSON data included in the request
        data = json.loads(request.data)
        response = data.get('response')
        ctry = data.get('country')

        #   get the country from the database
        currCountry = Country.query.filter_by(name=ctry).first()

        # check if user is authenticated
        if current_user.is_authenticated:
            #check the response
            if response == 'v1' and currCountry in current_user.visitedCountries:
                #   remove the country from the user's visited countries
                current_user.visitedCountries.remove(currCountry)
                # log the event
                app.logger.info('%s removed %s from their visited countries', current_user.username, currCountry.name)
            elif response == 'v2' and currCountry not in current_user.visitedCountries:
                #   add the country to the user's visited countries
                current_user.visitedCountries.append(currCountry)
                # log the event
                app.logger.info('%s added %s to their visited countries', current_user.username, currCountry.name)
            elif response == 'b1' and currCountry in current_user.bucketList:
                #   remove the country from the user's bucket list
                current_user.bucketList.remove(currCountry)
                # log the event
                app.logger.info('%s removed %s from their bucket list', current_user.username, currCountry.name)
            elif response == 'b2' and currCountry not in current_user.bucketList:
                #   add the country to the user's bucket list
                current_user.bucketList.append(currCountry)
                # log the event
                app.logger.info('%s added %s to their bucket list', current_user.username, currCountry.name)
            elif response == 'l1' and current_user in currCountry.citizens:
                #   remove the user from the country's citizens
                currCountry.citizens.remove(current_user)
                # log the event
                app.logger.info('%s removed his home country (%s)', current_user.username, currCountry.name)
            elif response == 'l2' and current_user not in currCountry.citizens:
                #   add the user to the country's citizens
                currCountry.citizens.append(current_user)
                # log the event
                app.logger.info('%s added his home country (%s)', current_user.username, currCountry.name)

            db.session.commit()
    except Exception as e:
        #  log the error
        app.logger.error('Route "/respond" failed to execute error="%s"',e)
        
    #  return a response
    return json.dumps({'status': 'OK', 'response': response, 'ctry':ctry, 'username':current_user.username})

@app.route('/ctryrmv', methods=['POST'])
def ctryrmv():
    try:
        # Parse the JSON data included in the request
        data = json.loads(request.data)
        response = data.get('response')
        col = data.get('list')

        #   get the country from the database
        country = Country.query.filter_by(name=response).first()

        if current_user.is_authenticated:
            if col == 'vs' and country in current_user.visitedCountries:
                #   remove the country from the user's visited countries
                current_user.visitedCountries.remove(Country.query.filter_by(name=response).first())
                app.logger.info('%s removed %s from their bucket list', current_user.username, country.name)
            elif col == 'bs' and country in current_user.bucketList:
                #   remove the country from the user's bucket list
                current_user.bucketList.remove(Country.query.filter_by(name=response).first())
                app.logger.info('%s removed %s from their bucket list', current_user.username, country.name)
            elif col == 'ls' and current_user in country.citizens:
                #   remove the user from the country's citizens
                app.logger.info('%s removed his home country (%s)', current_user.username, country.name)
                Country.query.filter_by(name=response).first().citizens.remove(current_user)

            db.session.commit()
    except Exception as e:
        #  log the error
        app.logger.error('Route "/ctryrmv" failed to execute error="%s"',e)

    return json.dumps({'status': 'OK', 'response': response, 'col':col})

@app.route('/coords', methods=['POST'])
def coords():
    try:
        # Parse the JSON data included in the request
        data = json.loads(request.data)
        response = data.get('response')

        #   get the country from the database
        country = Country.query.filter_by(name=response).first()

        # get the coordinates of the country and the capital
        lat = country.lat
        lang = country.lang
        city = country.capital

    except Exception as e:
        #  log the error
        app.logger.error('Route "/coords" failed to execute error="%s"',e)

    #  return a response
    return json.dumps({'status': 'OK', 'response': response, 'lat':lat, 'lang':lang, 'city':city})

@app.route('/about')
def about():
    return render_template('about.html', title='About')