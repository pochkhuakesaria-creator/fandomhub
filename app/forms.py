from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length
)



# REGISTER

class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3)
        ]
    )


    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )


    submit = SubmitField(
        "Register"
    )





# LOGIN

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )


    submit = SubmitField(
        "Login"
    )






# ADD FANDOM

class FandomForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired()]
    )


    category = StringField(
        "Category",
        validators=[DataRequired()]
    )


    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )


    image = StringField(
        "Image URL",
        validators=[DataRequired()]
    )


    submit = SubmitField(
        "Add Fandom"
    )


# POST

class PostForm(FlaskForm):

    text = TextAreaField(
        "Post",
        validators=[
            DataRequired()
        ]
    )


    submit = SubmitField(
        "Post"
    )