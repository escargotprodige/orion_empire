from orion_empire_modele import *
import random
from mathPlus import *
from IdMaker import Id
import numpy as np


#
class Ressource:
	def __init__(self):
		self.metaux = 0
		self.energie = 0
		self.food = 0


class Planete():
	def __init__(self, parent, type, dist, taille, angle):
		self.parent = parent
		self.id = Id.prochainid()
		#self.parent = parent
		self.posXatterrissage = random.randrange(5000)
		self.posYatterrissage = random.randrange(5000)
		self.infrastructures = []  # A CONTINUER
		self.proprietaire = "inconnu"
		self.visiteurs = {}
		self.distance = dist
		self.type = type
		self.taille = taille
		self.angle = angle

		self.detailLevel = 8
		self.terrainTailleCarre = pow(2, self.detailLevel) + 1

		self.elevationMax = 255
		self.roughness = 8
		
		self.couleurPlanete = 0

		self.terrain = list(np.zeros((self.terrainTailleCarre, self.terrainTailleCarre))) #[[0 for x in range(self.terrainTailleCarre)] for y in range(self.terrainTailleCarre)]
		self.terrainColor = list(np.full((self.terrainTailleCarre, self.terrainTailleCarre), '#000000'))#[['#000000' for x in range(self.terrainTailleCarre)] for y in
							 #range(self.terrainTailleCarre)]

		self.terrainRessource = list(np.full((self.terrainTailleCarre, self.terrainTailleCarre), Ressource() ))#[[Ressource() for x in range(self.terrainTailleCarre)] for y in
								 #range(self.terrainTailleCarre)]

		self.genTerrain()
		self.genTerrainColor()

		self.genTerrainRessource()

		self.parent.parent.parent.vue.attenteloading()

		self.delais = 5
		
		
	def genTerrain(self):
		size = self.terrainTailleCarre
		#for n in range(self.terrainTailleCarre * self.terrainTailleCarre):
		#	self.terrain.append(0)
		self.terrain[0][0] = self.elevationMax / 2
		self.terrain[size - 1][0] = self.elevationMax / 2
		self.terrain[size - 1][size - 1] = self.elevationMax / 2
		self.terrain[0][size - 1] = self.elevationMax / 2

		self.divideHeightMap(self.terrainTailleCarre)

	def divideHeightMap(self, size):

		half = int(size / 2)
		if half < 1:
			return

		scale = self.roughness * size

		for i in range(half, self.terrainTailleCarre, size):
			for j in range(half, self.terrainTailleCarre, size):
				self.squareStep(i, j, half, random.random() * scale * 2 - scale)
		for i in range(0, self.terrainTailleCarre, half):
			for j in range((i + half) % size, self.terrainTailleCarre, size):
				self.diamondStep(i, int(j), half, random.random() * scale * 2 - scale)

		self.divideHeightMap(int(size / 2))

	def squareStep(self, x, y, size, variation):
		topLeft = self.terrain[x - size][y - size]
		topRight = self.terrain[x + size][y - size]
		bottomRight = self.terrain[x + size][y + size]
		bottomLeft = self.terrain[x - size][y + size]

		self.terrain[x][y] = (topLeft + topRight + bottomLeft + bottomRight) / 4 + variation
		if self.terrain[x][y] > self.elevationMax:
			self.terrain[x][y] = self.elevationMax

	def diamondStep(self, x, y, size, variation):
		var = 0
		c = 0
		if y - size >= 0:
			var += self.terrain[x][y - size]
			c += 1
		if x + size < self.terrainTailleCarre:
			var += self.terrain[x + size][y]
			c += 1
		if y + size < self.terrainTailleCarre:
			var += self.terrain[x][y + size]
			c += 1
		if x - size >= 0:
			var += self.terrain[x - size][y]
			c += 1

		self.terrain[x][y] = var / c + variation
		if self.terrain[x][y] > self.elevationMax:
			self.terrain[x][y] = self.elevationMax

	def genTerrainColor(self):
		normalizeDist = self.distance / 25
		r = 1 - normalizeDist
		b = 1 - (1 - normalizeDist)
		g = r * b
		r -= g / 2
		b -= g / 2
		
		self.couleurPlanete = self.rgbToHex(255*r, 255*g*2, 255*b);
		
		

		waterlevel = 0
		if (r > b):
			waterlevel = (r * b) - 0.25  # le niveau de l'eau
		else:
			waterlevel = (b) - 0.25

		waterlevel *= 255

		elevationLevelUn = waterlevel + (255 - waterlevel) / 4  # 1/4 de ce qu'il reste
		elevationLevelDeux = elevationLevelUn + ((255 - waterlevel) / 4) * 3  # 3/4 de ce qu'il reste
		for x in range(self.terrainTailleCarre):
			for y in range(self.terrainTailleCarre):
				if (self.terrain[x][y] < waterlevel):
					self.terrainColor[x][y] = self.rgbToHex(r * 10, g * self.terrain[x][y] + 50,
															b * self.terrain[x][y] + 120)
				elif (self.terrain[x][y] <= elevationLevelUn):
					self.terrainColor[x][y] = self.rgbToHex(r * self.terrain[x][y] * 3, g * self.terrain[x][y] * 3,
															b * self.terrain[x][y])
				elif (self.terrain[x][y] <= elevationLevelDeux):
					self.terrainColor[x][y] = self.rgbToHex(r * self.terrain[x][y] * 0.9, g * self.terrain[x][y] * 1.2,
															b * self.terrain[x][y] / 4)
				else:
					self.terrainColor[x][y] = self.rgbToHex(r * self.terrain[x][y] * 0.9, g * self.terrain[x][y] * 1.2,
															b * self.terrain[x][y] / 3)

	def hexToRgb(self, hex):
		t = hex.lstrip('#')
		return tuple(int(t[i:i + 2], 16) for i in (0, 2, 4))

	def genTerrainRessource(self):
		for i in range(len(self.terrainColor)):
			for j in range(len(self.terrainColor[i])):
				self.terrainRessource[i][j].metaux = self.hexToRgb(self.terrainColor[i][j])[0]  # red
				self.terrainRessource[i][j].energie = self.hexToRgb(self.terrainColor[i][j])[1]  # green
				self.terrainRessource[i][j].food = self.hexToRgb(self.terrainColor[i][j])[2]  # blue

	def rgbToHex(self, r, g, b):
		if r < 0:
			r = 0
		if g < 0:
			g = 0
		if b < 0:
			b = 0
		if r > 255:
			r = 255
		if g > 255:
			g = 255
		if b > 255:
			b = 255
		hex = '#%02x%02x%02x' % (r, g, b)
		return hex

	def orbiter(self):
		self.delais -= 1
		if self.delais <= 0:
			self.delais = 5
			self.angle += 1
			if self.angle >= 360:
				self.angle = 0
