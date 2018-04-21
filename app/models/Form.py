from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ScanDocumentForm(FlaskForm):
    photo = FileField(validators=[FileRequired(), FileAllowed(['pdf'], 'Pdf only!!')])
