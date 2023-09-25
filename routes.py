import os
import datetime
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# local
import lib.dates as dates
import lib.movies_list as movies_list

app = Flask(__name__)


@app.route('/register', methods=["GET"])
def register():
    
    return render_template('register.html', name='', email='', age='')


@app.route('/about')
def about():

    current_date = datetime.now()
    expired_date = dates.calculate_expired_date(current_date)
    date = current_date.strftime('%d/%m/%Y  %H:%M')

    return render_template('about.html', date=date, expired_date=expired_date)


@app.route('/')
def home():

    oscar_environment_variable = f"{os.environ['OSCAR_DATE']}"
    oscar_date = datetime.strptime(oscar_environment_variable, "%Y/%m/%d")
    current_date = datetime.now()
    today_date = current_date.replace(
        minute=0, hour=0, second=0, microsecond=0)
    difference_day = dates.calculate_difference_day(today_date, oscar_date)
    year = oscar_date.year

    movies = movies_list.movies_list()

    return render_template('home.html', year=year, difference_day=difference_day, movies=movies)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method != "POST":
        return redirect(url_for('register'))

    name = request.form.get('name')
    email = request.form.get('email')
    age = int(request.form.get('age'))

    return render_template('profile.html', name=name, email=email, age=age)

@app.route('/login', methods=["GET"])
def login():
    """ Read login variables

    :args:
        name: the username, a string.
        password: the password, a string.

    :returns reading the variables.

    """

    email = request.form.get('name')
    password = request.form.get('password')

    return render_template('login.html', email=email, password=password)

@app.route('/begin', methods=['GET'])
def begin():
    """ Route accessed by logged in users

    """

    return render_template('begin.html')
