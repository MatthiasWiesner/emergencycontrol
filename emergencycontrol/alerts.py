import imaplib
import email

from .config import config_vars


def get_mails(since, before):
    m = imaplib.IMAP4_SSL('imap.gmail.com')
    m.login(config_vars['OPERATIONS_EMAIL_LOGIN'], config_vars['OPERATIONS_EMAIL_PW'])
    m.select('SMS')
    _, msgids = m.search(None, '(SINCE %s BEFORE %s)' % (since, before))
    mails = []
    for id_ in msgids[0].split():
        _, data = m.fetch(id_, '(RFC822)')
        mails.append(email.message_from_string(data[0][1]))
    m.close()
    return mails
