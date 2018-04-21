from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import IntegerField, validators


class ScanDocumentForm(FlaskForm):
    filePdf = FileField(label="File",validators=[FileRequired(), FileAllowed(['pdf'], 'Pdf only!!')])
    file_range_min = IntegerField(validators=[validators.NumberRange(min=0, max=500)],label="Start")
    file_range_max = IntegerField(validators=[validators.NumberRange(min=0, max=500)],label="End")
