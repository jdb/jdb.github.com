import imaplib, getpass
i=imaplib.IMAP4_SSL('imap.gmail.com')
i.login('jeandaniel.browne', getpass.getpass())
i.select('INBOX')
i.search(None,'FROM','alerteimmo@seloger.com')
ans, ids = i.search(None,'(FROM "alerteimmo@seloger.com") (UNSEEN)')


