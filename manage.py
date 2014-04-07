from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from emergencycontrol import app, db
from emergencycontrol.report import Report
from emergencycontrol.heronotify import HeroNotify
from emergencycontrol.alertmails import AlertMails

manager = Manager(app)

server = Server(host="0.0.0.0", use_debugger=app.config['DEBUG'])
manager.add_command("runserver", server)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('report', Report())
manager.add_command('notify', HeroNotify())
manager.add_command('alerts', AlertMails())


if __name__ == '__main__':
    manager.run()
