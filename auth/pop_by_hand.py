from socket import socket

s=socket()
s.connect(('127.0.0.1',25))
print s.recv(4096)
s.send('EHLO jd_laptop\n')
print s.recv(4096)
s.send('MAIL FROM:<jd@jd>\n')
print s.recv(4096)
s.send('RCPT TO:<jd@jd>\n')
print s.recv(4096)
s.send('DATA\n')
print s.recv(4096)
s.send("""Subject: movie Tonight?

Terminator2 or Lady Chatterley?, you decide !
.

""")
