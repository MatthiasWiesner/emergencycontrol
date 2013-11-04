from emergencycontrol import app
from flask import request, render_template, redirect, url_for, flash
from .model import User, Person, db_session
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

@app.route('/example')
def example():
    return render_template('example.html')

