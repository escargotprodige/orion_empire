from c_Batiment import *


class Generatrice(Batiment):
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "generatrice")

	def generer(self):
		pass
