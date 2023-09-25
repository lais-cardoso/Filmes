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

    """ Read registration variables

    :args:
        name (string): the username.
        email (string): the user's email.
        age (int): the user's age.

    :returns reading the variables.

    """
    
    return render_template('register.html', name='', email='', age='')


@app.route('/about')
def about():

    """ Set current date and the limit date.

    :args:
        current_date (date): the current date with current time.
        expired_date (date) : days left until oscar day.
        date (date): the current date and time.

    :returns current date and the limit date.

    """

    current_date = datetime.now()
    expired_date = dates.calculate_expired_date(current_date)
    date = current_date.strftime('%d/%m/%Y  %H:%M')

    return render_template('about.html', date=date, expired_date=expired_date)


@app.route('/')
def home():

    """ Set the list of films and the calculation for the Oscar date.

    :args:
        oscar_environment_variable (string): the oscar date, a environment variable.
        oscar_date (date): oscar date in correct format.
        current_date (date): the current date.
        today_date (date): the current date without current time.
        difference_day (date): 
        year (string): A year of oscar date.
        movies (array): A list of movies. 

    :returns the list of films and how many days until the Oscars.

    """

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

    """ Read login variables

    :args:
        name (string): the username.
        email (string): the user's email.
        age (string): the user's age.

    :returns reading the variables.

    """

    if request.method != "POST":
        return redirect(url_for('register'))

    name = request.form.get('name')
    email = request.form.get('email')
    age = int(request.form.get('age'))

    return render_template('profile.html', name=name, email=email, age=age)