from orion_empire_modele import *


class StationGalactique():
	def __init__(self, parent, nom, systeme, x, y):
		self.parent = parent
		self.id = Id.prochainid()
		self.proprietaire = nom
		self.taille = 25
		self.x = x
		self.y = y
		self.systemeOrigine = systeme
