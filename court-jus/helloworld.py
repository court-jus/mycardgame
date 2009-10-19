# -*- coding: utf-8 -*-
import cgi, os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from models import *

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'index.html'),{}))
class CardList(webapp.RequestHandler):
    def get(self):
        cartes = CardType.all()
        self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'cardlist.html'),{'cartes': cartes}))

class Actions(webapp.RequestHandler):
    def post(self):
        g = self.request.get
        if g('action') == 'addcard':
            c = CardType(name = g('name'), desc = g('desc'))
            c.put()
        self.response.out.write('<html><body>Done <a href="/">Go</a>')
        self.response.out.write('</body></html>')

#        user = users.get_current_user()
#
#        if user:
#            self.response.headers['Content-Type'] = 'text/plain'
#            self.response.out.write('Hello, ' + user.nickname())
#        else:
#            self.redirect(users.create_login_url(self.request.uri))

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/cards', CardList),
     ('/addcard', Actions)],
    debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
