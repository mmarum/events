import flask
import json
from flask import request
from forms import LoginForm, EventForm
from reader import Read

# export FLASK_ENV=development
# FLASK_APP=app.py flask run

app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'development'


@app.route("/", methods=['GET'])
def main():
    if get_cookie('event_app'):
        username =  get_cookie('event_app').split('=')[1]
        if username_legit(username):
            r = Read('events')
            data = r.read_file()
            return flask.render_template('events.html', data=data, user=username)
    else:
    	return flask_redirect('/login')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.data['username']
            return set_cookie('event_app', 'username=' + username)
        else:
            return 'FORM VALIDATION FAILED'

    return flask.render_template('login.html', form=form)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if get_cookie('event_app'):
        username =  get_cookie('event_app').split('=')[1]
        if username_legit(username):
            form = EventForm()
            if request.method == 'POST':
                if form.validate_on_submit():
                    return 'FORM SUCCESS'
                else:
                    return 'FORM FAILED'
            else:
                return flask.render_template('add.html', form=form, user=username)
    else:
        return flask_redirect('/login')




        


# # # # # # # # # # # # # # # # #


def get_cookie(cookie_name):
    if cookie_name in request.cookies:
        return request.cookies.get(cookie_name)
    else:
        return False


def set_cookie(cookie_name, cookie_value):
    resp = flask.Response(status=302)
    resp.headers['location'] = '/'
    resp.set_cookie(cookie_name, cookie_value)
    return resp


def flask_redirect(location):
    resp = flask.Response(status=302)
    resp.headers['location'] = location
    return resp


def username_legit(username):
    r = Read('users')
    user_data = r.read_file()
    print(user_data)
    if username in user_data:
        return True
    else:
        return False

if __name__ == "__main__":
    app.run()

