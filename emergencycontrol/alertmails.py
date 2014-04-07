import time
import email
import imaplib
from flask_script import Command
from datetime import date, timedelta, datetime
from emergencycontrol import app
from .model import EmergencyService, Alert, db
from dateutil.relativedelta import relativedelta


class AlertMails(Command):

    def run(self):
        while True:
            now = date.today()
            month_before = now - relativedelta(months=1)

            weeks_until_today = EmergencyService.query\
                .filter(EmergencyService.start_date <= now)\
                .filter(EmergencyService.start_date > month_before)\
                .order_by(EmergencyService.start_date.desc()).all()

            since = weeks_until_today[-1].start_date.strftime("%d-%b-%Y")
            before = (date.today() + timedelta(1)).strftime("%d-%b-%Y")

            mails = self.get_mails(since, before)
            Alert.query.delete()
            for m in mails:
                pd = email.utils.parsedate(m.get("Date"))
                alert = Alert(
                    subject=m.get("Subject"),
                    payload=m.get_payload(),
                    datetime=datetime.fromtimestamp(time.mktime(pd)))
                db.session.add(alert)
            db.session.commit()
            time.sleep(60 * 30)


    def get_mails(self, since, before):
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
