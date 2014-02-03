import imaplib
import email
import time
from datetime import date, datetime, timedelta
from emergencycontrol import app
from .model import Person, EmergencyService
from flask_login import login_required
from flask import render_template


def get_mails(since, before):
    mails = []
    m = imaplib.IMAP4_SSL('imap.gmail.com')
    m.login(app.config['OPERATIONS_EMAIL_LOGIN'], app.config['OPERATIONS_EMAIL_PW'])
    m.select('SMS')
    _, msgids = m.search(None, '(SINCE %s BEFORE %s)' % (since, before))
    _, data = m.fetch(msgids[0].replace(' ', ','), '(RFC822)')
    # data is a list of tuples: ((envelopStart, msg), envelopEnd)
    for i in range(0, len(data), 2):
        _, msg = data[i][0], data[i][1]
        mails.append(email.message_from_string(msg))
    m.close()
    return mails


@app.route('/alerts')
@login_required
def alerts():
    now = date.today()
    weeks_until_today = EmergencyService.query\
        .filter(EmergencyService.start_date <= now)\
        .order_by(EmergencyService.start_date.desc()).all()

    since = weeks_until_today[-1].start_date.strftime("%d-%b-%Y")
    before = (date.today() + timedelta(1)).strftime("%d-%b-%Y")

    mails = get_mails(since, before)
    persons = Person.query.all()

    for week in weeks_until_today:
        week.adcloud_count = 0
        week.mails = []
        for mail in mails:
            if not 'up' or 'fixed' in mail.get_payload().lower():
                pd = email.utils.parsedate(mail.get("Date"))
                mdate = date.fromtimestamp(time.mktime(pd))
                mail.date = datetime.fromtimestamp(time.mktime(pd)).strftime('%d.%m.%Y - %H:%M:%S')
                if mdate >= week.start_date and mdate < week.end_date:
                    week.mails.append(mail)
                    if 'adcloud' in mail.get_payload().lower():
                        week.adcloud_count += 1

        for p in persons:
            if p.id == week.person_id:
                week.person = p

    return render_template('alerts.jinja', weeks=weeks_until_today)
