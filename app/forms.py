from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

# Registration form
class RegistrationForm(FlaskForm):
	# Username field with validators (DataRequired, Length)
	username = StringField('Username', 
								validators=[DataRequired(), 
								Length(min=4,max=20,message='Invalid Username Length')])
	# Email field with validators (DataRequired, Email)
	email = StringField('Email', 
							validators=[DataRequired(),
							Email()])
	# Password field with validators (DataRequired, Length)
	password = PasswordField('Password',
								validators=[DataRequired()])
	# name field with validators (DataRequired, Length)
	name = StringField('Name',
							validators=[DataRequired(),
							Length(min=1,max=64,message='Invalid Username Length')])
	# confirm password field with validators (DataRequired, EqualTo)
	confirm_password = PasswordField('Confirm Password',
										validators=[DataRequired(),
										EqualTo('password',message='Passwords must match')])

	submit = SubmitField('Sign Up')

	# function to check if username is already in use
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already taken')

	# function to check if email is already in use
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already in use')

# Login form
class LoginForm(FlaskForm):
	# Email field with validators (DataRequired, Email)
	email = StringField('Email', 
							validators=[DataRequired(),
							Email()])
	# Password field with validators (DataRequired)
	password = PasswordField('Password',
								validators=[DataRequired()])
	# remember me field with validators (BooleanField)
	remember = BooleanField('Remember Me')

	submit = SubmitField('Login')

# Update Account form
class UpdateAccountForm(FlaskForm):
	# Username field with validators (DataRequired, Length)
	username = StringField('Username', 
								validators=[DataRequired(), 
								Length(min=4,max=20,message='Invalid Username Length')])
	# Email field with validators (DataRequired, Email)
	email = StringField('Email', 
							validators=[DataRequired(),
							Email()])
	# name field with validators (DataRequired, Length)
	name = StringField('Name',
							validators=[DataRequired(),
							Length(min=1,max=64,message='Invalid Username Length')])
	# picture field with validators (FileAllowed)
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

	submit = SubmitField('Update')

	# function to check if username is already in use
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already taken')

	# function to check if email is already in use
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already in use')

# Request Reset Password form
class ChangePasswordForm(FlaskForm):
	# Password field with validators (DataRequired)
	oldPassword = PasswordField('Old Password',
								validators=[DataRequired()])
	# New Password field with validators (DataRequired)
	newPassword = PasswordField('New Password',
								validators=[DataRequired()])
	# Confirm Password field with validators (DataRequired, EqualTo)
	confirmPassword = PasswordField('Confirm Password',
										validators=[DataRequired(),
										EqualTo('newPassword',message='Passwords must match')])
	submit = SubmitField('Change Password')