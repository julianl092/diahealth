from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()], description="First Name")
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    s_submit = SubmitField('Sign Up')

class QuestionForm(FlaskForm):
    question = TextAreaField("What's your question?", validators = [DataRequired()])
    submit = SubmitField('Submit your question') 

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
