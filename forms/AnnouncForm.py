
from wtforms import Form,  StringField
from wtforms.validators import DataRequired


class AnnouncForm(Form):
    title = StringField(
        'Tilte',
        validators=[
            DataRequired()
        ]
    )
    description = StringField('Description')
