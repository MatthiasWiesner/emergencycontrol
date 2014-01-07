from time import sleep
import datetime
from model import Person, EmergencyService
import sendgrid
from emergencycontrol import app

from flask_script import Command
from flask import render_template


class HeroNotify(Command):

    def run(self):
        while True:
            now = datetime.date.today()
            if now.weekday() == 4:
                monday = now + datetime.timedelta(days=3)
                week = EmergencyService.query \
                    .filter(EmergencyService.start_date == monday) \
                    .first()

                person = Person.query.get(week.person_id)
                data = {'start_date': week.start_date,
                    'end_date': week.end_date,
                    'hero': person.name}

                # make a secure connection to SendGrid
                s = sendgrid.Sendgrid(app.config['SENDGRID_USERNAME'], app.config['SENDGRID_PASSWORD'], secure=True)

                content = render_template('notify.jinja', **data)
                message = sendgrid.Message("ops@cloudcontrol.de", "You are operations hero", text="You are operations hero", html=content)
                message.add_to(["mw@cloudcontrol.de", person.email],
                               ["Matthias Wiesner", person.name])

                s.web.send(message)
                print "Notification was send to {hero}".format(**data)

            m = now + datetime.timedelta(days=1)
            t = datetime.datetime(m.year, m.month, m.day, 7, 0, 0)
            n = datetime.datetime.today()
            sleep(int((t - n).total_seconds()))
