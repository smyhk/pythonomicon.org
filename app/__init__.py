from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    # configure appropriate environment
    config[config_name].init_app(app)

    """
    from app.model import db
    db.init_app(app)
    """

    from app.views import mod
    app.register_blueprint(mod, url_prefix="/")

    return app
