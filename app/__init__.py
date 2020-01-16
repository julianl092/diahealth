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
from flask_login import current_user

class SecuredModelView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

admin = Admin(app, name='Dia Health Admin', template_mode='bootstrap3')
admin.add_view(SecuredModelView(models.ModifiedQuestion, db.session))
