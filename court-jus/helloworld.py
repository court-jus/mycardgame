# -*- coding: utf-8 -*-
import cgi, os, sys

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from models import *

def GenerateCards():
    # card stocks
    mcards = ManyCards.all()
    for m in mcards:
        m.delete()
    hand1 = ManyCards(name="hand1")
    hand1.put()
    hand2 = ManyCards(name="hand2")
    hand2.put()
    deck1 = ManyCards(name="deck1")
    deck1.put()
    deck2 = ManyCards(name="deck2")
    deck2.put()
    cem1 = ManyCards(name="cem1")
    cem1.put()
    cem2 = ManyCards(name="cem2")
    cem2.put()
    table1 = ManyCards(name="table1")
    table1.put()
    table2 = ManyCards(name="table2")
    table2.put()
    tablec = ManyCards(name="tablec")
    tablec.put()
    # ressources
    ress = Ressource.all()
    for r in ress:
        r.delete()
    wood = Ressource(name="Wood")
    wood.put()
    blood = Ressource(name="Blood")
    blood.put()
    alcohol = Ressource(name="Alcohol")
    alcohol.put()
    gold = Ressource(name="Gold")
    gold.put()
    mana = Ressource(name="Mana")
    mana.put()
    # card categoires
    cardcats = CardCategory.all()
    for cc in cardcats:
        cc.delete()
    building = CardCategory(name="Building")
    building.put()
    factory = CardCategory(name="Factory",parent_card = building)
    factory.put()
    creature = CardCategory(name="Creature")
    creature.put()
    # card rules (constraint)
    contraintes = Contrainte.all()
    for c in contraintes:
        c.delete()
    bldoc = Contrainte(name="For bldo")
    bldoc.put()
    # prices
    for p in Price.all():
        p.delete()
    bldop = Price(ressource = wood, contrainte = bldoc, qte = 1)
    bldop.put()
    # cardtypes
    cardtypes = CardType.all()
    for c in cardtypes:
        c.delete()
    bldo = CardType(name="Blood Donation",desc="Produces 1 blood per turn",quote="Give your blood, if it doesn't help an injuried one, it can help a dead one...",img="blooddonation",cat=factory, need = bldoc)
    bldo.put()
    wocu = CardType(name="Wood Cutter",desc="Produces 1 wood per turn",quote="As long as he uses his axe against trees only, everything is cool.",cat=factory)
    wocu.put()
    alem = CardType(name="Alembic",desc="Produces 1 alcohol per turn",quote="Prohibition doesn't mean it's prohibited, only that you must hide.",cat=factory)
    alem.put()
    # card instances
    cards = Card.all()
    for c in cards:
        c.delete()
    c = Card(ctyp = bldo, lieu = hand1)
    c.put()
    c = Card(ctyp = wocu, lieu = hand1)
    c.put()
    c = Card(ctyp = alem, lieu = hand1)
    c.put()
    # in the deck
    c = Card(ctyp = alem, lieu = deck1)
    c.put()
    c = Card(ctyp = alem, lieu = deck1)
    c.put()
    c = Card(ctyp = alem, lieu = deck1)
    c.put()
    c = Card(ctyp = alem, lieu = deck1)
    c.put()
    # players
    js = Joueur.all()
    for j in js:
        j.delete()
    j1 = Joueur(deck=deck1,main=hand1,cimetiere=cem1,table=table1,vie=20,name="Player 1")
    j1.put()
    j2 = Joueur(deck=deck2,main=hand2,cimetiere=cem2,table=table2,vie=20,name="Player 2", adv = j1)
    j2.put()
    j1.adv = j2
    j1.put()
    j2.put()
    # stock
    for s in Stock.all():
        s.delete()
    s = Stock(ressource = wood, quantite = 0, joueur = j1)
    s.put()
    return (j1.key(), j2.key())

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
            j1key, j2key = GenerateCards()
            j1 = Joueur.get(j1key)
            #self.redirect("/table")
        bldo = CardType.all().filter('name = ','Blood Donation')[0]
        allcards = CardType.all()
        self.response.out.write(template.render(getFullPath('table.html'),{
            'j1':Joueur.get(j1key),
            'j2':Joueur.get(j2key),
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
    def post(self):
        g = self.request.get
        if g('ctyp_id'):
            c = CardType.get(g('ctyp_id'))
            if c:
                self.response.out.write(c.getHTML(True))
                return
        self.response.out.write("Unknown card")

class playCard(webapp.RequestHandler):
    def post(self):
        g = self.request.get
        if g('card_id') and g('adv_id'):
            c = Card.get(g('card_id'))
            adv = Joueur.get(g('adv_id'))
            if not c:
                self.response.out.write("Unknown card")
                return
            if not adv:
                self.response.out.write("Unknown player")
                return
            if c and adv:
                canp = c.canPlay(adv)
                if canp is True:
                    js = """var nextplace = document.getElementById('table1');
                nextplace.appendChild(carddiv);
                currentplace.parentNode.removeChild(currentplace);"""
                else:
                    js = """alert("Can't play this card right now : %s");""" % (canp,);
                self.response.out.write(js.replace('"','\"'),)

                return
        self.response.out.write("erreur inconnue")

class drawCard(webapp.RequestHandler):
    def post(self):
        g = self.request.get
        if g('player_id'):
            p = Joueur.get(g('player_id'))
            if not p:
                self.response.out.write("Unknown player")
                return
            deck = p.deck
            hand = p.main
            try:
                pick_up = deck.card_set[0]
                pick_up.lieu = hand
                pick_up.put()
                self.response.out.write("""var dest = document.getElementById('hand1'); dest.innerHTML += "<a href=\\\"javascript:playCard('%s','%s');\\\">%s</a>";""" % (pick_up.key(),pick_up.lieu.joueur_main[0].adv.key(),pick_up.getHTML().replace('"','\\\"').replace("\n",""),))
            except IndexError:
                self.response.out.write("""alert('No more card to pick');""");
            return
        self.response.out.write("erreur, no player_id")

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/cards', CardList),
     ('/addcard', Actions),
     ('/table',Table),
     ('/tools/getBigCard',getBigCard),
     ('/tools/playCard',playCard),
     ('/tools/drawCard',drawCard),
    ],
    debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
