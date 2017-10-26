from c_Batiment import *


class Ferme(Batiment):
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "ferme")

	def generer(self):
		pass
