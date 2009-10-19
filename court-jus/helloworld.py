# -*- coding: utf-8 -*-
import cgi, os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from models import *

def getFullPath(filename):
    return os.path.join(os.path.dirname(__file__), filename)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render(getFullPath('index.html'),{}))

class CardList(webapp.RequestHandler):
    def get(self):
        cartes = CardType.all()
        self.response.out.write(template.render(getFullPath('cardlist.html'),{'cartes': cartes}))

class Table(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render(getFullPath('table.html'),{'hand1':['coucou','toi','hello','world'],'hand2':[1,2,3]}))

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
     ('/addcard', Actions),
     ('/table',Table),
    ],
    debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
