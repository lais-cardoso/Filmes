from flask import Flask, render_template
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os
import dates

oscar_environment_variable = f"{os.environ['OSCAR_DATE']}"

oscar_date = datetime.strptime(oscar_environment_variable, "%Y/%m/%d")

app = Flask(__name__)

@app.route('/about')
def index():
    current_date = datetime.now()
    expired_date = dates.calculate_expired_date(current_date)
    date = current_date.strftime('%d/%m/%Y  %H:%M')

    return render_template('index.html', date=date, expired_date=expired_date)


@app.route('/')
def home():
    current_date = datetime.now()
    difference_day = dates.calculate_difference_day(current_date)
    year = oscar_date.year
    return render_template('home.html', year=year, difference_day=difference_day)
