# -*- coding: utf-8 -*-
from django.db import models

class ManyCards(models.Model):
    pass

class Ressource(models.Model):
    name               = models.CharField()

class CardCategory(models.Model):
    name               = models.CharField()

class CardType(models.Model):
    name               = models.CharField()
    cat                = models.ForeignKey(CardCategory)
    need               = models.ForeignKey('Contrainte')
    desc               = models.TextField()
        
class Card(models.Model):
	ctyp               = models.ForeignKey(CardType)
	lieu               = models.ForeignKey(ManyCards)

class Price(models.Model):
    ressource          = models.ForeignKey(Ressource)
    qte                = models.IntegerField()

class Contrainte(models.Model):
    name               = models.CharField()
    need_on_self_table = models.ManyToManyField(CardType)
    need_on_adv_table  = models.ManyToManyField(CardType)
    prices             = models.ManyToManyField(Price)

class Joueur(models.Model):
	deck               = models.ForeignKey(ManyCards)
	main               = models.ForeignKey(ManyCards)
	cimetiere          = models.ForeignKey(ManyCards)
	table              = models.ForeignKey(ManyCards)
	vie                = models.IntegerField()
	name               = models.CharField()

class Stock(models.Model):
    ressource          = models.ForeignKey(Ressource)
    quantite           = models.IntegerField()
    joueur             = models.ForeignKey(Joueur)

