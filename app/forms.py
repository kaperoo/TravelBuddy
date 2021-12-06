from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(Form):
	username = StringField('Username', 
								validators=[DataRequired(), 
								Length(min=4,max=20,message='Invalid Username Length')])

	email = StringField('Email', 
							validators=[DataRequired(),
							Email()])

	password = PasswordField('Password',
								validators=[DataRequired()])

	name = StringField('Name',
							validators=[DataRequired(),
							Length(min=1,max=64,message='Invalid Username Length')])

	confirm_password = PasswordField('Confirm Password',
										validators=[DataRequired(),
										EqualTo('password',message='Passwords must match')])

	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already taken')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already in use')

class LoginForm(Form):
	email = StringField('Email', 
							validators=[DataRequired(),
							Email()])

	password = PasswordField('Password',
								validators=[DataRequired()])

	remember = BooleanField('Remember Me')

	submit = SubmitField('Login')

class UpdateAccountForm(Form):
	username = StringField('Username', 
								validators=[DataRequired(), 
								Length(min=4,max=20,message='Invalid Username Length')])

	email = StringField('Email', 
							validators=[DataRequired(),
							Email()])

	name = StringField('Name',
							validators=[DataRequired(),
							Length(min=1,max=64,message='Invalid Username Length')])

	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already taken')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already in use')

class ChangePasswordForm(Form):


	oldPassword = PasswordField('Old Password',
								validators=[DataRequired()])

	newPassword = PasswordField('New Password',
								validators=[DataRequired()])

	confirmPassword = PasswordField('Confirm Password',
										validators=[DataRequired(),
										EqualTo('newPassword',message='Passwords must match')])
	submit = SubmitField('Change Password')