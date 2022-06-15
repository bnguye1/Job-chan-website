from job_chan import app
from job_chan.models import User, Job
from flask import g, request, render_template, redirect, url_for, session
from .forms import RegistrationForm, LoginForm, SearchForm
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


"""
https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates
Borrowed server-driven table template from https://github.com/miguelgrinberg/flask-tables
"""


@app.route('/data')
def data():
    query = Job.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Job.job_title.like(f'%{search}%'),
            Job.location.like(f'%{search}%'),
            Job.company.like(f'%{search}%'),
            Job.post_date.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['job_title', 'company', 'location', 'salary', 'post_date', 'job_link']:
            col_name = 'job_title'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Job, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@app.route('/home', methods=['POST', 'GET'])
def home():
    data2 = {
        'jobs': Job.query.all()
    }

    form = SearchForm()
    if request.method == 'POST':
        if "search_jobs" in request.form:
            if form.validate_on_submit():
                position = form.position.data
                location = form.location.data
                print(position, location)
                jobs = get_list_of_jobs(position, location)

                for job in jobs:

                    a_job = Job(job_title=job[0], company=job[1], location=job[2], salary=job[3],
                                post_date=job[4], updated_date=job[5], job_link=job[6])

                    if not Job.query.filter_by(job_title=job[0], company=job[1], location=job[2], salary=job[3],
                                               post_date=job[4], updated_date=job[5], job_link=job[6]).first():
                        db.session.add(a_job)
                        db.session.commit()

        return redirect(url_for('home'))

    return render_template('home.html', form=form, data=data2)


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

        # else:
        #     message = "A user associated with that email already exists!"

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
