from c_Batiment import *


class Ville(Batiment):
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "ville")
		self.range=0
		
		Batiment.calculfoodgen(self)
		Batiment.calculenergiegen(self)
		Batiment.calculmetauxgen(self)
		
		print(self.metauxgen,self.energiegen,self.foodgen)
 
		self.ressource =  {"metal": 20,
				  "energie": 20,
				  "nourriture": 20,}

	def generer(self):
		pass
