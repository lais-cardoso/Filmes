from flask import Flask, render_template, request

from forms import register_validate

app = Flask(__name__)

@app.route('/register', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        register_validate(name, email, age)
    return render_template('register.html')

