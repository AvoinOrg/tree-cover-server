from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class FileForm(FlaskForm):
    # name = StringField('Please upload your data as .csv file', validators=[DataRequired()])
    file = FileField(validators=[FileRequired()])
    submit = SubmitField("Submit")
