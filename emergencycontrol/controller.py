from emergencycontrol import app
from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user
from .model import Person, db_session, EmergencyService, Incident, User
from .forms import PersonForm
from flask.ext.login import login_required
from datetime import date, datetime, timedelta
import time
from markdown import markdown
import email.utils
from .alerts import get_mails


@app.route('/person', methods=['GET', 'POST'])
@login_required
def person():
    form = PersonForm()
    persons = Person.query.all()

    if form.validate_on_submit():
        person = Person(name=form.name.data,
                        phone=form.phone.data,
                        image_url=form.image_url.data)

        db_session.add(person)
        db_session.commit()
        persons = Person.query.all()
        flash('Person saved!', 'success')

    return render_template('persons.jinja', form=form, persons=persons)


@app.route('/swap', methods=['POST'])
@login_required
def swap():
    week_from_id = int(request.form['week_from_id'])
    week_to_id = int(request.form['week_to_id'])

    week_from = EmergencyService.query.get(week_from_id)
    week_to = EmergencyService.query.get(week_to_id)

    person_from = week_from.person_id
    person_to = week_to.person_id

    week_from.person_id = person_to
    week_to.person_id = person_from

    db_session.add(week_from)
    db_session.add(week_to)

    db_session.commit()

    return ''


@app.route('/set', methods=['POST'])
@login_required
def set():
    week_id = int(request.form['week_id'])
    week = EmergencyService.query.get(week_id)

    week.person_id = int(request.form['person_id'])

    db_session.add(week)
    db_session.commit()

    return ''


@app.route('/calendar')
def calendar():
    now = date.today()
    weeks_from_today = EmergencyService.query\
        .filter(EmergencyService.end_date >= now)\
        .order_by(EmergencyService.start_date.asc()).all()

    c = len(weeks_from_today)
    if c < 12:
        last_week = weeks_from_today[c-1]
        current_year = last_week.end_date.year
        current_week = last_week.week_nr
        new_weeks = 0
        while new_weeks < 12-c:
            current_week += 1
            start_date = datetime.strptime('{0} {1} 1'.format(current_year, current_week-1), '%Y %W %w')
            end_date = start_date + timedelta(days=7, seconds=-1)
            current_week = start_date.isocalendar()[1]
            current_year = start_date.isocalendar()[0]
            es = EmergencyService(week_nr=current_week, start_date=start_date, end_date=end_date)
            db_session.add(es)
            new_weeks += 1
        db_session.commit()
        return redirect(url_for('calendar'))

    persons = Person.query.all()
    for week in weeks_from_today:
        for p in persons:
            if p.id == week.person_id:
                week.person = p
    return render_template('calendar.jinja', weeks=weeks_from_today, persons=persons)


@app.route('/incidents', methods=['GET', 'POST'])
@login_required
def incidents():
    weeks = EmergencyService.query.order_by(EmergencyService.start_date.asc()).all()
    for week in weeks:
        if week.person_id:
            week.person = Person.query.get(week.person_id)
        incident = Incident.query.filter(Incident.emergency_service_id == week.id).first()
        if incident:
            incident.html = markdown(unicode(incident.text), ['fenced_code'])
            if incident.users_id:
                incident.last_user = User.query.get(incident.users_id)
            week.incident = incident
    return render_template('incidents.jinja', weeks=weeks)


@app.route('/savetext', methods=['POST'])
def save():
    week_id = int(request.form['week_id'])
    text = request.form['text']
    incident = Incident.query.filter(Incident.emergency_service_id == week_id).first()
    if not incident:
        incident = Incident(emergency_service_id=week_id)
    incident.text = text
    incident.users_id = current_user.id
    db_session.add(incident)
    db_session.commit()
    return markdown(text, ['fenced_code'])


@app.route('/gettext', methods=['GET'])
def gettext():
    week_id = int(request.args.get('week_id'))
    incident = Incident.query.filter(Incident.emergency_service_id == week_id).first()
    if incident:
        return incident.text
    else:
        return ""


@app.route('/alerts')
@login_required
def alerts():
    now = date.today()
    weeks_until_today = EmergencyService.query\
        .filter(EmergencyService.end_date <= now)\
        .order_by(EmergencyService.start_date.asc()).all()

    since = weeks_until_today[0].start_date.strftime("%d-%b-%Y")
    before = (date.today() + timedelta(1)).strftime("%d-%b-%Y")

    mails = get_mails(since, before)
    persons = Person.query.all()

    for week in weeks_until_today:
        week.mails = []
        for mail in mails:
            pd = email.utils.parsedate(mail.get("Date"))
            mdate = date.fromtimestamp(time.mktime(pd))
            mail.date = mdate.strftime('%d.%m.%Y')
            if mdate >= week.start_date and mdate < week.end_date:
                week.mails.append(mail)
            week.adcloud_count = 0
            if 'adcloud' in mail.get_payload().lower():
                week.adcloud_count += 1

        for p in persons:
            if p.id == week.person_id:
                week.person = p

    return render_template('alerts.jinja', weeks=weeks_until_today)


@app.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    Person.query.delete()
    db_session.commit()
    flash('Person table resetted!', 'success')
    return redirect(url_for('person'))


@app.route('/migrate')
def migrate():
    # do what you want
    return ''
