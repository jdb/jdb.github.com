

nc 127.0.0.1 25 -C -q 2  <<EOF
EHLO jd_laptop
MAIL FROM:<jd@jd>case 
RCPT TO:<jd@jd>
DATA
Subject: movie Tonight?

Terminator2 or Lady Chatterley?, you decide !
.


EOF