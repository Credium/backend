import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
import pytest

from app import create_app, db
from app.account.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    app.run()


@manager.command
def test():
    pytest.main(['-x', 'tests'])


if __name__ == "__main__":
    manager.run()
