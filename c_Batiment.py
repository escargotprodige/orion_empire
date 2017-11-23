from orion_empire_modele import *
from IdMaker import Id

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
		self.range = 0
		self.metauxgen=0
		self.foodgen=0
		self.energiegen=0

	def generer(self):
		joueur = self.parent.parent.joueurs[self.proprietaire]
		joueur.ajoutessource(metaux=self.metauxgen,food=self.foodgen,energie=self.energiegen)
		
	def calculfoodgen(self):
		
		planete=None
		
		joueur = self.parent.parent.joueurs[self.proprietaire]
		
		for s in joueur.systemesvisites:
			for p in s.planetes:
				if p.id == self.planeteid:
					planete = p
					break
					
		if planete:
			x = int(self.x)
			y = int(self.y)
			self.foodgen = planete.terrainRessource[x][y].food
			#print(self.metauxgen)
			for i in range(self.range):
				if x - i >= 0:
					self.foodgen += planete.terrainRessource[x-i][y].food
					#print(self.metauxgen)
					if y - i >= 0:
						self.foodgen += planete.terrainRessource[x-i][y-i].food
						#print(self.metauxgen)
					if y + i < planete.terrainTailleCarre:
						self.foodgen += planete.terrainRessource[x-i][y+i].food
						#print(self.metauxgen)
				if x + i < planete.terrainTailleCarre:
					self.foodgen += planete.terrainRessource[x+i][y].food
					#print(self.metauxgen)
					if y - i >= 0:
						self.foodgen += planete.terrainRessource[x+i][y-i].food
						#print(self.metauxgen)
					if y + i < planete.terrainTailleCarre:
						self.foodgen += planete.terrainRessource[x+i][y+i].food
						#print(self.metauxgen)
				if y - i >= 0:
					self.foodgen += planete.terrainRessource[x][y-i].food
					#print(self.metauxgen) 
				if y + i < planete.terrainTailleCarre:
					self.foodgen += planete.terrainRessource[x][y+i].food
					#print(self.metauxgen)
	
	def calculmetauxgen(self):
		
		planete=None
		
		joueur = self.parent.parent.joueurs[self.proprietaire]
		
		for s in joueur.systemesvisites:
			for p in s.planetes:
				if p.id == self.planeteid:
					planete = p
					break
					
		if planete:
			x = int(self.x)
			y = int(self.y)
			self.metauxgen = planete.terrainRessource[x][y].metaux
			#print(self.metauxgen)
			for i in range(self.range):
				if x - i >= 0:
					self.metauxgen += planete.terrainRessource[x-i][y].metaux
					#print(self.metauxgen)
					if y - i >= 0:
						self.metauxgen += planete.terrainRessource[x-i][y-i].metaux
						#print(self.metauxgen)
					if y + i < planete.terrainTailleCarre:
						self.metauxgen += planete.terrainRessource[x-i][y+i].metaux
						#print(self.metauxgen)
				if x + i < planete.terrainTailleCarre:
					self.metauxgen += planete.terrainRessource[x+i][y].metaux
					#print(self.metauxgen)
					if y - i >= 0:
						self.metauxgen += planete.terrainRessource[x+i][y-i].metaux
						#print(self.metauxgen)
					if y + i < planete.terrainTailleCarre:
						self.metauxgen += planete.terrainRessource[x+i][y+i].metaux
						#print(self.metauxgen)
				if y - i >= 0:
					self.metauxgen += planete.terrainRessource[x][y-i].metaux
					#print(self.metauxgen) 
				if y + i < planete.terrainTailleCarre:
					self.metauxgen += planete.terrainRessource[x][y+i].metaux
					#print(self.metauxgen)
			
	def calculenergiegen(self):
		
		planete=None
		
		joueur = self.parent.parent.joueurs[self.proprietaire]
		
		for s in joueur.systemesvisites:
			for p in s.planetes:
				if p.id == self.planeteid:
					planete = p
					break
					
		if planete:
			x = int(self.x)
			y = int(self.y)
			self.energiegen = planete.terrainRessource[x][y].energie
			#print(self.metauxgen)
			for i in range(self.range):
				if x - i >= 0:
					self.energiegen += planete.terrainRessource[x-i][y].energie
					#print(self.metauxgen)
					if y - i >= 0:
						self.energiegen += planete.terrainRessource[x-i][y-i].energie
						#print(self.metauxgen)
					if y + i < planete.terrainTailleCarre:
						self.energiegen += planete.terrainRessource[x-i][y+i].energie
						#print(self.metauxgen)
				if x + i < planete.terrainTailleCarre:
					self.energiegen += planete.terrainRessource[x+i][y].energie
					#print(self.metauxgen)
					if y - i >= 0:
						self.energiegen += planete.terrainRessource[x+i][y-i].energie
						#print(self.metauxgen)
					if y + i < planete.terrainTailleCarre:
						self.energiegen += planete.terrainRessource[x+i][y+i].energie
						#print(self.metauxgen)
				if y - i >= 0:
					self.energiegen += planete.terrainRessource[x][y-i].energie
					#print(self.metauxgen) 
				if y + i < planete.terrainTailleCarre:
					self.energiegen += planete.terrainRessource[x][y+i].energie
					#print(self.metauxgen)
