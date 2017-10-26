from c_Batiment import *


class Mine(Batiment):
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "mine")

	def generer(self):
		pass
