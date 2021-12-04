from flask import render_template, flash, redirect, request
from app import app, db, models, admin
from .forms import TaskForm

from datetime import datetime, timedelta, date
from flask_admin.contrib.sqla import ModelView 

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

#   A page where the user can add a new assignment
@app.route('/addTask', methods=['GET', 'POST'])
def addTask():

    #   create an instance of the form from forms.py file
    form = TaskForm()

    #   If form is submited and it is valid take an action
    if form.validate_on_submit():
        
        #   Assign data from the form to the instance of an object in db
        task = models.CheckList(moduleCode=form.moduleCode.data,
                                title=form.title.data,
                                description=form.description.data,
                                deadline=form.deadline.data,
                                isDone=form.isDone.data)

        try:
            #   try to update the db and return to main page
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    
    #   to change the active button at the top of the page
    active = ["","","","active"]
        
    #   render the add task page
    return render_template('addTask.html',
                           title='Add Task',
                           form=form,
                           active=active)

#   A page for displaying all the completed assignments


