from django.db import models

def CardType(models.Model):
	name = models.CharField()

def Card(models.Model):
	type = models.ForeignKey(CardType)
	name = models.CharField()
	lieu = models.ForeignKey(ManyCards)

def Ressource(models.Model):
	name = models.CharField()

def Stock(models.Model):
	ressource = models.ForeignKey(Ressource)
	quantite  = models.IntegerField()
	joueur    = models.ForeignKey(Joueur)

def ManyCards(models.Model):
	pass

def Joueur(models.Model):
	deck = models.ForeignKey(ManyCards)
	main = models.ForeignKey(ManyCards)
	cimetiere = models.ForeignKey(ManyCards)
	table = models.ForeignKey(ManyCards)
	vie = models.IntegerField()
	name = models.CharField()
