import flask
import json
import calendar
from flask import request
from forms import LoginForm, EventForm
from filer import File

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
            f = File('events')
            data = f.read()
            data = sorted(data, key=lambda x: x['start'])

            c = calendar.TextCalendar(calendar.SUNDAY)
            c = c.formatmonth(2018, 8)
            c = c.replace('   ', '0 ')
            items = c.split()

            print(items)
            
            month = c[1]
            year = c[2]
            items = items[10:]

            return flask.render_template('events.html', data=data, user=username, calendar=items)
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
                    new_data = form.data
                    new_data['start'] = str(new_data['start'])
                    new_data['end'] = str(new_data['end'])
                    del new_data['csrf_token']
                    del new_data['submit']
                    f = File('events')
                    data = f.read()
                    data.append(new_data)
                    data = json.dumps(data)
                    f.write(data)
                    return data
                else:
                    return 'FORM FAILED'
            else:
                return flask.render_template('add.html', form=form, user=username)
    else:
        return flask_redirect('/login')


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    return 'EDIT'

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
    f = File('users')
    user_data = f.read()
    if username in user_data:
        return True
    else:
        return False

if __name__ == "__main__":
    app.run()

