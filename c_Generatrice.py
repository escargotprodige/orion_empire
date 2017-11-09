from c_Batiment import *


class Generatrice(Batiment):
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "generatrice")
		self.range=0
		
		Batiment.calculenergiegen(self)
		print(self.metauxgen,self.energiegen,self.foodgen)
