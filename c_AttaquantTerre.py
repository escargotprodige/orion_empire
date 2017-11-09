from IdMaker import *
from mathPlus import *
from enum import Enum

class AT_TYPE(Enum):
	LAZERBOI = 0
	FISTBOI = 1

class AttaquantTerre:
	def __init__(self, nom, x, y, nearRange, farRange, atk, hp, speed, defense, systemid, planeteid, proprietaire,
	             type):
		self.nearRange = nearRange
		self.farRange = farRange
		self.atk = atk
		self.defense = defense
		self.hp = hp
		self.speed = speed
		self.x = x
		self.y = y
		self.id = Id.prochainid()
		self.systemid = systemid
		self.planeteid = planeteid
		self.proprietaire = proprietaire
		self.nom = nom
		self.type = type
		self.target = None
		self.isTargetInRange = False

		self.targetPositionX = None
		self.targetPositionY = None

	def attaquer(self):
		# v�rifie s'il existe un target
		if self.target == None:
			pass

		# fait avancer l'Attaquant vers son target
		dist = distance(self.x, self.y, self.target.x, self.target.y)
		if (dist <= self.farRange and dist >= self.nearRange):
			self.avancer(self.target.x, self.target.y)
			self.isTargetInRange = False;
		else:
			self.isTargetInRange = True;

		# fait attaquer l'attaquant quand celui-ci est rendu a destination
		if (self.isTargetInRange):
			damage = self.atk - self.target.defense
			if (damage > 1):
				self.target.hp -= damage
			else:
				self.target.hp -= 1

	def avancer(self, x, y):
		dirVers = directionVers(self.x, self.y, x, y)
		self.x += dirVers[0]
		self.y += dirVers[1]

	def arboderBoat(self, target):
		pass
