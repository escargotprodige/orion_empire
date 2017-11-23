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
		self.angle = 0
		self.delais = 2

	def attaquer(self):
		pass

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
