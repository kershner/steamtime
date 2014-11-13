from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#############################################
# SteamTime forms

class SteamTime(Form):
    steamid = StringField('SteamID', validators=[DataRequired('Enter Your SteamID')])
    submit = SubmitField('Submit')