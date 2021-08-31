from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from logger import trace, exc
from wtforms import (
    validators,
    SubmitField,
    StringField,
    BooleanField
)


class FilterForm(FlaskForm):
    try:
        trace.info('Initialised for filter model')
        startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
        enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
        chronological = BooleanField('Chronological')
        submit = SubmitField('Submit')
    except Exception as err:
        exc.exception(f'Error in Model generation for filter page: {err}')
        print(f'Error in Model generation for filter page: {err}')


class SearchForm(FlaskForm):
    try:
        trace.info('Initialised for serach form model')
        search = StringField('Search')
        submit = SubmitField('Search')
    except Exception as err:
        exc.exception(f'Error in serach form model: {err}')
        print(f'Error in serach form model: {err}')
