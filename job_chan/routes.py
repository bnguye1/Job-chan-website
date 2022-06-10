from job_chan import app
from job_chan.models import User, Job
from flask import g, request, render_template, redirect, url_for, session
from .forms import RegistrationForm, LoginForm
from . import db
from job_chan.scrapers.update_jobs import get_list_of_jobs


@app.before_request
def before_request():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        g.user = user


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # print(request.form)
        if "get_jobs" in request.form:
            jobs = get_list_of_jobs('software_engineer', 'maryland')
            print('they want jobs')

            for job in jobs:
                a_job = Job(job_title=job[0], company=job[1], location=job[2], salary=job[3],
                            post_date=job[4], updated_date=job[5], job_link=job[6])
                db.session.add(a_job)
                db.session.commit()
        else:
            print('they want something else')

        return redirect(url_for('home'))

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
def login():
    session.pop('user_id', None)
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                some_user = User.query.filter_by(email=form.email.data).first()
                if some_user.check_password(form.password.data):
                    session['user_id'] = some_user.id
                    return redirect(url_for('home'))

            except Exception:
                return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')


@app.route('/saved', methods=['GET', 'POST'])
def saved():
    return render_template('saved.html')

