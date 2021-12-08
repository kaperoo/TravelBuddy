from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import logging

# Create the application instance
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Initialize Flask Extensions
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category = 'info'

# Configure logging
app.logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(name)s: %(message)s')
file_handler = logging.FileHandler('logfile.log')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

# Configure admin view
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.isAdmin
        else:
            return False

migrate = Migrate(app, db, render_as_batch=True)

admin = Admin(app,template_mode='bootstrap3',index_view=MyAdminIndexView())

from app import views
from app import models
