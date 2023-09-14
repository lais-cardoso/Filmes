import lib.dates as dates
import os
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# local

app = Flask(__name__)


@app.route('/register', methods=["GET"])
def register():

    return render_template('register.html', name='', email='', age='')


@app.route('/about')
def index():
    current_date = datetime.now()
    expired_date = dates.calculate_expired_date(current_date)
    date = current_date.strftime('%d/%m/%Y  %H:%M')

    return render_template('index.html', date=date, expired_date=expired_date)


@app.route('/')
def home():
    oscar_environment_variable = f"{os.environ['OSCAR_DATE']}"
    oscar_date = datetime.strptime(oscar_environment_variable, "%Y/%m/%d")
    current_date = datetime.now()
    difference_day = dates.calculate_difference_day(current_date, oscar_date)
    year = oscar_date.year

    return render_template('home.html', year=year, difference_day=difference_day)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method != "POST":
        return redirect(url_for('register'))

    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')

    return render_template('profile.html', name=name, email=email, age=age)
