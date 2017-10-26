from orion_empire_modele import *


class Vaisseau():
	def __init__(self, parent, nom, systeme):
		self.parent = parent
		self.id = Id.prochainid()
		self.proprietaire = nom
		self.taille = 16
		# self.base = systeme
		self.angletrajet = 0
		self.degre = 0
		self.x = systeme.x
		self.y = systeme.y
		self.taille = 16
		self.cargo = 0
		self.energie = 100
		self.vitesse = random.choice([0.001, 0.003, 0.005, 0.01]) * 5  # 0.5
		self.cible = None
		# self.essence = (random.randrange(5) +5) * 100  # ------------------ essence entre 500 et 1000 unitee
		self.vaisseauxtransportee = []
		self.vie = 100
		self.niveau = 1
		self.systeme_courant = systeme

	def avancer(self):
		rep = None
		if self.cible:
			# if self.essence > 0: # -------------------------- s'il reste de l'essence, le vaisseau avance
			# self.essence -= 1 # -------------------------------- -1 unitee d'essence a chaque fois que le vaisseau avance
			x = self.cible.x
			y = self.cible.y
			self.x, self.y = hlp.getAngledPoint(self.angletrajet, self.vitesse, self.x, self.y)
			if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
				rep = self.cible
				self.systeme_courant = self.cible
				self.cible = None
			return rep
			# else: # ----------------------------------------- s'il n'y a plus d'essence, le vaisseau tombe en panne
			# print("Vaisseau ",self.id," : position ",self.x,",",self.y, " n'a plus d'essence!")
			# self.cible=None # ---------------------------- arrete d'essayer d'aller a sa cible destination

	def ciblerdestination(self, p):
		self.cible = p
		self.angletrajet = hlp.calcAngle(self.x, self.y, p.x, p.y)
		self.degre = 360 - hlp.calcDegre(self.x, self.y, p.x, p.y)
		dist = hlp.calcDistance(self.x, self.y, p.x, p.y)

	# print("Distance",dist," en ", int(dist/self.vitesse))

	def recevoir_dmg(self, dmg):
		if self.vie - dmg <= 0:
			self.meurt()
		else:
			self.vie -= dmg

	def meurt(self):
		pass

	def upgrade(self):
		self.niveau += 1

	def reparer(self, amnt):
		if self.vie > 0:
			self.vie += amnt

	def recycler(self):
		pass

	def sortir_systeme(self):
		pass

	def upgradeVitesse(self, boost):
		# print("upgrade vitesse")
		self.vitesse += boost
		pass


class VaisseauTransport(Vaisseau):
	def __init__(self, parent, nom, systeme):
		super().__init__(parent, nom, systeme)
		self.units = []
		self.max_units = 4

	def charger_unit(self, unit):
		if len(self.units) < self.max_units:
			self.units.append(unit)
		else:
			print("Trop de units dans le vaisseau, upgrade le vaisseau")

	def decharger_unit(self, id):
		i = 0
		for unit in self.units:
			i += 1
			if unit.id == id:
				return self.units.pop(i)


class VaisseauCombat(Vaisseau):
	def __init__(self, parent, nom, systeme):
		super().__init__(parent, nom, systeme)
		self.dmg = 5
		self.rayon = 10

	def attaquer(self):
		pass


class VaisseauGalactique(Vaisseau):
	def __init__(self, parent, nom, systeme):
		Vaisseau.__init__(self, parent, nom, systeme)
		self.vaisseauxtransportee = []

	def dechargervaisseaugalactique(self, systeme):
		# EN CONSTRUCTION #
		if len(self.vaisseauxtransportee) > 0:
			print("DECHARGEMENT VAISSEAU")
			etoile = systeme.etoile
			for v in self.vaisseauxtransportee:
				angle = randrange(360) / 360 * 2 * math.pi

				x, y = hlp.getAngledPoint(angle, etoile.taille, etoile.x, etoile.y)

				v.x = x
				v.y = y
				self.parent.vaisseauxinterplanetaires.append(v)
			self.vaisseauxtransportee.clear()

		else:
			print("AUCUN VAISSEAU TRANSPORTEE")
		pass

	def chargementvaisseau(self, vaisseau):
		self.vaisseauxtransportee.append(vaisseau)

	def avancer(self):
		rep = None
		if self.cible:
			# if self.essence > 0: # -------------------------- s'il reste de l'essence, le vaisseau avance
			# self.essence -= 1 # -------------------------------- -1 unitee d'essence a chaque fois que le vaisseau avance
			x = self.cible.x
			y = self.cible.y
			taille = 0
			if self.cible in self.parent.parent.systemes:
				taille = (self.cible.etoile.taille / 20)

			self.x, self.y = hlp.getAngledPoint(self.angletrajet, self.vitesse, self.x, self.y)
			dist = hlp.calcDistance(self.x, self.y, x, y) - taille
			if dist <= self.vitesse:
				rep = self.cible
				self.base = self.cible
				self.systeme_courant = self.cible  # ! MODIF ICI
				self.cible = None
			# ! ----------------------------- DEBUT MODIF
			elif self.systeme_courant:
				self.systeme_courant = None
			# ! -------------------------------- FIN MODIF
			return rep
