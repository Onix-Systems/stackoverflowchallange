from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class UserIdForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
