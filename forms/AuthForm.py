import re

# from flask_marshmallow import Marshmallow
from wtforms import Form, PasswordField, StringField
from wtforms.fields.core import DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

# ma = Marshmallow()


# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'username', 'first_name', 'last_name',
#                   'email', 'password', 'contact_no', 'address', 'city')


class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )
    password = StringField(
        'Password',
        validators=[
            DataRequired(),
            Regexp(
                re.compile(
                    r'^.*(?=.{8})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*()_+={}?:~\[\]]+$')
            )
        ])


class UserForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Regexp(
                r'^.*(?=.{8})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*()_+={}?:~\[\]]+$'
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    first_name = StringField(
        'First name',
        validators=[
            DataRequired()
        ]
    )
    last_name = StringField(
        'Last name',
        validators=[
            DataRequired()
        ]
    )
    contact_no = StringField(
        'Contact no.'
    )
    address = StringField('Address')
    city = StringField('City')
    dob = DateTimeField(
        'Date of Birth',
        format='%d-%m-%y',
        validators=[DataRequired()]
    )
    role = StringField('Role', validators=[DataRequired()])


class StudentForm(UserForm):
    pass


class AdminForm(UserForm):
    pass


class TeacherForm(UserForm):

    degree = StringField('Degree')
    exp = StringField('Experience')
