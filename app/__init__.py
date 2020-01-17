from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Dia Health Admin', template_mode='bootstrap3')

from app import routes, models


