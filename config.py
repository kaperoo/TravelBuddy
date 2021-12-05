import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'd18de0288d54c1f9bc346ee8b349375e'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
