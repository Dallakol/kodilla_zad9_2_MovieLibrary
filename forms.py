from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    Title = StringField('Title', validators=[DataRequired()])
    Description = StringField('Description', validators=[DataRequired()])
    Rating = SelectField('Rating', choices=range(1,11), validators=[DataRequired()])
    Time = StringField('Tine', validators=[DataRequired()])