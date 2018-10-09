import hashlib
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, DateField, validators
from wtforms.validators import InputRequired, DataRequired, ValidationError
from filer import File


def check_password(username):
    f = File('users')
    user_data = f.read()
    if username in user_data:
        password = user_data[username]
        return password
    else:
        raise ValidationError('Username not in system')


def hashed_password(password):
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hashed_password


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


    def validate(self):
        if not FlaskForm.validate(self):
            raise ValidationError('AUTH_FAIL')
        if hashed_password(self.password.data) != check_password(self.username.data):
            raise ValidationError('Password did not match')
        return True


class EventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    start = DateField('Start', validators=[InputRequired()], format='%Y-%m-%d %H:%M:%S')
    end = DateField('End', validators=[InputRequired()], format='%Y-%m-%d %H:%M:%S')
    location = StringField('Location')
    description = StringField('Description')
    submit = SubmitField('Submit')

