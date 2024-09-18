# app/forms.py

from flask_wtf import FlaskForm  # Import FlaskForm to create forms
from wtforms import StringField, PasswordField, SubmitField  # Import different field types for forms
from wtforms.validators import DataRequired, Email, EqualTo, Length  # Validators to ensure form data meets requirements
from wtforms import TextAreaField  # Import TextAreaField to handle larger text inputs

# Registration form for new users
class RegistrationForm(FlaskForm):
    # Username field with data required and length validation
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])  
    # Email field with required and email format validation
    email = StringField('Email', validators=[DataRequired(), Email()])  
    # Password field with required validation and a minimum length of 6 characters
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])  
    # Confirm password field, ensuring it matches the password field
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  
    # Submit button for the form
    submit = SubmitField('Sign Up')

# Login form for existing users
class LoginForm(FlaskForm):
    # Username field with data required validation
    username = StringField('Username', validators=[DataRequired()])  
    # Password field with data required validation
    password = PasswordField('Password', validators=[DataRequired()])  
    # Submit button for the form
    submit = SubmitField('Login')

# Form for creating and editing posts
class PostForm(FlaskForm):
    # Title field for the post with required validation and a length constraint
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])  
    # Content field for the post with required validation
    content = TextAreaField('Content', validators=[DataRequired()])  
    # Submit button for the form
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Reply', validators=[DataRequired()])  # Content for the comment
    submit = SubmitField('Post Reply')  # Submit button