import flask
import json
from flask import request
from forms import LoginForm, EventForm
from reader import Read


app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'development'


@app.route("/", methods=['GET'])
def main():
    if get_cookie('event_app') == 'yes':
        r = Read('events')
        data = r.read_file()
        return flask.render_template('events.html', data=data)
    else:
    	return flask_redirect('/login')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return set_cookie('event_app', 'yes')

    return flask.render_template('login.html', form=form)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if get_cookie('event_app') == 'yes':
        form = EventForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                return 'Something'

        return flask.render_template('add.html', form=form)


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


if __name__ == "__main__":
    app.run()

