from datetime import date, timedelta, time as dtime
from emergencycontrol import app
from .model import Person, EmergencyService, Alert
from flask_login import login_required
from flask import render_template


@app.route('/alerts')
@login_required
def alerts():
    now = date.today()
    weeks = {}

    alerts = Alert.query.all()
    persons = Person.query.all()

    for alert in alerts:
        if 'Fixed:' in alert.payload or 'UP:' in alert.payload:
            continue

        alert.date = alert.datetime.strftime('%Y-%m-%d')
        alert_monday_date = (alert.datetime - timedelta(days=(alert.datetime.isoweekday()-1))).date()

        if not alert_monday_date in weeks.keys():
            week = EmergencyService.query\
                .filter(EmergencyService.start_date <= alert.date)\
                .filter(EmergencyService.end_date >= alert.date)\
                .first()

            weeks[alert_monday_date] = week
            week.mails = []
            week.count_alarm_worktime = 0
            week.count_alarm_nighttime = 0
            week.days = {i:0 for i in range(7)}

        adate = alert.datetime.date()
        if  adate >= week.start_date and adate < week.end_date:
            week.days[alert.datetime.weekday()] += 1
            if alert.datetime.time() >= dtime(18, 0) or alert.datetime.time() < dtime(9, 0):
                week.count_alarm_nighttime += 1
            else:
                week.count_alarm_worktime += 1
        week.mails.append(alert)

        for p in persons:
            if p.id == week.person_id:
                week.person = p

    weeks = [v for k,v in sorted(weeks.items())]
    weeks.reverse()

    this_week_accumulative = sum(x[1] for x in weeks[0].days.iteritems() if x[0] <= now.weekday())
    last_week_accumulative = sum(x[1] for x in weeks[1].days.iteritems() if x[0] <= now.weekday())

    return render_template('alerts.jinja', weeks=weeks, this_week_accumulative=this_week_accumulative, last_week_accumulative=last_week_accumulative, weekday=now.strftime("%A"))
