#/usr/bin/env python3
import socket, ssl
import re
import getpass

def read_page(s):

    if not hasattr(s, 'recv'):
        s.recv=s.read
        # Yeah great! sock and ssl_sock do not have the same APIs 

    # 1. Get the content length
    buf = s.recv(4096)
    while True:
        m = re.search(b'Content-Length: (\d+)',buf)
        if m:
            content_length = int(m.groups()[0])
            break
        else:
            buf += s.recv(4096)

    # 2. Find the empty line
    while True:
        m = re.search(b'\\r\\n\\r\\n',buf)
        if m:
            hdr, body = buf[:m.start()], buf[:m.end()]
            break
        else:
            buf += s.recv(4096)

    remaining = content_length - len(body)

    # 3. Read exactly "content length" bytes, 
    while remaining>0 and len(buf)!=0:   # why can't recv exactly the content length !
        buf = s.recv(4096 if remaining > 4096 else remaining)
        remaining -= len(buf)
        body += buf
    s.close()
    return (hdr, body)

def getpage(path):
    # Read a page
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('lwn.net',80))

    req = """GET %s HTTP/1.1
Host: lwn.net 
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US)
Content-Length: 0

""" % (path)

    s.send(bytes(req, 'ascii'))
    return read_page(s)


def get_auth_cookie(username='RobWilco'):
    # 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s,
                           ca_certs=None,
                           cert_reqs=ssl.CERT_NONE)
    ssl_sock.connect(('lwn.net',443))

    req = """POST /login HTTP/1.1
Host: lwn.net 
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US)
Content-Length: 37
Content-Type: application/x-www-form-urlencoded

Username=%s&Password=%s""" % (username, getpass.getpass())

    ssl_sock.write(bytes(req,'ascii'))
    hdr, body = read_page(ssl_sock)
    m = re.search(b'Set-Cookie: (.*?);',hdr)
    if m:
        return m.groups()[0] 
    else:
        print('Could not find the cookie')

def getpage_auth(path, cookie):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('lwn.net',80))

    req = """GET %s HTTP/1.1
Host: lwn.net
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US)
Cookie: %s

""" % (path, cookie.decode('ascii'))

    s.send(bytes(req, 'ascii'))
    return read_page(s)


cookie = get_auth_cookie()
print(cookie.decode('ascii'))
print(getpage_auth('/Articles/402512/', cookie)[0].decode('ascii'))





## Example POST page
# POST /examplehandler HTTP/1.1
# Host: www.google.com
# Connection: keep-alive
# User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US)
# Referer: http://www.google.com/exampleform
# Content-Length: 66
# Cache-Control: max-age=0
# Origin: http://www.google.com
# Content-Type: application/x-www-form-urlencoded
# Accept: application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
# Accept-Encoding: gzip,deflate,sdch
# Accept-Language: en-US,en;q=0.8
# Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3

# firstname=John&lastname=Smith&company=Smith+%26+Sons&id=1234567890
