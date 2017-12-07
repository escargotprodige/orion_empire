
from orion_empire_modele import *
import c_Vaisseau
from c_StationGalactique import StationGalactique
from c_Station import Station
from Couts import *

class Joueur():
	def __init__(self, parent, nom, systemeorigine, couleur):
		self.parent = parent
		self.id = Id.prochainid()
		# self.id=parent.createurId.prochainid()
		self.artificiel = 0  # IA
		self.nom = nom
		self.systemeorigine = systemeorigine
		self.couleur = couleur
		self.systemesvisites = [systemeorigine]
		self.vaisseauxinterstellaires = []
		self.vaisseauxinterplanetaires = []
		self.stationGalactiques = []
		self.actions = {"creervaisseauGalactique": self.creervaisseauGalactique,
		                "ciblerdestination": self.ciblerdestination,
		                "atterrirplanete": self.atterrirplanete,
		                "visitersysteme": self.visitersysteme,
		                "creermine": self.creermine,
		                "creerville": self.creerville,
		                "creergeneratrice": self.creergeneratrice,
		                "creerferme": self.creerferme,
		                "dechargervausseaugalactique": self.dechargervaisseaugalactique,
		                "creerstationGalactique": self.creerstationGalactique,
		                "creerstationSolaire": self.creer_station,
		                "upgradevitessevaisseau": self.upgradeVitesseVaisseau,
		                "creerbarrack": self.creerbarrack,
		                "creerlazerboi": self.creerLazerBoi,
		                "creervaisseauSolaire": self.creervaisseauSolaire,
		                "movelazerboi": self.moveLazerBoi,
		                "enfuireVaisseauSolaire": self.enfuireVaisseauSolaire,
		                "changeretatvaisseau": self.changeretatvaisseau,
		                "vaisseaumort": self.vaisseaumort,
		                "lazerboiumort": self.lazerboimort,
		                "attacklazerboi": self.attackLazerBoi
		                }

		# self.stationGalactiques = []
		self.stationSolaire = []
		self.barrackMere = None

		# self.stationGalactiques = []
		# self.barrackMere = None

		self.planeteOrigine = random.choice(self.systemeorigine.planetes)
		self.planeteOrigine.proprietaire = self.nom
		# self.creerVilleOrigine()

		self.barrackMere = Barrack(self, "barrack" + self.nom, None, None, -1, -1)
		self.attaquantTerre = []
		self.ressourcesTEMP = 100

		self.ressourceM = 1000
		self.ressourceE = 1000
		self.ressourceN = 1000

		self.delais = 20
	
	def printRessource(self):
		print('Ressource----------------------')
		print('Energie ')
		print(self.ressourceE)
		print('Metal ')
		print(self.ressourceM)
		print('Nourriture ')
		print(self.ressourceN)
		print('-------------------------------')
		
	def creerVilleOrigine(self):
		ville = Ville(self, self.nom, self.systemeorigine, self.planeteOrigine, 25, 25)  ### TEST ICI  ###
		self.planeteOrigine.infrastructures.append(ville)

		# Choisir X Y pour ville
		# coords[]

		self.parent.parent.afficherBatiment(ville)  ### TEST ICI  ###

	# return coords

	def creervaisseauSolaire(self, listeparams):
		if self.haveFunds("creervaisseauSolaire",listeparams[2]):
			dict_vaisseau = {0: VaisseauTransport,
			                 1: VaisseauCombat}
	
			systemeid, planeteid, type_vaisseau = listeparams
			print("creer vaisseau solaire", systemeid, planeteid, type_vaisseau)
			for i in self.systemesvisites:
				if i.id == systemeid:
					for j in i.planetes:
						if j.id == planeteid:
							# print(i,j)
							v = dict_vaisseau[type_vaisseau](self, self.nom, i, j)
							self.vaisseauxinterplanetaires.append(v)
							return 1

	# ajout
	def creer_infrastructure(self, nom, systemeid, planeteid, x, y, type_infrastructure):
		for i in self.systemesvisites:
			if i.id == systemeid:
				for j in i.planetes:
					if j.id == planeteid:
						infrastructure = type_infrastructure(self, nom, systemeid, planeteid, x, y)
						j.infrastructures.append(infrastructure)
						self.parent.parent.afficherBatiment(infrastructure)

	def creermine(self, listeparams):
		if self.haveFunds("creermine"):
			nom, systemeid, planeteid, x, y = listeparams
			for i in self.systemesvisites:
				if i.id == systemeid:
					for j in i.planetes:
						if j.id == planeteid:
							mine = Mine(self, nom, systemeid, planeteid, x, y)
							j.infrastructures.append(mine)
							# self.parent.parent.affichermine(nom,systemeid,planeteid,x,y)
							self.parent.parent.afficherBatiment(mine)

	def creerville(self, listeparams):
		if self.haveFunds("creerville"):
			nom, systemeid, planeteid, x, y = listeparams
			for i in self.systemesvisites:
				if i.id == systemeid:
					for j in i.planetes:
						if j.id == planeteid:
							ville = Ville(self, nom, systemeid, planeteid, x, y)
							j.infrastructures.append(ville)
							# self.parent.parent.afficherville(nom,systemeid,planeteid,x,y)
							self.parent.parent.afficherBatiment(ville)

	def creerferme(self, listeparams):
		if self.haveFunds("creerville"):
			nom, systemeid, planeteid, x, y = listeparams
			for i in self.systemesvisites:
				if i.id == systemeid:
					for j in i.planetes:
						if j.id == planeteid:
							ferme = Ferme(self, nom, systemeid, planeteid, x, y)
							j.infrastructures.append(ferme)
							# self.parent.parent.afficherferme(nom,systemeid,planeteid,x,y)
							self.parent.parent.afficherBatiment(ferme)

	def creergeneratrice(self, listeparams):
		if self.haveFunds("creergeneratrice"):
			nom, systemeid, planeteid, x, y = listeparams
			for i in self.systemesvisites:
				if i.id == systemeid:
					for j in i.planetes:
						if j.id == planeteid:
							generatrice = Generatrice(self, nom, systemeid, planeteid, x, y)
							j.infrastructures.append(generatrice)
							# self.parent.parent.afficherferme(nom,systemeid,planeteid,x,y)
							self.parent.parent.afficherBatiment(generatrice)
	
						# ! MODIF

	def creerbarrack(self, listeparams):
		if self.haveFunds("creerbarrack"):
			nom, systemeid, planeteid, x, y = listeparams
			for i in self.systemesvisites:
				if i.id == systemeid:
					for j in i.planetes:
						if j.id == planeteid:
							barrack = Barrack(self, nom, systemeid, planeteid, x, y)
	
							if self.barrackMere:
								barrack.setBarrackMere(self.barrackMere)
							else:
								self.barrackMere = barrack
							j.infrastructures.append(barrack)
							# self.parent.parent.afficherferme(nom,systemeid,planeteid,x,y)
							self.parent.parent.afficherBatiment(barrack)

	def atterrirplanete(self, d):
		nom, systeid, planeid = d
		for i in self.systemesvisites:
			if i.id == systeid:
				for j in i.planetes:
					if j.id == planeid:
						i.planetesvisites.append(j)
						if nom == self.parent.parent.monnom:
							self.parent.parent.voirplanete(i.id, j.id)
						return 1

	def visitersysteme(self, systeme_id):
		for i in self.parent.systemes:
			if i.id == systeme_id:
				self.systemesvisites.append(i)

	def creervaisseauGalactique(self, id):
		if self.ressourceM >= getCoutMvg() and self.ressourceE >= getCoutEvg():
			for i in self.systemesvisites:
				if len(self.stationGalactiques)>0:
					for station in self.stationGalactiques:
						if i.id == id and station.systemeOrigine.id == i.id:
							v = VaisseauGalactique(self, self.nom, i)
							self.ressourceM -= v.coutM
							self.ressourceE -= v.coutE
							self.printRessource()
							self.vaisseauxinterstellaires.append(v)
							return 1
				else:
					print('vous n avez pas de station sur se systeme' )
				
			print('vous n avez pas de station sur se systeme' )
		else:
			print("Tu es trop pauvre!")
			
	def creerstationGalactique(self,id):
		if self.ressourceM >= getCoutMsg() and self.ressourceE >= getCoutEsg():
			for i in self.systemesvisites:
				if i.id == id:
					sg = StationGalactique(self, self.nom, i, i.x, i.y)
					self.ressourceM -= sg.coutM
					self.ressourceE -= sg.coutE
					self.printRessource()
					self.stationGalactiques.append(sg)
					
					return 1
		else:
			print("Tu es trop pauvre!")

	def creerstationSolaire(self, id):
		if self.haveFunds("stationSolaire"):
			for i in self.systemesvisites:
				if i.id == id:
					ss = Station(self, self.nom, i, i.x, i.y)
					self.stationSolaire.append(ss)
					self.transaction()
					print(self.stationSolaire)
					return 1

	def creer_station(self, liste_params):
		systeme_id, planete_id = liste_params
		for i in self.systemesvisites:
			if i.id == systeme_id:
				for j in i.planetes:
					if j.id == planete_id:
						x, y = hlp.getAngledPoint(math.radians(j.angle), j.distance, 0, 0)
						sg = Station(j, self.nom, i, x, y)
						self.stationSolaire.append(sg)
						return 1

	def creerLazerBoi(self, listeparams):
		if self.haveFunds("creerlazerboi"):
			nom, systemeid, planeteid, x, y = listeparams
			for i in self.systemesvisites:
				if i.id == systemeid:
					for j in i.planetes:
						if j.id == planeteid:
							lazerboi = self.barrackMere.creerLazerBoi(self.nom)
							lazerboi.x = x
							lazerboi.y = y
							print(str(lazerboi.x) + ", " + str(lazerboi.y))
							lazerboi.systemid = systemeid
							lazerboi.planeteid = planeteid
							self.attaquantTerre.append(lazerboi)
							self.parent.parent.afficherLazerBoi(lazerboi)


	def moveLazerBoi(self, listparams):
		lazerboi_id, x, y = listparams
		for at in self.attaquantTerre:
			if at.id == lazerboi_id:
				at.setTargetPosition(x, y)
			
	def attackLazerBoi(self, listparams):
		lazerboi_id, lazerboiEnemy = listparams
		for at in self.attaquantTerre:
			if at.id == lazerboi_id:
				for j in self.parent.joueurs:
					for at_enemi in self.parent.joueurs[j].attaquantTerre:
						if lazerboiEnemy == at_enemi.id:	
							at.setTarget(at_enemi)

	def ciblerdestination(self, ids):
		idori, iddesti = ids
		for i in self.vaisseauxinterstellaires:
			if i.id == idori:
				for j in self.parent.systemes:
					if j.id == iddesti:
						# i.cible=j
						i.ciblerdestination(j)
						return
				for j in self.systemesvisites:
					if j.id == iddesti:
						# i.cible=j
						i.ciblerdestination(j)
						return
				for j in self.parent.pulsars:
					if j.id == iddesti:
						i.ciblerdestination(j)
						return

		for i in self.vaisseauxinterplanetaires:
			if i.id == idori:
				for j in i.systeme_courant.planetes:
					if j.id == iddesti:
						i.ciblerdestination(j)
						return
				for k in self.parent.joueurscles:
					for j in self.parent.joueurs[k].vaisseauxinterplanetaires:
						if j.id == iddesti:
							i.ciblerdestination(j)

	def prochaineaction(self):  # NOTE : cette fonction sera au coeur de votre developpement
		for i in self.vaisseauxinterstellaires:
			if i.cible:
				rep = i.avancer()
				if rep:
					if rep in self.parent.systemes:  # ------------------------ verifie si la cible est un systeme
						if rep not in self.systemesvisites:
							self.systemesvisites.append(rep)
							if self.nom == self.parent.parent.monnom:
								self.parent.changeetatsystem(self.nom, rep)
					elif rep in self.parent.pulsars:  # ---------------------------- verifie si la cible est une pulsar
						# ----------------------------------------Teleporte vaisseau vers autre pulsar au hazard
						teleport = random.choice(self.parent.pulsars)
						while teleport == rep:
							teleport = random.choice(self.parent.pulsars)
						i.x = teleport.x
						i.y = teleport.y
						print(i.id, " >> TELEPORTE VERS PULSAR ", teleport)

						if self.nom == self.parent.parent.monnom:
							if self.parent.parent.vue.modecourant == self.parent.parent.vue.modes["galaxie"]:
								self.parent.parent.vue.deplacerCanevas(i.x, i.y)

		for i in self.vaisseauxinterplanetaires:
			if i.cible:
				rep = i.avancer()
				if rep:
					print(rep)
			else:
				i.orbite()

			if i.type == 'combat':
				i.attaquer()

			if i.vie <= 0:
				# i.meurt()
				self.parent.vaisseaumort(i.id)

		self.delais = self.delais - 1
		if self.delais <= 0:
			self.delais = 20
			for s in self.systemesvisites:
				for p in s.planetes:
					for i in p.infrastructures:
						if i.proprietaire == self.nom:
							i.generer()
						# print(self.ressource1,self.ressource2,self.ressource3)

		for at in self.attaquantTerre:
			at.update()
			
		for at in self.attaquantTerre:
			if at.isDead():
				self.parent.lazerboimort(at.id)

	def dechargervaisseaugalactique(self, rep):
		v = None
		s = None
		for i in self.vaisseauxinterstellaires:
			if i.id == rep[0]:
				v = i
				break
		for i in self.parent.systemes:
			if i.id == rep[1]:
				s = i
				break
		if s and v:
			v.dechargervaisseaugalactique(s)

	def upgradeVitesseVaisseau(self, rep):
		id = rep[0]
		ajout = rep[1]
		v = None

		# print(self.nom,"UPGRADE VAISSEAU",id)

		for i in self.vaisseauxinterstellaires:
			if id == i.id:
				v = i
				break

		if v:
			#  print("UPGRADE VITESSE VAISSEAU",id)
			v.upgradeVitesse(ajout)

	def chargementdansvaisseaugalactique(self, rep):
		vg = rep[0]
		vs = rep[1]

		print("CHARGEMENT VAISSEAU", vs, "DANS", vg)

		for i in self.vaisseauxinterstellaires:
			if vg == i.id:
				vg == i
				break

		for i in self.vaisseauxinterplanetaires:
			if vs == i.id:
				vs = i
				break

		vg.chargementvaisseau(vs)

		self.vaisseauxinterstellaires.pop(vs)

	def ajoutessource(self, metaux=0, energie=0, food=0):
		self.ressourceM += metaux
		self.ressourceE += energie
		self.ressourceN += food

	def enfuireVaisseauSolaire(self, ids):
		idv, ida = ids

		vaisseau = None
		attaque = None

		for v in self.vaisseauxinterplanetaires:
			if v.id == idv:
				vaisseau = v
				break
		if vaisseau:
			for j in self.parent.joueurscles:
				for v in self.parent.joueurs[j].vaisseauxinterplanetaires:
					if v.id == ida:
						vaisseau.runaway(v)
						attaque = v
						break
			if attaque:
				for v in self.vaisseauxinterplanetaires:
					if v.id != idv and v.systeme_courant == vaisseau.systeme_courant:
						if v.type == "combat" and v.agressif:
							v.ciblerdestination(attaque)

	def changeretatvaisseau(self, idv):
		for v in self.vaisseauxinterplanetaires:
			if v.id == idv:
				if v.type == "combat":
					v.changeretatvaisseau()
				break

	def vaisseaumort(self, idv):
		for v in self.vaisseauxinterplanetaires:
			if v.id == idv:
				if self.nom == self.parent.parent.monnom:
					self.parent.parent.vue.vaisseaumort(v)
				v.meurt()
				break
	
	def removeFunds(self,ressourceM,ressourceE,ressourceN): #Girls wanna keep fun
		self.ressourceM += ressourceM
		self.ressourceE += ressourceE
		self.ressourceN += ressourceN
		
	def haveFunds(self,objetACree,params = None): #Girls wanna have fun
		#print("haveFunds")
		c = Cout()
		print(params)
		if objetACree == "creervaisseauSolaire":
			if params == 0:
				if abs(c.vSTransport["metal"]) <= self.ressourceM:
					if abs(c.vSTransport["energie"]) <= self.ressourceE:
						if abs(c.vSTransport["nourriture"]) <= self.ressourceN:
							self.removeFunds(c.vSTransport["metal"],c.vSTransport["energie"],c.vSTransport["nourriture"])
							return True
			elif params == 1:
				if abs(c.vSCombat["metal"]) <= self.ressourceM:
					if abs(c.vSCombat["energie"]) <= self.ressourceE:
						if abs(c.vSCombat["nourriture"]) <= self.ressourceN:
							self.removeFunds(c.vSCombat["metal"],c.vSCombat["energie"],c.vSCombat["nourriture"])
							return True
		#elif objetACree == "creervaisseauGalactique":
			#pass
		elif objetACree == "creermine":
			if abs(c.mine["metal"]) <= self.ressourceM:
				if abs(c.mine["energie"]) <= self.ressourceE:
					if abs(c.mine["nourriture"]) <= self.ressourceN:
						self.removeFunds(c.mine["metal"],c.mine["energie"],c.mine["nourriture"])
						return True
						
		elif objetACree == "creerville":
			if abs(c.ville["metal"]) <= self.ressourceM:
				if abs(c.ville["energie"]) <= self.ressourceE:
					if abs(c.ville["nourriture"]) <= self.ressourceN:
						self.removeFunds(c.ville["metal"],c.ville["energie"],c.ville["nourriture"])
						return True
		elif objetACree == "creergeneratrice":
			if abs(c.generatrice["metal"]) <= self.ressourceM:
				if abs(c.generatrice["energie"]) <= self.ressourceE:
					if abs(c.generatrice["nourriture"]) <= self.ressourceN:
						self.removeFunds(c.generatrice["metal"],c.generatrice["energie"],c.generatrice["nourriture"])
						return True
		elif objetACree == "creerferme":
			if abs(c.ferme["metal"]) <= self.ressourceM:
				if abs(c.ferme["energie"]) <= self.ressourceE:
					if abs(c.ferme["nourriture"]) <= self.ressourceN:
						self.removeFunds(c.ferme["metal"],c.ferme["energie"],c.ferme["nourriture"])
						return True
		#elif objetACree == "creerstationGalactique":
		elif objetACree == "creerstationSolaire":
			if abs(c.stationSolaire["metal"]) <= self.ressourceM:
				if abs(c.stationSolaire["energie"]) <= self.ressourceE:
					if abs(c.stationSolaire["nourriture"]) <= self.ressourceN:
						self.removeFunds(c.stationSolaire["metal"],c.stationSolaire["energie"],c.stationSolaire["nourriture"])
						return True
		#elif objetACree == "upgradevitessevaisseau":
		elif objetACree == "creerbarrack":
			if abs(c.barrack["metal"]) <= self.ressourceM:
				if abs(c.barrack["energie"]) <= self.ressourceE:
					if abs(c.barrack["nourriture"]) <= self.ressourceN:
						self.removeFunds(c.barrack["metal"],c.barrack["energie"],c.barrack["nourriture"])
						return True
		elif objetACree == "creerlazerboi":
			if abs(c.lazerboi["metal"]) <= self.ressourceM:
				if abs(c.lazerboi["energie"]) <= self.ressourceE:
					if abs(c.lazerboi["nourriture"]) <= self.ressourceN:
						self.removeFunds(c.lazerboi["metal"],c.lazerboi["energie"],c.lazerboi["nourriture"])
						return True
			
		return False
	
	def lazerboimort(self, idv):
		for v in self.attaquantTerre:
			if v.id == idv:
				self.attaquantTerre.remove(v)
				break
