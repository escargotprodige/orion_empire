from c_Batiment import *


class Ferme(Batiment):
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "ferme")
		self.range = 1
		
		Batiment.calculfoodgen(self)
		print(self.metauxgen,self.energiegen,self.foodgen)
