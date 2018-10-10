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

            # THIS WILL ALL BECOME A CLASS

            c = calendar.TextCalendar(calendar.MONDAY) # week starts with MONDAY

            year = 2018
            month = 10

            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            monthrange = calendar.monthrange(year, month)
            weekday_of_first = monthrange[0] # 'zero' is MONDAY
            days_in_month = monthrange[1]

            grid_array = []

            if month <= 9:
                month = str(month).zfill(2)

            # Creating skeleton json for the grid
            for n in range(days_in_month):
                day = n + 1
                if day <= 9:
                    day = str(day).zfill(2)
                grid_array.append( { "day": str(year) + "-" + str(month) + "-" + str(day), "events": [ ] } )

            #print(grid_array)

            # INSERT DATA INTO GRID

            # NOTE: In its current state
            # it assumes that data holds *this* month's data
            # it does not necessarily
            # TODO: make that dynamic

            # possible fix: break events.json up 
            # into month-based files like events-2018-10.json ???

            previous = -1
            for item in data:
                placement = int(item['start'].split('-')[2].lstrip('0')) - 1
                #print(placement)
                if previous != placement:
                    grid_array[placement]['events'] = []
                grid_array[placement]['events'].append(item)
                previous = placement


            #print(grid_array)

            # INSERT PLACEHOLDER ITEMS BEFORE THE FIRST
            # so that first starts in correct spot on grid
            if weekday_of_first > 0:
                y = range(weekday_of_first)
                for b in y:
                    grid_array.insert(0, { "day": "xxx", "events": [ ] })

            array_length = len(grid_array)

            # INSERT PLACEHOLDER ITEMS AFTER
            if array_length > 35:
                grid_size = 42
            else:
                grid_size = 35
            book_end = grid_size - array_length

            if book_end > 0:
                y = range(book_end)
                for b in y:
                    grid_array.append({ "day": "xxx", "events": [ ] })

            return flask.render_template('events.html', data=data, user=username, calendar=grid_array, weekdays=weekdays)
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

