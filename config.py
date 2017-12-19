import os
import logging
from logging import StreamHandler

__author__ = "Steve"

'''Stores configuration settings'''


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_SESSION_FOR_NEXT = True

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class HerokuConfig(ProdConfig):
    @classmethod
    def init_app(cls, app):
        ProdConfig.init_app(app)

        # logging
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    "development": DevConfig,
    "production": ProdConfig,
    "heroku": HerokuConfig,
    "default": DevConfig
}
