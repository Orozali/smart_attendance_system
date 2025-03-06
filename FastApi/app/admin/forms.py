from wtforms.validators import DataRequired, Email
from wtforms import EmailField, Form, PasswordField, StringField


class TeacherForm(Form):
    name = StringField('Name', validators=[DataRequired()], render_kw={'class': 'form-control'})
    surname = StringField('Surname', validators=[DataRequired()], render_kw={'class': 'form-control'})
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'form-control'})
    password = PasswordField('Password', render_kw={'class': 'form-control'})

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Hide the password field during editing
    #     if kwargs.get('obj') and kwargs['obj'].id:  # Check if an object is passed (editing mode)
    #         self.password.render_kw = {'class': 'form-control', 'style': 'display:none;'}  # Hide the password field