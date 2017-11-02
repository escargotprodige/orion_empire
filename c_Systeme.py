from orion_empire_modele import *
from IdMaker import *


class Systeme():
	def __init__(self, parent, x, y):
		self.parent = parent
		self.id = Id.prochainid()
		# self.id=self.parent.createurId.prochainid()
		self.proprietaire = "inconnu"
		self.visiteurs = {}
		self.diametre = 50  # UA unite astronomique = 150000000km
		self.x = x
		self.y = y
		self.etoile = Etoile(self, x, y)
		self.planetes = []
		self.planetesvisites = []
		self.vaisseaux = []
		self.creerplanetes()

	def creerplanetes(self):
		systemeplanetaire = True
		# systemeplanetaire=random.randrange(5) # 4 chance sur 5 d'avoir des planetes
		if systemeplanetaire:
			nbplanetes = random.randrange(12) + 1
			for i in range(nbplanetes):
				type = random.choice(["roc", "gaz", "glace"])
				# distsol=random.randrange(250)/10 #distance en unite astronomique 150000000km

				taille = random.randrange(50) / 100 + 0.1  # en masse solaire # Taille planete

				distanceBool = True  # Distance incorrecte
				while (distanceBool):
					distsol = 0.0  # random.randrange(250)/10 #distance en unite astronomique 150000000km # Distance entre planete et soleil
					while (distsol < 1):
						distsol = random.randrange(
							250) / 10  # distance en unite astronomique 150000000km # Distance entre planete et soleil
					angle = random.randrange(360)  # angle de depart

					if len(
							self.planetes) > 1:  # and distsol > 0.5 : # Faut aumoins avoir une planete avant de checker et que la planete sois pas sur la soleil
						for i in range(len(self.planetes)):
							distanceBool = False
							if distsol <= self.planetes[i].distance - .2 and distsol >= self.planetes[
								i].distance + .2:  # Si fonctionne pas relancer la position
								distanceBool = True

					else:
						distanceBool = False

				self.planetes.append(Planete(self, type, distsol, taille, angle))
