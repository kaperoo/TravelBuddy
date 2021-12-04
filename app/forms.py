from flask_wtf import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms.validators import Length

#	Form that the uset completes in order to create a new task/assignment
class TaskForm(Form):

	#	A field to enter the module code with restricted length of 8 characters
	moduleCode = StringField('Module Code:', 
								validators=[DataRequired(), 
								Length(min=8,max=8,message='Invalid Module Code')])

	#	A field to enter the title of the assignment (max 20 characters)
	title = StringField('Assignment Title:', 
							validators=[DataRequired(), 
							Length(max=20,message='Invalid Module Code')])

	#	Textfield to save the description of the task
	description = TextAreaField('Assignment Description:', 
									validators=[DataRequired()])

	#	The deadline of the assignment. Calendar widget to choose the date from
	deadline = DateField('Deadline:', format='%Y-%m-%d')

	#	Is the assignment already done (checkbox)
	isDone = BooleanField('Is it already completed?')

class SignInForm(Form):

	#	A field to enter the module code with restricted length of 8 characters
	username = StringField('Username:', 
								validators=[DataRequired(), 
								Length(min=8,max=8,message='Invalid Module Code')])

	#	A field to enter the title of the assignment (max 20 characters)
	title = StringField('Assignment Title:', 
							validators=[DataRequired(), 
							Length(max=20,message='Invalid Module Code')])

	#	Textfield to save the description of the task
	description = TextAreaField('Assignment Description:', 
									validators=[DataRequired()])

	#	The deadline of the assignment. Calendar widget to choose the date from
	deadline = DateField('Deadline:', format='%Y-%m-%d')

	#	Is the assignment already done (checkbox)
	isDone = BooleanField('Is it already completed?')