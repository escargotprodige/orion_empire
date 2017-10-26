from IdMaker import *


class Batiment:
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y, type):
		self.parent = parent
		self.proprietaire = proprietaire
		self.systemeid = systemeid
		self.planeteid = planeteid
		self.x = x
		self.y = y
		self.id = Id.prochainid()
		self.type = type

	def generer(self):
		pass
