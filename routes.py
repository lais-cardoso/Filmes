from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/about')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('home.html')
