from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class StockForm(FlaskForm):
    ticker = StringField('Ticker', validators = [DataRequired()])
    quantity = IntegerField('Quantity', validators = [DataRequired()])
    submit = SubmitField('Add')
