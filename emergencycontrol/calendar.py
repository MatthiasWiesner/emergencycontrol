from emergencycontrol import app
from .model import Person, db_session, EmergencyService
from datetime import date, datetime, timedelta
from flask_login import login_required
from flask import request, render_template, redirect, url_for, Response
import json


@app.route('/calendar')
@login_required
def calendar():
    now = date.today()
    this_week = EmergencyService.query \
        .filter(EmergencyService.start_date <= now) \
        .filter(EmergencyService.end_date > now).first()
    persons = Person.query.all()
    for p in persons:
        p.active = False
        if this_week.person_id and p.id == this_week.person_id:
            p.active = True
    return render_template('calendar.jinja', persons=persons)


@app.route('/calendar/load')
@login_required
def load():
    now = date.today()
    if request.args.get('type') == 'next':
        weeks = EmergencyService.query\
            .filter(EmergencyService.end_date >= now)\
            .order_by(EmergencyService.start_date.asc()).all()

        c = len(weeks)
        if c < 12:
            last_week = weeks[c-1]
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

    elif request.args.get('type') == 'previous':
        weeks = EmergencyService.query\
            .filter(EmergencyService.start_date <= now)\
            .order_by(EmergencyService.start_date.desc()).all()

    persons = Person.query.all()
    data_list = []
    for week in weeks:
        w = week.to_dict()
        for p in persons:
            if w['person_id'] \
                and p.id == int(w['person_id']):
                w['person'] = p.to_dict()
        data_list.append(w)
    return Response(json.dumps(data_list),  mimetype='application/json')


@app.route('/calendar/set', methods=['POST'])
@login_required
def set():
    week_id = int(request.form['week_id'])
    week = EmergencyService.query.get(week_id)
    week.person_id = int(request.form['person_id'])

    db_session.add(week)
    db_session.commit()
    return ''


@app.route('/calendar/swap', methods=['POST'])
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
