from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/about')
def index():
    return render_template('index.html')

@app.route('/')
def hello():
    return render_template('home.html')