import datetime
import sendgrid
from time import sleep
from flask import render_template
from flask_script import Command
from model import Person, EmergencyService
from emergencycontrol import app


class Report(Command):
    def run(self):
        while True:
            now = datetime.date.today()
            if now.day == 1:
                month = now.month - 1
                year = now.year
                if month < 1:
                    year = now.year - 1
                    month = 12
                one_month_ago = datetime.date(day=1, month=month, year=year)

                report_list = []
                weeks = EmergencyService.query \
                    .filter(EmergencyService.start_date >= one_month_ago) \
                    .filter(EmergencyService.start_date < now) \
                    .order_by(EmergencyService.start_date.asc()).all()

                for w in weeks:
                    person = Person.query.get(w.person_id)
                    report = {'week': w.week_nr,
                            'start_date': w.start_date,
                            'end_date': w.end_date,
                            'hero': person.name}
                    report_list.append(report)

                s = sendgrid.Sendgrid(app.config['SENDGRID_USERNAME'], app.config['SENDGRID_PASSWORD'], secure=True)

                content = render_template("report.jinja", report_list=report_list)

                message = sendgrid.Message("ops@cloudcontrol.de", "Operations Hero: Report for {}".format(one_month_ago.strftime('%B of %Y')), "Report of the month", content)
                message.add_to(["cl@cloudcontrol.de", "fa@cloudcontrol.de", "pe@cloudcontrol.de"],
                               ["Claudia Leihener", "Fernando Alvarez", "Peter Elsayeh"])
                s.web.send(message)
                print('Send email on {}'.format(now))

            m = now + datetime.timedelta(days=1)
            t = datetime.datetime(m.year, m.month, m.day, 7, 0, 0)
            n = datetime.datetime.today()
            sleep(int((t - n).total_seconds()))
