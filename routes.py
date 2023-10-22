import os
import datetime
import sqlite3
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# local
import lib.movies_list as movies_list
import lib.dates as dates


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///login.db"

app.config["SECRET_KEY"] = "123456"

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=["GET", "POST"])
def register():
    """ Read registration variables

    Attributes:
        name (string): the username.
        email (string): the user's email.
        age (int): the user's age.

    Returns: 
        read the variables.

    """
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)

        db.session.commit()

        return redirect(url_for("login"))

    return render_template('register.html')


@app.route('/about')
def about():
    """ Set current date and the limit date.

    Attributes:
        current_date (date): the current date with current time.
        expired_date (date) : days left until oscar day.
        date (date): the current date and time.

    Returns:
        current date and the limit date.

    """

    current_date = datetime.now()
    expired_date = dates.calculate_expired_date(current_date)
    date = current_date.strftime('%d/%m/%Y  %H:%M')

    return render_template('about.html', date=date, expired_date=expired_date)


@app.route('/')
def home():
    """ Set the list of films and the calculation for the Oscar date.

    Attributes:
        oscar_environment_variable (string): the oscar date, a environment variable.
        oscar_date (date): oscar date in correct format.
        current_date (date): the current date.
        today_date (date): the current date without current time.
        difference_day (date): 
        year (string): A year of oscar date.
        movies (array): A list of movies. 

    Returns:
        the list of films and how many days until the Oscars.

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


# @app.route('/profile', methods=["GET", "POST"])
# def profile():
#     """ Set registration variables

#     Attributes:
#         name (string): the username.
#         email (string): the user's email.
#         age (string): the user's age.

#     Returns:
#         Set the values in registration variables.

#     """

#     if request.method != "POST":
#         return redirect(url_for('register'))

#     # name = request.form.get('name')
#     # email = request.form.get('email')
#     # age = int(request.form.get('age'))

#     return render_template('profile.html')

@login_manager.user_loader
def load_user(user_id):
     #connection = sqlite3.connect('/var/www/flask/login.db')
     return Users.query.get(user_id)

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

    if request.method == "POST":
        user = Users.query.filter_by(
            username = request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("begin"))
        else:
            alertMessage = "This user does not exist!"

    return render_template('login.html', alertMessage=alertMessage)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/begin', methods=["GET", "POST"])
def begin():
    """ Route accessed by logged in users

    """

    return render_template('begin.html')
