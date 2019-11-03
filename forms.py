from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class StockForm(FlaskForm):
    ticker = StringField('Ticker', validators = [DataRequired()])
    quantity = IntegerField('Quantity', validators = [DataRequired()])
    submit = SubmitField('Add')

class GenreForm(FlaskForm):
    genre = SelectField('Genre')
    submit = SubmitField('Generate Playlist')
