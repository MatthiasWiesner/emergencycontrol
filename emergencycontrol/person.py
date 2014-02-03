from emergencycontrol import app
from .model import Person
from .forms import PersonForm
from flask_login import login_required
from flask import render_template, redirect, url_for, flash, request
from emergencycontrol import db

@app.route('/person', methods=['GET', 'POST'])
def person():
    form = PersonForm()
    persons = Person.query.all()

    if form.validate_on_submit():
        person = Person(name=form.name.data,
                        phone=form.phone.data,
                        picture=form.image_url.data)
        db.session.add(person)
        db.session.commit()
        persons = Person.query.all()

    return render_template('persons.jinja', form=form, persons=persons)


@app.route('/person/set', methods=['POST'])
def person_set():
    person_id = int(request.form['person_id'])
    person = Person.query.get(person_id)
    if 'phone' in request.form:
        person.phone = request.form['phone']
    if 'picture' in request.form:
        person.picture = request.form['picture']
    if 'is_hero' in request.form:
        person.is_hero = request.form['is_hero'] == 'true'
    db.session.add(person)
    db.session.commit()
    return ''


@app.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    Person.query.delete()
    db.session.commit()
    return redirect(url_for('person'))
