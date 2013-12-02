import imaplib
import email

from .config import config_vars


def get_mails(since, before):
    mails = []
    m = imaplib.IMAP4_SSL('imap.gmail.com')
    m.login(config_vars['OPERATIONS_EMAIL_LOGIN'], config_vars['OPERATIONS_EMAIL_PW'])
    m.select('SMS')
    _, msgids = m.search(None, '(SINCE %s BEFORE %s)' % (since, before))
    _, data = m.fetch(msgids[0].replace(' ', ','), '(RFC822)')
    # data is a list of tuples: ((envelopStart, msg), envelopEnd)
    for i in range(0, len(data), 2):
        _, msg = data[i][0], data[i][1]
        mails.append(email.message_from_string(msg))
    m.close()
    return mails
