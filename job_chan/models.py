from job_chan import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

login = LoginManager()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Job(db.Model):
    __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String, nullable=False)
    company = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    salary = db.Column(db.String, nullable=False)
    post_date = db.Column(db.String, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)
    job_link = db.Column(db.String, nullable=False)

    # def __init__(self, id, title, company, location, salary, post_date, updated_date, link):
    #     self.job_id = id
    #     self.job_title = title
    #     self.company = company
    #     self.location = location
    #     self.salary = salary
    #     self.post_date = post_date
    #     self.updated_date = updated_date
    #     self.job_link = link
    #


@login.user_loader
def load_user(ids):
    return User.query.get(int(ids))

