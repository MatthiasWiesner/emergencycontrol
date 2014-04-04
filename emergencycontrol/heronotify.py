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
                content = render_template('notify.jinja', **data)
                sg = sendgrid.SendGridClient(app.config['SENDGRID_USERNAME'], app.config['SENDGRID_PASSWORD'], secure=True)
                message = sendgrid.Mail()
                message.add_to(["%s <%s>" % (person.name, person.email), 'MatthiasWiesner <mw+hero@cloudcontrol.de>'])
                message.set_subject('You are operations hero')
                message.set_text("You are operations hero")
                message.set_html(content)
                message.set_from('Operational Hero <ops@cloudcontrol.de>')
                sg.send(message)

                print "Notification was send to {hero}".format(**data)

            m = now + datetime.timedelta(days=1)
            t = datetime.datetime(m.year, m.month, m.day, 7, 0, 0)
            n = datetime.datetime.today()
            sleep(int((t - n).total_seconds()))
