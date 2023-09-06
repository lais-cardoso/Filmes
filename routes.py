from flask import Flask, render_template, url_for, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

data_atual = datetime.now()

# index route calculation
freeSample = timedelta(30)

unsubscribeDate = data_atual + freeSample

expiredDate = unsubscribeDate.strftime('%d/%m/%Y')

# home route calculation

date = data_atual.strftime('%d/%m/%Y  %H:%M')

oscarDate = datetime(2024, 3, 10)

year = oscarDate.year

difference = oscarDate - data_atual

differenceDay = difference.days

@app.route('/about')
def index():
    redirect(url_for('home'))
    return render_template('index.html', date=date, expiredDate=expiredDate)


@app.route('/')
def home():
    redirect(url_for('index'))
    return render_template('home.html', year=year, differenceDay=differenceDay)
