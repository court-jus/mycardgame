# -*- coding: utf-8 -*-
from django.db import models

class ManyCards(models.Model):
    name               = models.CharField(max_length = 200)
    def __repr__(self):
        return ">%s<" % self.name

class Ressource(models.Model):
    name               = models.CharField(max_length = 200)
    def __repr__(self):
        return "$%s$" % self.name

class CardCategory(models.Model):
    name               = models.CharField(max_length = 200)
    parent             = models.ForeignKey('self', null = True)
    def __repr__(self):
        return "(%s)" % self.name

class CardType(models.Model):
    name               = models.CharField(max_length = 200)
    cat                = models.ForeignKey(CardCategory)
    need               = models.ForeignKey('Contrainte')
    desc               = models.TextField()
    def __repr__(self):
        return "[%s]" % self.name
        
class Card(models.Model):
    ctyp               = models.ForeignKey(CardType)
    lieu               = models.ForeignKey(ManyCards)
    def __repr__(self):
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
    def __repr__(self):
        return "!%s!" % self.name

class Joueur(models.Model):
    deck               = models.ForeignKey(ManyCards, related_name = 'joueur_deck')
    main               = models.ForeignKey(ManyCards, related_name = 'joueur_main')
    cimetiere          = models.ForeignKey(ManyCards, related_name = 'joueur_cimetiere')
    table              = models.ForeignKey(ManyCards, related_name = 'joueur_table')
    vie                = models.IntegerField()
    name               = models.CharField(max_length = 200)
    def __repr__(self):
        return self.name

class Stock(models.Model):
    ressource          = models.ForeignKey(Ressource)
    quantite           = models.IntegerField()
    joueur             = models.ForeignKey(Joueur)