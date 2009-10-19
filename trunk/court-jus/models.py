# -*- coding: utf-8 -*-
from google.appengine.ext import db

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
    def __unicode__(self):
        return "[%s]" % self.name
        
class Card(db.Model):
    ctyp               = db.ReferenceProperty(CardType)
    lieu               = db.ReferenceProperty(ManyCards)

    def canPlay(self, adv):
        joueur     = self.lieu.joueur_main.get()
        contrainte = self.ctyp.need
        print "on commence par verifier les ressources :"
        for price in contrainte.price_set.all():
            print price
            found_stock = False
            stock_joueur = joueur.stock_set.filter(ressource = price.ressource)
            if stock_joueur:
                for sj in stock_joueur:
                    if sj.quantite >= price.qte:
                        found_stock = True
                        break
            if not found_stock:
                return "pas assez de %s" % (price.ressource,)
        print "ensuite les cartes qu'on a sur la table"
        for card in contrainte.need_on_self_table.all():
            print card
            if not joueur.table.card_set.filter(ctyp = card):
                return "nécessite d'avoir la carte %s sur la table" % (card,)
        print "enfin les cartes que l'adversaire a sur la table"
        for card in contrainte.need_on_adv_table.all():
            print card
            if not adv.table.card_set.filter(ctyp = card):
                return "nécessite que l'adversaire ait la carte %s sur la table" % (card,)
        return True
        

    def __unicode__(self):
        return "%s-%s" % (self.ctyp,self.lieu)

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
    def __unicode__(self):
        return self.name

class Stock(db.Model):
    ressource          = db.ReferenceProperty(Ressource)
    quantite           = db.IntegerProperty()
    joueur             = db.ReferenceProperty(Joueur)