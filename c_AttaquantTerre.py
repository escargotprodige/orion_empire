from IdMaker import *
from mathPlus import *
from test.test_threading_local import target


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
		self.dir = directionVers(x, y, x, y)

		self.targetPositionX = None
		self.targetPositionY = None

	def setTarget(self, target):
		self.target = target
		self.targetPositionX = None
		self.targetPositionY = None

	def setTargetPosition(self, x, y):
		self.targetPositionX = x
		self.targetPositionY = y
		self.target = None
		
		
	def attaquer(self):
		# v�rifie s'il existe un target
		if self.target == None:
			return

		# fait avancer l'Attaquant vers son target
		dist = distance(self.x, self.y, self.target.x, self.target.y)
		if (dist >= self.farRange and dist <= self.nearRange):
			self.avancer(self.target.x, self.target.y)
			self.isTargetInRange = False;
		else:
			self.isTargetInRange = True;

		# fait attaquer l'attaquant quand celui-ci est rendu a destination
		if (self.isTargetInRange):
			damage = self.atk - target.defense
			if (damage > 1):
				target.hp -= damage
			else:
				target.hp -= 1

	def move(self):
		if self.targetPositionX == None or self.targetPositionY == None:
			return
		
		dist = distance(self.x, self.y, self.targetPositionX, self.targetPositionY)
		if dist < 1:
			return

		self.avancer(self.targetPositionX, self.targetPositionY)
		
	def avancer(self, x, y):
		self.dir = directionVers(self.x, self.y, x, y)
		self.x += self.dir[0]
		self.y += self.dir[1]
	
	def update(self):
		self.attaquer()
		self.move()
		
	def arboderBoat(self, target):
		pass
