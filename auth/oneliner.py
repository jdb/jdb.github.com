
from urllib import request
from http import cookiejar
from getpass import getpass


### Password based
# pm = request.HTTPPasswordMgr()
# pm.add_password(None,'https://lwn.net/login',user='RobWilco', passwd=getpass())
# opener = request.build_opener(request.HTTPBasicAuthHandler(pm))   


### Cookie based
ch = request.HTTPCookieProcessor(cookiejar.CookieJar())
opener = request.build_opener(ch)   

opener.open("https://lwn.net/login", 'Username=RobWilco&Password=%s' % getpass() )

r = opener.open("http://lwn.net/Articles/402512" )

print(r.info())



