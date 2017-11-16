from c_Batiment import *


class Mine(Batiment):
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "mine")
		self.range = 2
		
		Batiment.calculmetauxgen(self)
		print(self.metauxgen,self.energiegen,self.foodgen)

