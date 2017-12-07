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
		#self.vitesse = random.choice([ 0.1, 0.13,0.15,0.17]) * 5
		self.vitesse = 0.1 * 5

		self.x,self.y = hlp.getAngledPoint(math.radians(self.planete_courrant.angle),self.planete_courrant.distance,0,0)
		#print(self.x,self.y)
		self.type=type
		
	def avancer(self):
		rep = None
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
		#print("RUN")
		limitcadre = 25
		self.cible = None
		if self.planete_courrant:
			self.planete_courrant = None
		if self.type == 'combat' and self.cibleattaque:
			self.cibleattaque = None
		x = vaisseau.x
		y = vaisseau.y
		direction = hlp.calcDegre(self.x,self.y,x,y) - 180
		if direction < 0:
			direction += 360
			
		self.angletrajet = math.radians(direction)
		self.degre = 360 - direction
		px,py = hlp.getAngledPoint(math.radians(direction), self.vitesse, self.x, self.y)
		#print(px,py)
		while px >= limitcadre or px <= -limitcadre or py >= limitcadre or py <= -limitcadre:
			
			direction  = direction  +45
			if direction  >= 360:
				direction  -= 360
				
			self.degre = 360 - direction
			self.angletrajet = math.radians(direction)
			
			px,py = hlp.getAngledPoint(math.radians(direction), self.vitesse, self.x, self.y)
			#print(px,py)
			
		self.x,self.y = px,py

class VaisseauTransport(VaisseauSolaire):
	def __init__(self, parent, nom, systeme,planete):
		VaisseauSolaire.__init__(self,parent, nom, systeme,planete,"transport")
		self.units = []
		self.max_units = 4

	def charger_unit(self, unit):
		if len(self.units) < self.max_units:
			unit.planeteid = None
			unit.systemeid = None
			self.units.append(unit)
			print("UNIT CHARGEE")
		else:
			print("Trop de units dans le vaisseau, upgrade le vaisseau")

	def decharger_unit(self, id):
		i = 0
		for unit in self.units:
			i += 1
			if unit.id == id:
				return self.units.pop(i)
			
	def dechargerDansPlanete(self,planete):
		if len(self.units) > 0:
			for u in self.units:
				u.planeteid = self.planete_courrant.id
				u.systemeid = self.systeme_courant
				
				self.parent.attaquantTerre.append(u)
			self.units.clear()
			print("DECHARGER")
		else:
			print("AUCUN UNITS")
		
		pass

class VaisseauCombat(VaisseauSolaire):
	def __init__(self, parent, nom, systeme,planete):
		VaisseauSolaire.__init__(self,parent, nom, systeme,planete,"combat")
		self.dmg = 5
		self.rayon = 5
		self.cibleattaque = None
		self.agressif = False

	def attaquer(self):
		if self.cibleattaque:
			self.cibleattaque.recevoir_dmg(self.dmg)
			if not self.cibleattaque.cible:
				if self.cibleattaque.type == 'combat' and self.cibleattaque.agressif:
					self.cibleattaque.ciblerdestination(self)
				else:
					self.parent.parent.enfuireVaisseauSolaire(self.cibleattaque,self)

			x = self.cibleattaque.x
			y = self.cibleattaque.y
			if hlp.calcDistance(x,y,self.x,self.y) > self.rayon:
				self.cible = self.cibleattaque
				self.cibleattaque = None
				
			elif self.cibleattaque.vie <= 0:
				self.cible = None
				self.cibleattaque = None
				
	def changeretatvaisseau(self):
		if self.agressif:
			self.agressif = False
		else:
			self.agressif = True

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

def getCoutMvg():
	return 10000
def getCoutEvg():
	return 2000

class VaisseauGalactique(Vaisseau):
	def __init__(self, parent, nom, systeme):
		Vaisseau.__init__(self, parent, nom, systeme)
		self.vaisseauxtransportee = []
		self.vitesse = random.choice([0.001, 0.003, 0.005, 0.01]) * 5 
		self.coutM = getCoutMvg()
		self.coutE = getCoutEvg()

	def dechargervaisseaugalactique(self, systeme):
		# EN CONSTRUCTION #
		if len(self.vaisseauxtransportee) > 0:
			print("DECHARGEMENT VAISSEAU")
			etoile = systeme.etoile
			for v in self.vaisseauxtransportee:
				x = 0
				y = 0
				angle = random.randrange(360)
	
				x, y = hlp.getAngledPoint(math.radians(angle), etoile.taille, 0, 0)
					
				v.x = x
				v.y = y
					
				v.systeme_courant = self.systeme_courant
				self.parent.vaisseauxinterplanetaires.append(v)
					
					
			self.vaisseauxtransportee.clear()

		else:
			print("AUCUN VAISSEAU TRANSPORTEE")
		pass

	def chargementvaisseau(self, vaisseau):
		vaisseau.systeme_courant = None
		vaisseau.planete_courrant = None
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
 		
	def ciblerdestination(self, p):
		self.cible = p
		self.angletrajet = hlp.calcAngle(self.x, self.y, p.x, p.y)
		self.degre = 360 - hlp.calcDegre(self.x, self.y, p.x, p.y)
		dist = hlp.calcDistance(self.x, self.y, p.x, p.y)
