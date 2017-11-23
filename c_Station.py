from orion_empire_modele import *


class Station():
	def __init__(self, parent, nom, systeme, x, y):
		self.parent = parent
		self.id = Id.prochainid()
		self.proprietaire = nom
		self.taille = 25
		self.x = x
		self.y = y
		self.systemeOrigine = systeme
		self.vie = 100
		self.dmg = 25
		self.rayon = 5
		self.angle = 0
		self.delais = 2

	def attaquer(self):
		for j in self.parent.parent.joueurs:
			if j.nom != self.proprietaire:
				for cible in j.vaisseauxinterplanetaires:
					x = cible.x
					y = cible.y
					if hlp.calcDistance(x, y, self.x, self.y) > self.rayon:
						cible.recevoir_dmg(self.dmg)

	def recevoir_dmg(self, dmg):
		if self.vie - dmg <= 0:
			self.meurt()
		else:
			self.vie -= dmg

	def orbiter(self):
		self.delais -= 1
		if self.delais <= 0:
			# self.delais = 5
			self.delais = 0
			self.angle += 1
			if self.angle >= 360:
				self.angle = 0

	def pointOrbite(self,x,y):
		self.x = x
		self.y = y
	
	def meurt(self):
		print(self.id,"est mort!")
		self.parent.stationSolaire.remove(self)
