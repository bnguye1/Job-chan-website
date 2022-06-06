from job_chan import app
from job_chan.models import User, Job, load_user
from flask import render_template, session, redirect, url_for
from .forms import RegistrationForm, LoginForm
from . import db, login_manager
from flask_login import login_required, logout_user, current_user


@app.route('/home')
def home():
    return render_template('home.html')


# Works, do not touch
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    message = ""
    if form.validate_on_submit():
        some_user = User.query.filter_by(email=form.email.data).first()
        if not some_user:
            if form.password.data == form.confirm_password.data:
                user = User(email=form.email.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

        else:
            message = "A user associated with that email already exists!"

    return render_template('register.html', form=form, message=message)


# Isn't working entirely at all
# TTODO: Implement authentication backend
@app.route('/login', methods=['POST', 'GET'])
@login_manager.user_loader
def login():
    form = LoginForm()
    if form.validate_on_submit():
        some_user = User.query.filter_by(email=form.email.data).first()
        if some_user.check_password(form.password.data):
            load_user(some_user.id)
            data = some_user
            return render_template('home.html', data=data)

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('logout'))
    else:
        return redirect(url_for('login'))

