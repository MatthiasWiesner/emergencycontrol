from flask.ext.script import Manager, Server

from emergencycontrol import app
from emergencycontrol.model import init_db, clear_db

manager = Manager(app)
if app.debug:
    server = Server()
else:
    server = Server(host="0.0.0.0", use_debugger=False)
manager.add_command("runserver", server)


@manager.command
def initdb():
    """Initialize database."""
    with app.app_context():
        init_db()


@manager.command
def cleardb():
    """Clear database."""
    with app.app_context():
        clear_db()


if __name__ == '__main__':
    manager.run()
