from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField, SubmitField, BooleanField
from wtforms.validators import  DataRequired, Length,Email, EqualTo, ValidationError
from flaskblog.models import User

# registration form class controller
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                       validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    #custom username and email validation
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.Please choose a different one')


# login form controller
class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

# Update the account form controller
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                       validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    # Allowed image files
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')
    #custom username and email validation
    def validate_username(self, username):
        #Update only if username is different that the one that exists in the database
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.Please choose a different one')

    def validate_email(self, email):
        # Update only if email is different that the one that exists in the database
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.Please choose a different one')

