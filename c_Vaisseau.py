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
		self.vitesse = 0  # 0.5
		self.cible = None
		# self.essence = (random.randrange(5) +5) * 100  # ------------------ essence entre 500 et 1000 unitee
		#self.vaisseauxtransportee = []
		self.vie = 100
		self.niveau = 1
		self.systeme_courant = systeme
		self.enfuire = None
		
	def avancer(self):
		pass
	
	def ciblerdestination(self,p):
		pass

	"""
=======
		self.vitesse = random.choice([0.001, 0.003, 0.005, 0.01]) * 5  # 0.5
		self.cible = None
		# self.essence = (random.randrange(5) +5) * 100  # ------------------ essence entre 500 et 1000 unitee
		self.vaisseauxtransportee = []
		self.vie = 100
		self.niveau = 1
		self.systeme_courant = systeme

>>>>>>> affichage menu selection
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
<<<<<<< HEAD
	
"""
	def recevoir_dmg(self, dmg):
		self.vie -= dmg

	def meurt(self):
		print(self.id,"est mort!")
		self.parent.vaisseauxinterplanetaires.remove(self)

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
					

class VaisseauSolaire(Vaisseau):
	def __init__(self,parent,nom,systeme,planete,type):
		Vaisseau.__init__(self,parent,nom,systeme)
		self.planete_courrant=planete
		self.vitesse = random.choice([0.01, 0.03, 0.05, 0.1]) * 5

		self.x,self.y = hlp.getAngledPoint(math.radians(self.planete_courrant.angle),self.planete_courrant.distance,0,0)
		#print(self.x,self.y)
		self.type=type
		
	def avancer(self):
		rep = None
		if self.enfuire:
			#print("RUN")
			self.cible = None
			if self.type == 'combat' and self.cibleattaque:
				self.cibleattaque = None
			x = self.enfuire.x
			y = self.enfuire.y
			direction = hlp.calcDegre(self.x,self.y,x,y) - 180
			if direction < 0:
				direction += 360
				
			self.angletrajet = math.radians(direction)
			self.degre = 360 - direction
			self.x, self.y = hlp.getAngledPoint(direction, self.vitesse, self.x, self.y)
			self.enfuire = None
		elif self.cible:
			#print("avance")
			x = 0
			y = 0
			if type(self.cible) is Planete:
				x,y =  hlp.getAngledPoint(math.radians(self.cible.angle),self.cible.distance,0,0)
				
			elif isinstance(self.cible, VaisseauSolaire):
				x = self.cible.x
				y = self.cible.y
				
			self.x, self.y = hlp.getAngledPoint(self.angletrajet, self.vitesse, self.x, self.y)
			
			self.ciblerdestination(self.cible)
			if hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
				rep = self.cible
				if type(self.cible) is Planete:
					self.planete_courrant = self.cible
				self.cible = None
			return rep
		
	
	def ciblerdestination(self,p):
		self.enfuire = None
		if not self.cible:
			self.cible = p
			self.planete_courrant = None
		x =0
		y = 0
		if type(p) is Planete:
			x,y = hlp.getAngledPoint(math.radians(p.angle),p.distance,0,0)
			self.cibleattaque = None
		elif isinstance(p, VaisseauSolaire):
			x = p.x
			y = p.y
			if self.type == 'combat' and hlp.calcDistance(self.x,self.y,x,y) <= self.rayon:
				self.cibleattaque = p
			else:
				self.cibleattaque =None
			
		self.angletrajet = hlp.calcAngle(self.x, self.y, x, y)
		self.degre = 360 - hlp.calcDegre(self.x, self.y, x, y)
		#dist = hlp.calcDistance(self.x, self.y, p.x, p.y)
		
	def orbite(self):
		if self.planete_courrant:
			self.x,self.y = hlp.getAngledPoint(math.radians(self.planete_courrant.angle),self.planete_courrant.distance+self.planete_courrant.taille,0,0)
		
	def runaway(self,vaisseau):
		self.enfuire = vaisseau
			

class VaisseauTransport(VaisseauSolaire):
	def __init__(self, parent, nom, systeme,planete):
		super().__init__(parent, nom, systeme,planete,"transport")
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

class VaisseauCombat(VaisseauSolaire):
	def __init__(self, parent, nom, systeme,planete):
		super().__init__(parent, nom, systeme,planete,"combat")
		self.dmg = 5
		self.rayon = 5
		self.cibleattaque = None
		self.agressif = False

	def attaquer(self):
		if self.cibleattaque:
			self.cibleattaque.recevoir_dmg(self.dmg)
			if self.cibleattaque.type == 'combat' and self.cibleattaque.agressif:
				self.cibleattaque.ciblerdestination(self)
			else:
				self.cibleattaque.runaway(self)
				#print("Run Attaque")
				#self.cibleattaque.runaway(self)
			x = self.cibleattaque.x
			y = self.cibleattaque.y
			if hlp.calcDistance(x,y,self.x,self.y) > self.rayon:
				self.cible = self.cibleattaque
				self.cibleattaque = None
				
			elif self.cibleattaque.vie <= 0:
				self.cible = None
				self.cibleattaque = None

		"""		
		else:
			for j in self.parent.parent.joueurscles:
				if j != self.proprietaire:
					j = self.parent.parent.joueurs[j]
					for v in j.vaisseauxinterplanetaires:
						if hlp.calcDistance(self.x,self.y,v.x,v.y) <= self.rayon:
							self.cibleattaque = v
							break
					if self.cibleattaque:
						break
		"""

class VaisseauGalactique(Vaisseau):
	def __init__(self, parent, nom, systeme):
		Vaisseau.__init__(self, parent, nom, systeme)
		self.vaisseauxtransportee = []
		self.vitesse = random.choice([0.001, 0.003, 0.005, 0.01]) * 5 

	def dechargervaisseaugalactique(self, systeme):
		# EN CONSTRUCTION #
		if len(self.vaisseauxtransportee) > 0:
			print("DECHARGEMENT VAISSEAU")
			etoile = systeme.etoile
			for v in self.vaisseauxtransportee:
				angle = random.randrange(360) / 360 * 2 * math.pi

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
# <<<<<<< HEAD
# 		
# 	def ciblerdestination(self, p):
# 		self.cible = p
# 		self.angletrajet = hlp.calcAngle(self.x, self.y, p.x, p.y)
# 		self.degre = 360 - hlp.calcDegre(self.x, self.y, p.x, p.y)
# 		dist = hlp.calcDistance(self.x, self.y, p.x, p.y)
# =======
# >>>>>>> affichage menu selection
