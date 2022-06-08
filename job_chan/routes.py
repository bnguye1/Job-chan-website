from job_chan import app
from job_chan.models import User, load_user, Job
from flask import request, render_template, redirect, url_for
from .forms import RegistrationForm, LoginForm
from . import db, login_manager
from flask_login import logout_user, current_user
from job_chan.scrapers.update_jobs import get_list_of_jobs


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # print(request.form)
        if "get_jobs" in request.form:
            jobs = get_list_of_jobs('software_engineer', 'maryland')
            #print(jobs)
            print('they want jobs')

            for job in jobs:
                a_job = Job(job_title=job[0], company=job[1], location=job[2], salary=job[3],
                            post_date=job[4], updated_date=job[5], job_link=job[6])
                db.session.add(a_job)
                db.session.commit()
        else:
            print('they want something else')
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


# Add a donate option years beyond when this thing is done

# Works, do not touch
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    message = ""
    if form.validate_on_submit():
        some_user = User.query.filter_by(email=form.email.data).first()
        if some_user is None:
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

