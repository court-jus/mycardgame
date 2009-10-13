# -*- coding: utf-8 -*-
from django.db import models

class ManyCards(models.Model):
    name               = models.CharField(max_length = 200)
    def __unicode__(self):
        return ">%s<" % self.name

class Ressource(models.Model):
    name               = models.CharField(max_length = 200)
    def __unicode__(self):
        return "$%s$" % self.name

class CardCategory(models.Model):
    name               = models.CharField(max_length = 200)
    parent             = models.ForeignKey('self', null = True)
    def __unicode__(self):
        return "(%s)" % self.name

class CardType(models.Model):
    name               = models.CharField(max_length = 200)
    cat                = models.ForeignKey(CardCategory)
    need               = models.ForeignKey('Contrainte')
    desc               = models.TextField()
    def __unicode__(self):
        return "[%s]" % self.name
        
class Card(models.Model):
    ctyp               = models.ForeignKey(CardType)
    lieu               = models.ForeignKey(ManyCards)

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

class Price(models.Model):
    ressource          = models.ForeignKey(Ressource)
    contrainte         = models.ForeignKey('Contrainte')
    qte                = models.IntegerField()

class Contrainte(models.Model):
    name               = models.CharField(max_length = 200)
    need_on_self_table = models.ManyToManyField(CardType, related_name = 'cont_selftable')
    need_on_adv_table  = models.ManyToManyField(CardType, related_name = 'cont_advtable')
    need_ressources    = models.ManyToManyField(Ressource, through = 'Price')
    def __unicode__(self):
        return "!%s!" % self.name

class Joueur(models.Model):
    deck               = models.ForeignKey(ManyCards, related_name = 'joueur_deck')
    main               = models.ForeignKey(ManyCards, related_name = 'joueur_main')
    cimetiere          = models.ForeignKey(ManyCards, related_name = 'joueur_cimetiere')
    table              = models.ForeignKey(ManyCards, related_name = 'joueur_table')
    vie                = models.IntegerField()
    name               = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.name

class Stock(models.Model):
    ressource          = models.ForeignKey(Ressource)
    quantite           = models.IntegerField()
    joueur             = models.ForeignKey(Joueur)