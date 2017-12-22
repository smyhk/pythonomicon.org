import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import create_app
from app.models import db

app = create_app(os.getenv("DEPLOYMENT_ENV") or "default")

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, db)


@manager.command
def deploy():
    upgrade()


if __name__ == '__main__':
    manager.run()
