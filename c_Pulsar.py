from orion_empire_modele import *


class Pulsar():
	def __init__(self, parent, x, y):
		self.parent = parent
		self.id = Id.prochainid()
		# self.id=parent.parent.createurId.prochainid()
		self.proprietaire = "inconnu"
		self.x = x
		self.y = y
		self.periode = random.randrange(20, 50, 5)
		self.moment = 0
		self.phase = 1
		self.mintaille = self.taille = random.randrange(2, 4)
		self.maxtaille = self.mintaille + +random.randrange(1, 3)
		self.pas = self.maxtaille / self.periode
		self.taille = self.mintaille
		self.destination = None

	def evoluer(self):
		self.moment = self.moment + self.phase
		if self.moment == 0:
			self.taille = self.mintaille
			self.phase = 1
		elif self.moment == self.periode:
			self.taille = self.mintaille + self.maxtaille
			self.phase = -1
		else:
			self.taille = self.mintaille + (self.moment * self.pas)
