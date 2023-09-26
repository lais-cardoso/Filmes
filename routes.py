import os
import datetime
from flask import Flask, redirect, render_template, request, url_for, session
from datetime import datetime
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import MySQLdb.cursors
load_dotenv()

# local
import lib.dates as dates
import lib.movies_list as movies_list

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LAIS123456'
app.config['MYSQL_DB'] = 'db_filmes'
app.config['SECRET_KEY'] = 'super secret key'

mysql = MySQL(app)

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

@app.route('/login', methods=["GET", "POST"])
def login():
    """ Read and validate login variables

    Attributes:
        email (string): the user's email.
        password (string): the password.

    Returns:
        If email and password are correct, 'begin' route is returned, if not, the alert message.
    """

    alertMessage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))

        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            session['id_user'] = user['id_user']
            session['email'] = user['email']
            session['password'] = user['password']
            
            return render_template('begin.html')
        else:
            alertMessage = 'This user does not exist!'

    return render_template('login.html', alertMessage=alertMessage)

@app.route('/begin', methods=["GET", "POST"])
def begin():
    """ Route accessed by logged in users

    """

    return render_template('begin.html')
