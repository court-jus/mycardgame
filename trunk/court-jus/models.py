# -*- coding: utf-8 -*-
from google.appengine.ext import db
import sys

class ManyCards(db.Model):
    name               = db.StringProperty()
    def __unicode__(self):
        return ">%s<" % self.name

class Ressource(db.Model):
    name               = db.StringProperty()
    def __unicode__(self):
        return "$%s$" % self.name

class CardCategory(db.Model):
    name               = db.StringProperty()
    parent_card        = db.SelfReferenceProperty()
    def __unicode__(self):
        return "(%s)" % self.name

class Contrainte(db.Model):
    name               = db.StringProperty()
    def __unicode__(self):
        return "!%s!" % self.name

class CardType(db.Model):
    name               = db.StringProperty()
    cat                = db.ReferenceProperty(CardCategory)
    need               = db.ReferenceProperty(Contrainte)
    desc               = db.TextProperty()
    quote              = db.TextProperty()
    img                = db.StringProperty()
    def __unicode__(self):
        return "[%s]" % self.name

    def getHTML(self, big = False):
        return """<div class="%scard" onmouseover="javascript:showCard('%s');">
<img src="/img/%s.png">
<span class="cardtitle">%s</span>
<div class="carddesc">%s
<div class="cardquote">%s</div>
</div>
</div>""" % ((big and "big" or ""), self.key(), (self.img or "card1") + (big and "_b" or "_r"), self.name, (big and self.desc or ""), (big and self.quote or ""))
class Card(db.Model):
    ctyp               = db.ReferenceProperty(CardType)
    lieu               = db.ReferenceProperty(ManyCards)

    def canPlay(self, adv):
        joueur     = self.lieu.joueur_main.get()
        contrainte = self.ctyp.need
        if contrainte:
            for price in contrainte.price_set:
                found_stock = False
                stock_joueur = joueur.stock_set.filter('ressource = ',price.ressource.key())
                if stock_joueur:
                    for sj in stock_joueur:
                        if sj.quantite >= price.qte:
                            found_stock = True
                            break
                if not found_stock:
                    return "Not enough %s" % (price.ressource.name,)
            for card in contrainte.needonselftable_set:
                if not joueur.table.card_set.filter(ctyp = card):
                    return "nécessite d'avoir la carte %s sur la table" % (card,)
            for card in contrainte.needonadvtable_set:
                if not adv.table.card_set.filter(ctyp = card):
                    return "nécessite que l'adversaire ait la carte %s sur la table" % (card,)
        return True

    def __unicode__(self):
        return "%s-%s" % (self.ctyp,self.lieu)

    def getHTML(self, big = False):
        return """<div id="card_%s" class="%scard" onmouseover="javascript:showCard('%s');">
<img src="/img/%s.png">
<span class="cardtitle">%s</span>
<div class="carddesc">%s
<div class="cardquote">%s</div>
</div>
</div>""" % (self.key(), (big and "big" or ""), self.ctyp.key(), (self.ctyp.img or "card1") + (big and "_b" or "_r"), self.ctyp.name, (big and self.ctyp.desc or ""), (big and self.ctyp.quote or ""))

class Price(db.Model):
    ressource          = db.ReferenceProperty(Ressource)
    contrainte         = db.ReferenceProperty(Contrainte)
    qte                = db.IntegerProperty()

class NeedOnSelfTable(db.Model):
    cardtype           = db.ReferenceProperty(CardType)
    contrainte         = db.ReferenceProperty(Contrainte)

class NeedOnAdvTable(db.Model):
    cardtype           = db.ReferenceProperty(CardType)
    contrainte         = db.ReferenceProperty(Contrainte)


class Joueur(db.Model):
    deck               = db.ReferenceProperty(ManyCards, collection_name = 'joueur_deck')
    main               = db.ReferenceProperty(ManyCards, collection_name = 'joueur_main')
    cimetiere          = db.ReferenceProperty(ManyCards, collection_name = 'joueur_cimetiere')
    table              = db.ReferenceProperty(ManyCards, collection_name = 'joueur_table')
    vie                = db.IntegerProperty()
    name               = db.StringProperty()
    adv                = db.SelfReferenceProperty()
    def __unicode__(self):
        return self.name

class Stock(db.Model):
    ressource          = db.ReferenceProperty(Ressource)
    quantite           = db.IntegerProperty()
    joueur             = db.ReferenceProperty(Joueur)
