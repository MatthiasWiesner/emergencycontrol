from time import sleep
import datetime
from model import Person, EmergencyService
import sendgrid
from emergencycontrol import app

from flask.ext.script import Command

class Report(Command):
    def run(self):
        while True:
            sleep(86400) # One day long
            now = datetime.date.today()
            month = now.month - 1
            year = now.year
            if month < 1:
                year = now.year - 1
                month = 12

            one_month_ago = datetime.date(day=1, month=month, year=year)

            if now.day == 1:
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



                # make a secure connection to SendGrid
                s = sendgrid.Sendgrid(app.config['SENDGRID_USERNAME'], app.config['SENDGRID_PASSWORD'], secure=True)

                content ="""
<!DOCTYPE html>
<html>
<head>
<style>
table
{
    border-collapse:collapse;
}
table, td, th
{
    border:1px solid black;
    padding: 3px;
}
</style>
</head>

<body>

<h2>Dear Claudia,</h2>

<table>
<tr>
    <th>Week</th>
    <th>Start Date</th>
    <th>End Date</th>
    <th>Hero</th>
</tr>
"""

                for r in report_list:
                    content += """
<tr>
        <td>
            {}
        </td>
        <td>
            {}
        </td>
        <td>
            {}
        </td>
        <td>
            {}
        </td>
</tr>
""".format(r.get('week'), r.get('start_date'), r.get('end_date'), r.get('hero'))

                content += """
</table>
</body>
</html>
"""

                message = sendgrid.Message("ops@cloudcontrol.de", "Operations Hero: Report for {}".format(one_month_ago.strftime('%B of %Y')), "Report of the month", content)
                message.add_to(["cl@cloudcontrol.de", "fa@cloudcontrol.de", "pe@cloudcontrol.de"],
                               ["Claudia Leihener", "Fernando Alvarez", "Peter Elsayeh"])

                s.web.send(message)
                print('Send email on {}: {}'.format(now, content))
