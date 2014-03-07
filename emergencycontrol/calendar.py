import json
from emergencycontrol import app, db
from .model import Person, EmergencyService, CalendarLog
from datetime import date, datetime, timedelta
from flask_login import current_user, login_required
from flask import request, render_template, redirect, url_for, Response


@app.route('/calendar')
@login_required
def calendar():
    now = date.today()
    this_week = EmergencyService.query \
        .filter(EmergencyService.start_date <= now) \
        .filter(EmergencyService.end_date > now).first()
    persons = Person.query.filter(Person.is_hero == True, Person.is_gone == False).all()
    for p in persons:
        p.active = False
        if this_week.person_id and p.id == this_week.person_id:
            p.active = True
    now = date.today()
    return render_template('calendar.jinja', persons=persons, init_date=now)


@app.route('/calendar/load')
#@login_required
def load():
    fetch_type = request.args.get('fetch_type')
    init_date = datetime.strptime(request.args.get('init_date'), "%Y-%m-%d").date()

    if fetch_type == 'next':
        day_of_week = init_date.weekday()
        start_date = (init_date - timedelta(days=day_of_week))

        start_dates = [start_date + timedelta(days=(7*i)) for i in range(12)]
        weeks = EmergencyService.query.filter(EmergencyService.start_date.in_(start_dates)).all()
        week_start_dates = [w.start_date for w in weeks]

        for i, start_date in enumerate(start_dates):
            if start_date not in week_start_dates:
                current_week = start_date.isocalendar()[1]
                week = EmergencyService(week_nr=current_week, start_date=start_date, end_date=(start_date + timedelta(days=7, seconds=-1)))
                db.session.add(week)
                weeks.insert(i, week)
        db.session.commit()

    if fetch_type == 'previous':
        weeks = EmergencyService.query\
            .filter(EmergencyService.end_date < init_date)\
            .order_by(EmergencyService.end_date.desc())\
            .limit(12)\
            .all()
        weeks.reverse()

    persons = Person.query.all()
    data_list = []
    for week in weeks:
        w = week.to_dict()
        w['month'] = week.start_date.strftime("%d") + ' ' + week.start_date.strftime("%B")
        for p in persons:
            if w['person_id'] \
                and p.id == int(w['person_id']):
                w['person'] = p.to_dict()
        data_list.append(w)

    data = dict(weeks=data_list, prev=str(weeks[0].start_date), next=str(weeks[-1].end_date + timedelta(days=1)))
    return Response(json.dumps(data),  mimetype='application/json')


@app.route('/calendar/logs')
@login_required
def logs():
    data = [log.to_dict() for log in CalendarLog.query.order_by(CalendarLog.id.desc()).all()]
    return Response(json.dumps(data),  mimetype='application/json')


@app.route('/calendar/set', methods=['POST'])
@login_required
def calendar_set():
    week_id = int(request.form['week_id'])
    week = EmergencyService.query.get(week_id)
    week.person_id = int(request.form['person_id'])
    db.session.add(week)

    person = Person.query.get(int(request.form['person_id']))
    d = datetime.now()
    log = CalendarLog()
    log.date = d
    log.text = '{date} - {current_user} set {hero} as hero for week {week}'.format(
        date=d.strftime("%d.%m.%Y %H:%M"),
        current_user=current_user.name,
        hero=person.name,
        week=week.week_nr
    )
    db.session.add(log)
    db.session.commit()
    return ''


@app.route('/calendar/swap', methods=['POST'])
@login_required
def calendar_swap():
    week_from_id = int(request.form['week_from_id'])
    week_to_id = int(request.form['week_to_id'])

    week_from = EmergencyService.query.get(week_from_id)
    week_to = EmergencyService.query.get(week_to_id)

    person_from = week_from.person_id
    person_to = week_to.person_id

    week_from.person_id = person_to
    week_to.person_id = person_from

    db.session.add(week_from)
    db.session.add(week_to)

    d = datetime.now()
    log = CalendarLog()
    log.date = d
    hero_from = Person.query.get(week_from.person_id)
    hero_to = Person.query.get(week_to.person_id)
    log.text = '{date} - {current_user} swapped {hero_from}(wnr:{week_from}) with {hero_to}(wnr:{week_to})'.format(
        date=d.strftime("%d.%m.%Y %H:%M"),
        current_user=current_user.name,
        hero_from=hero_from.name,
        hero_to=hero_to.name,
        week_from=week_from.week_nr,
        week_to=week_to.week_nr,
    )
    db.session.add(log)
    db.session.commit()
    return ''
