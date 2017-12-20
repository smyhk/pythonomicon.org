from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length

'''
Define form elements
'''


class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=9, max=80)])
    # remember = BooleanField("remember")
    submit = SubmitField("Sign in")


class SignupForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=50)])
    email = StringField("email", validators=[InputRequired(),
                                             Email(message="Invalid email"),
                                             Length(max=80)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=9, max=80)])
    submit = SubmitField("Create account")


class NewPostForm(FlaskForm):
    title = StringField("title", validators=[InputRequired(), Length(min=1, max=256)])
    subtitle = StringField("subtitle", validators=[InputRequired(), Length(min=1, max=256)])
    content = TextAreaField("subtitle", validators=InputRequired())
    submit = SubmitField("Publish")
