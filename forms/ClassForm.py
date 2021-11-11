from wtforms import Form, IntegerField, StringField
from wtforms.validators import DataRequired, Length


class ClassForm(Form):
    name = StringField(
        'name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    no_of_students = IntegerField(
        'no_of_students',
        validators=[
            DataRequired()
        ]
    )
    image = StringField('Image')
