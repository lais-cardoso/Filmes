from flask import Flask, render_template, request
from forms import login_validate

app = Flask(__name__)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
        print(request.form["password"])
        
    return render_template('register.html')

