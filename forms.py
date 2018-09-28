import hashlib
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, DateField, validators
from wtforms.validators import InputRequired, DataRequired, ValidationError
from reader import Read


def check_user():
    r = Read('users')
    users = r.read_file()
    print(users)


def validate_password(form, field):
    if field.data:
        password = field.data
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        if hashed_password != 'f4e86e89151d55bad3fbd1c62a797d6f':
            raise ValidationError('Password is not valid.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), validate_password])
    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    start = DateField('Start', validators=[InputRequired()], format='%Y-%m-%d %H:%M:%S')
    end = DateField('End', validators=[InputRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Submit')

