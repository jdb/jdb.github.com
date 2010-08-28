
from twisted.web import client, error as weberror
from twisted.internet import reactor, defer
import sys, getpass, base64
import base64

@defer.inlineCallbacks    
def main():

    url = sys.argv[1]
    try:
        client.getPage('http://lwn,net')
    except failure:
        if failure.value.status == '401':
            creds = base64('%s:%s' % (username, password) )
            auth = 'Basic ' + creds.strip()
            print (yield client.getPage(url, headers = {'Authorization': auth}))
    reactor.stop()

main()
reactor.run()
            
    

