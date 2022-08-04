from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import upgrade, Migrate, stamp, init

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24).hex()
db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()

from job_chan import routes
from job_chan.models import User, Job

db.create_all()
migrate = Migrate(app, db)

# migrate database to latest revision
if not os.path.isfile('database.db') and not os.path.isdir('migrations'):
    init()

stamp()
migrate.init_app(app, db)
upgrade()


