from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField, TextField
from wtforms.validators import InputRequired, Email, DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.widgets import TextArea


class SignUpForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    gender=SelectField('Gender', choices=[('Female','Female'), ('Male','Male')])
    location = StringField('Location', validators=[InputRequired()])
    image = FileField('Profile Picture',validators=[FileRequired(),FileAllowed(['jpg','png'])])
    email = StringField('Email', validators = [Email(message ='Invalid email'), InputRequired()])
    bib=TextField('Biography', validators=[InputRequired()], widget=TextArea())
    
class SendID(FlaskForm):
    myid = HiddenField('', validators=[InputRequired()])
