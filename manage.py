from flask_script import Manager, Server

from emergencycontrol import app
from emergencycontrol.model import init_db, clear_db

manager = Manager(app)
server = Server(host="0.0.0.0", use_debugger=app.config['DEBUG'])
manager.add_command("runserver", server)


@manager.command
def initdb():
    with app.app_context():
        init_db()


@manager.command
def cleardb():
    with app.app_context():
        clear_db()


if __name__ == '__main__':
    manager.run()
