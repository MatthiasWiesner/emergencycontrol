from emergencycontrol import app
from flask import request, render_template, redirect, url_for, flash
from .model import User, Person, db_session, EmergencyService
from .forms import PersonForm
from flask.ext.login import login_required


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


@app.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    Person.query.delete()
    db_session.commit()
    flash('Person table resetted!', 'success')
    return redirect(url_for('person'))


@app.route('/testcall')
def testcall():
    return request.args.get('emps')

@app.route('/calendar')
def calendar():
    return render_template('calendar.jinja')
