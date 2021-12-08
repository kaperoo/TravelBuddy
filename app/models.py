from app import db, loginManager
from flask_login import UserMixin


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

visitors = db.Table('visitors',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'))
)

futureVisitors = db.Table('futureVisitors',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'))
)

class User(db.Model, UserMixin):

    #   Unique ID of each user
    id = db.Column(db.Integer, primary_key=True)
    #   Name of the user
    name = db.Column(db.String(64),nullable=False)
    #   Unique username of each user
    username = db.Column(db.String(20), unique=True, nullable=False)
    #   Password of each user
    password = db.Column(db.String(60), nullable=False)
    #   Email of each user
    email = db.Column(db.String(120), unique=True, nullable=False)
    #   Boolean which stores whether user is admin or not
    isAdmin = db.Column(db.Boolean, default=False)
    #   Profile picture of the user
    profilePicture = db.Column(db.String(20), nullable=False, default='default.jpg')

    country = db.Column(db.Integer, db.ForeignKey('country.id'))
    visitedCountries = db.relationship('Country', secondary = visitors, backref=db.backref('visitors'), lazy='dynamic')
    bucketList = db.relationship('Country', secondary = futureVisitors, backref=db.backref('futureVisitors'), lazy='dynamic')

class Country(db.Model):

    #   Unique ID of each country
    id = db.Column(db.Integer, primary_key=True)
    #   Name of each country
    name = db.Column(db.String(50), unique=True, nullable=False)
    #   Capital of each country
    capital = db.Column(db.String(20), nullable=False)
    #   Coordinates of country capital
    lat = db.Column(db.String(120))
    lang = db.Column(db.String(120))
    #   Language spoken in this country
    language = db.Column(db.String(120), nullable=False)
    #   Currency of this country
    currency = db.Column(db.String(20), nullable=False)

    citizens = db.relationship('User', backref='livesin', lazy='dynamic')