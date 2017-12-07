from orion_empire_modele import *

def getCoutMsg():
	return 30000

def getCoutEsg():
	return 4000

class StationGalactique():
	def __init__(self,parent,nom,systeme,x,y):
		self.parent=parent
		self.id=Id.prochainid()
		self.proprietaire=nom
		self.taille=25
		self.x=x
		self.y=y
		self.systemeOrigine = systeme
		self.coutM = getCoutMsg()
		self.coutE = getCoutEsg()
		
		self.angle = 0
		self.delais = 2
		
		
	def orbiter(self):
		self.delais -= 1
		if self.delais <= 0:
			#self.delais = 5 
			self.delais = 0
			self.angle += 1
			if self.angle >= 360:
				self.angle = 0
				