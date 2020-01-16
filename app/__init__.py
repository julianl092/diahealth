from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

from app import routes, models

admin = Admin(app, name='run', template_mode='bootstrap3')
admin.add_view(ModelView(models.ModifiedQuestion, db.session))
