from twisted.web.resource import Resource

class ShowSession(Resource):
    def render_GET(self, request):
        return 'Your session id is: ' + request.getSession().uid

class ExpireSession(Resource):
    def render_GET(self, request):
        request.getSession().expire()
        return 'Your session has been expired.'

resource = ShowSession()
resource.putChild("expire", ExpireSession())
