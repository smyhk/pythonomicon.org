from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    # configure appropriate environment
    config[config_name].init_app(app)

    # initialize database
    from app.models import db
    db.init_app(app)

    login_manager.init_app(app)

    from app.views import mod
    app.register_blueprint(mod)

    return app
