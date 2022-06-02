from job_chan import app
from job_chan.models import User, Job
from flask import request, render_template, session, redirect

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # email = request.form['email']
        pass

    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # email = request.form['email']
        # username = request.form['username']
        # password = request.form['password']
        pass

    else:
        return render_template('login.html')