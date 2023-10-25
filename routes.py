import lib.dates as dates
import lib.movies_list as movies_list
import os
import datetime
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# local

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

app.config["SECRET_KEY"] = f"{os.environ['SECRET_KEY']}"

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/register', methods=["GET", "POST"])
def register():
    """ Set user registration

    Attributes:
        name (string): the username.
        email (string): the user's email.

    Returns: 
        read the variables e and redirects to the login page.

    """
    if request.method == "POST":
        user = User(email=request.form.get("email"),
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


@login_manager.user_loader
def load_user(user_id):
    """ Logs user in by set their id

    """
    return User.query.get(user_id)


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
        user = User.query.filter_by(
            email=request.form.get("email")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("begin"))
        else:
            alertMessage = "This user does not exist!"

    return render_template('login.html', alertMessage=alertMessage)


@app.route("/logout")
def logout():
    logout_user()

    """ Method to disconnect the user

    """

    return redirect(url_for("login"))


@app.route('/begin', methods=["GET", "POST"])
def begin():
    """ Route accessed by logged in users

    """

    return render_template('begin.html')
