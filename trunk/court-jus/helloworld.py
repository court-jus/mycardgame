# -*- coding: utf-8 -*-
import cgi, os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from models import *

def GenerateCards():
    cards = CardType.all()
    for c in cards:
        c.delete()
    c = CardType(name="Blood Donation",desc="Produces 1 blood per turn",quote="Give your blood, if it doesn't help an injuried one, it can help a dead one...",img="blooddonation")
    c.put()
    c = CardType(name="Wood Cutter",desc="Produces 1 wood per turn",quote="As long as he uses his axe against trees only, everything is cool.",img="card1")
    c.put()
    c = CardType(name="Alembic",desc="Produces 1 alcohol per turn",quote="Prohibition doesn't mean it's prohibited, only that you must hide.")
    c.put()

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
        if self.request.get("reset"):
            GenerateCards()
            self.redirect("/table")
        bldo = CardType.all().filter('name = ','Blood Donation')[0]
        allcards = CardType.all()
        self.response.out.write(template.render(getFullPath('table.html'),{
            'hand1':[bldo,bldo,bldo],
            'hand2':[1,2,3],
            'debug':allcards,
        }))

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

class getBigCard(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body><form action="/tools/getBigCard" method="post"><input name="card_id" type="text" /><input type="submit"/></form>')
        self.response.out.write('</body></html>')

    def post(self):
        g = self.request.get
        if g('card_id'):
            c = CardType.get(g('card_id'))
            if c:
                self.response.out.write(c.getHTML(True))
                return
        self.response.out.write("Unknown card")

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/cards', CardList),
     ('/addcard', Actions),
     ('/table',Table),
     ('/tools/getBigCard',getBigCard),
    ],
    debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
