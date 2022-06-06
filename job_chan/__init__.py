from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import upgrade, Migrate, stamp, init
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24).hex()
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()
db.create_all()
migrate = Migrate(app, db)


# migrate database to latest revision
stamp()
migrate.init_app(app)
upgrade()




from job_chan import routes
from job_chan.models import User, Job
