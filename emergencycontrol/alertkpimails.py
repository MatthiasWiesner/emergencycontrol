import time
import math
import email
import json
import imaplib
import requests
from flask_script import Command
from datetime import timedelta, datetime
from emergencycontrol import app


class AlertKpiMails(Command):

    def run(self):
        while True:
            yesterday = datetime.today() - timedelta(days=1)
            mails = self.get_mails(senton=yesterday.strftime("%d-%b-%Y"))
            for mail in mails:
                self.update_kpi(mail)
            # wait until tomorrow
            time.sleep(86400)

    def get_mails(self, senton):
        mails = []
        m = imaplib.IMAP4_SSL('imap.gmail.com')
        m.login(app.config['OPERATIONS_EMAIL_LOGIN'], app.config['OPERATIONS_EMAIL_PW'])
        m.select('SMS')
        search = '(SENTON %s)' % senton
        _, msgids = m.search(None, search)

        if not len(msgids):
            print "No SMS received on %s" % senton
            return []

        _, data = m.fetch(msgids[0].replace(' ', ','), '(RFC822)')
        # data is a list of tuples: ((envelopStart, msg), envelopEnd)
        for i in range(0, len(data), 2):
            _, msg = data[i][0], data[i][1]
            mails.append(email.message_from_string(msg))
        m.close()
        return mails

    def update_kpi(self, mail):
        pd = email.utils.parsedate(mail.get("Date"))
        url = 'https://kpi.cloudcontrolled.com/alert/messages'
        data = {"time": time.mktime(pd)}
        headers = {'Content-Type': 'application/json'}

        requests.post(url, data=json.dumps(data), headers=headers)
