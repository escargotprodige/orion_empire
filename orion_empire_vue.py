# -*- coding: utf-8 -*-
from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import os, os.path
import random
import math
from helper import Helper as hlp
from mathPlus import *
from Couts import *

from numpy.matlib import rand
from numpy.distutils.cpuinfo import command_by_line
from PIL.FontFile import WIDTH



class Vue():
	def __init__(self, parent, ip, nom, largeur=800, hauteur=600):
		self.root = Tk()
		self.root.title(os.path.basename(sys.argv[0]))
		self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
		self.parent = parent
		self.modele = None
		self.nom = None
		self.largeur = largeur
		self.hauteur = hauteur
		self.images = {}
		self.modes = {}
		self.modecourant = None
		self.cadreactif = None
		self.creercadres(ip, nom)
		self.changecadre(self.cadresplash)
		self.angleattente = 0

	def changemode(self, cadre):
		if self.modecourant:
			self.modecourant.pack_forget()
		self.modecourant = cadre
		self.modecourant.pack(expand=1, fill=BOTH)

	def changecadre(self, cadre, etend=0):
		if self.cadreactif:
			self.cadreactif.pack_forget()
		self.cadreactif = cadre
		if etend:
			self.cadreactif.pack(expand=1, fill=BOTH)
		else:
			self.cadreactif.pack()

	def creercadres(self, ip, nom):
		self.creercadresplash(ip, nom)
		self.creercadrelobby()
		self.creercadreloading()
		self.cadrejeu = Frame(self.root, bg="blue")
		self.modecourant = None

	def creercadresplash(self, ip, nom):
		self.cadresplash = Frame(self.root)
		#Canevas
		self.canevasplash = Canvas(self.cadresplash, bg="black", width=800, height=600)
		self.canevasplash.config(scrollregion=(0, 0, 1000, 800))
		self.canevasplash.pack()
		
		
		self.nomsplash = Entry(bg="pink")
		self.nomsplash.insert(0, nom)
		self.ipsplash = Entry(bg="pink")
		self.ipsplash.insert(0, ip)
		labip = Label(text=ip, bg="pink", borderwidth=0, relief=RIDGE)
		btncreerpartie = Button(text="Creer partie", bg="pink", command=self.creerpartie)
		btnconnecterpartie = Button(text="Connecter partie", bg="pink", command=self.connecterpartie)
		labUser = Label(bg="lightblue",text="Username", borderwidth=0, relief=RIDGE)
		labToi = Label(bg="lightblue",text="Ton IP", borderwidth=0, relief=RIDGE)
		labServ = Label(bg="lightblue",text="Serveur", borderwidth=0, relief=RIDGE)
		
		#Background
#		 im = Image.open("./images/orionBoiz600.png")
#		 logo = ImageTk.PhotoImage(im)
#		 labBG = Label(text=ip, bg="pink", borderwidth=0, relief=RIDGE, image=logo)
#		 self.canevasplash.create_window(0, 0, window=labBG, width=1200, height=670)
		
		labTitre = Label(font=("Courier bold", 44),text="Orion", borderwidth=0, bg="black",fg="white", relief=RIDGE)
		self.canevasplash.create_window(420, 200, window=labTitre, width=300, height=300)
		labTitre = Label(font=("Rage italic", 44),text="boiz", borderwidth=0, bg="black",fg="#f150a0", relief=RIDGE)
		self.canevasplash.create_window(460, 255, window=labTitre, width=100, height=65)
		
		#buttons
		self.canevasplash.create_window(320, 400, window=btncreerpartie, width=100, height=30)
		self.canevasplash.create_window(520, 400, window=btnconnecterpartie, width=100, height=30)
		#username
		self.canevasplash.create_window(150, 500, window=labUser, width=60, height=30)
		self.canevasplash.create_window(250, 500, window=self.nomsplash, width=120, height=30)
		#ip
		self.canevasplash.create_window(370, 500, window=labToi, width=50, height=30)
		self.canevasplash.create_window(440, 500, window=labip, width=100, height=30)
		#server
		self.canevasplash.create_window(550, 500, window=labServ, width=50, height=30)
		self.canevasplash.create_window(630, 500, window=self.ipsplash, width=100, height=30)
		
	def creercadrelobby(self):
		self.cadrelobby = Frame(self.root)
		#Canevas
		self.canevaslobby = Canvas(self.cadrelobby, width=800, height=600, bg="black")
		self.canevaslobby.pack()
		self.listelobby = Listbox(bg="lightblue", borderwidth=0, relief=FLAT)
		self.diametre = Entry(bg="pink")
		self.diametre.insert(0, 5)
		self.densitestellaire = Entry(bg="pink")
		self.densitestellaire.insert(0, 2)
		self.qteIA = Entry(bg="pink")
		self.qteIA.insert(0, 0)
		self.btnlancerpartie = Button(text="Lancer partie", bg="pink", command=self.lancerpartie, state=DISABLED)
		#usagers
		self.canevaslobby.create_text(550, 70, text="Usagers dans la partie :",fill="white")
		self.canevaslobby.create_window(600, 280, window=self.listelobby, width=200, height=400)
		#Parametres
		self.canevaslobby.create_text(200, 70, text="Parametres de la partie :",fill="white")
		
		self.canevaslobby.create_window(300, 140, window=self.diametre, width=100, height=30)
		self.canevaslobby.create_text(150, 140, text="Diametre en annees lumiere",fill="white")
		self.canevaslobby.create_window(300, 240, window=self.densitestellaire, width=100, height=30)
		self.canevaslobby.create_text(150, 240,fill="white", text="Nb systeme/AL cube")
		self.canevaslobby.create_window(300, 340, window=self.qteIA, width=100, height=30)
		self.canevaslobby.create_text(150, 340,text="Nb d'IA",fill="white", justify='right')

		self.canevaslobby.create_window(400, 500, window=self.btnlancerpartie, width=100, height=30)

	def creercadreloading(self):
		self.cadreloading = Frame(self.root)
		self.canevasloading = Canvas(self.cadreloading, width=640, height=480, bg="white")
		self.canevasloading.create_text(320, 240, font=("Arial", 36), text="Chargement en cours...")
		self.canevasloading.pack()

	def voirgalaxie(self):
		# A FAIRE comme pour voirsysteme et voirplanete, tester si on a deja la vuegalaxie
		#		 sinon si on la cree en centrant la vue sur le systeme d'ou on vient
		s = self.modes["galaxie"]
		self.changemode(s)

	def voirsysteme(self, systeme=None):
		if systeme:
			sid = systeme.id
			if sid in self.modes["systemes"].keys():
				s = self.modes["systemes"][sid]
			else:
				s = VueSysteme(self)
				self.modes["systemes"][sid] = s
				s.initsysteme(systeme)
			self.changemode(s)

	def voirplanete(self, maselection=None):
		s = self.modes["planetes"]

		if maselection:
			sysid = maselection[5]
			planeid = maselection[2]
			if planeid in self.modes["planetes"].keys():
				s = self.modes["planetes"][planeid]
			else:
				s = VuePlanete(self, sysid, planeid)
				self.modes["planetes"][planeid] = s
				s.initplanete(sysid, planeid)
			self.changemode(s)
		else:
			print("aucune planete selectionnee pour atterrissage")

	def voirplaneteP(self, idplanete, idsysteme):
		s = self.modes["planetes"]

		sysid = idsysteme
		planeid = idplanete
		if planeid in self.modes["planetes"].keys():
			s = self.modes["planetes"][planeid]
		else:
			s = VuePlanete(self, sysid, planeid)
			self.modes["planetes"][planeid] = s
			s.initplanete(sysid, planeid)
		self.changemode(s)

	def creerpartie(self):
		nom = self.nomsplash.get()
		ip = self.ipsplash.get()
		if nom and ip:
			self.parent.creerpartie()
			self.btnlancerpartie.config(state=NORMAL)
			self.connecterpartie()

	def connecterpartie(self):
		nom = self.nomsplash.get()
		ip = self.ipsplash.get()
		if nom and ip:
			self.parent.inscrirejoueur()
			self.changecadre(self.cadrelobby)
			self.parent.boucleattente()

	def attenteloading(self):
		self.angleattente += 5
		if self.angleattente >= 360:
			self.angleattente = 0

		angle = (self.angleattente / 360) * (2 * math.pi)

		x, y = hlp.getAngledPoint(angle, 10, 320, 350)

		self.canevasloading.delete("loading")

		self.canevasloading.create_oval(x - 10, y - 10, x + 10, y + 10, tags=("loading"), fill="red")
		self.root.update_idletasks()

	def lancerpartie(self):
		diametre = self.diametre.get()
		densitestellaire = self.densitestellaire.get()
		qteIA = self.qteIA.get()  # IA

		print("Loading...")
		if diametre:
			diametre = float(diametre)
		else:
			diametre = None
		if densitestellaire:
			densitestellaire = float(densitestellaire)
		else:
			densitestellaire = None
		self.parent.lancerpartie(diametre, densitestellaire, qteIA)  # IA

	def affichelisteparticipants(self, lj):
		self.listelobby.delete(0, END)
		for i in lj:
			self.listelobby.insert(END, i)

	def afficherinitpartie(self, mod):
		self.nom = self.parent.monnom
		self.modele = mod

		self.modes["galaxie"] = VueGalaxie(self)
		self.modes["systemes"] = {}
		self.modes["planetes"] = {}

		g = self.modes["galaxie"]
		g.labid.config(text=self.nom)
		g.labid.config(fg=mod.joueurs[self.nom].couleur)

		g.chargeimages(mod)
		g.afficherdecor()  # pourrait etre remplace par une image fait avec PIL -> moins d'objets
		self.changecadre(self.cadrejeu, 1)
		self.changemode(self.modes["galaxie"])

		self.voirsysteme(
			mod.joueurs[self.nom].systemeorigine)  # Commencer en Vue SystemeOrigine si PlaneteOrigine pas disponible
		for i in mod.joueurs[self.nom].systemeorigine.planetes:  # Trouver planete origine
			# print(mod.joueurs[self.nom].systemeorigine)
			# print(i.proprietaire)
			if i.proprietaire == self.nom:
				self.voirplaneteP(i.id, mod.joueurs[self.nom].systemeorigine.id)  # Afficher planeteOrigine
				mod.joueurs[self.nom].creerVilleOrigine()
				self.deplacerCanevas(250, 250)

	def afficherBatiment(self, Batiment):
		# 200 c'Est la taille du minimap
		for i in self.modes["planetes"].keys():
			if i == Batiment.planeteid:
				p = 200 / self.modes["planetes"][i].planete.terrainTailleCarre
				couleur = self.modele.joueurs[Batiment.proprietaire].couleur
				t = 200 / self.modes["planetes"][i].tailleterrainpixel
				x = Batiment.x * self.modes["planetes"][i].tailleTile
				y = Batiment.y * self.modes["planetes"][i].tailleTile
				im = self.modes["planetes"][i].images[Batiment.type]
				self.modes["planetes"][i].canevas.create_image(x, y, image=im,
															   tags=(Batiment.id, Batiment.type, "batiment"))

				self.modes["planetes"][i].minimap.create_oval(x * t - p, y * t - p, x * t + p, y * t + p, fill=couleur,
															  tags=(Batiment.id, Batiment.type))
				break

	def effacerBatiment(self, Batiment):
		for i in self.modes["planetes"].keys():
			if i == Batiment.planeteid:
				self.modes["planetes"][i].canevas.delete(Batiment.id)
				self.modes["planetes"][i].minimap(Batiment.id)
				break;
			
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
	
	def afficherLazerBoi(self, lazerBoi):
		subDivisionLevel = 20
		quantiteReflet = 20
		# 200 c'Est la taille du minimap
		for i in self.modes["planetes"].keys():
			if i == lazerBoi.planeteid:
				p = 200 / self.modes["planetes"][i].planete.terrainTailleCarre
				couleur = self.modele.joueurs[lazerBoi.proprietaire].couleur
				t = 200 / self.modes["planetes"][i].largeur
				x = lazerBoi.x
				y = lazerBoi.y

				im = self.modes["planetes"][i].images["lazerboi"]
				self.modes["planetes"][i].canevas.create_image(lazerBoi.x, lazerBoi.y, image=im,
															   tags=(lazerBoi.id, "lazerboi"))

				self.modes["planetes"][i].minimap.create_oval(x * t - p, y * t - p, x * t + p, y * t + p, fill=couleur, tags=(lazerBoi.id, "lazerboi"))
				
				#lazer
				if lazerBoi.target != None:
					if lazerBoi.isTargetInRange:
						lesRayons = []
						unRayon = []
						
						p = lazerBoi
						q = lazerBoi.target
						distTotal = distance(p.x, p.y, q.x, q.y) #D
						direction = list(directionVers(p.x, p.y, q.x, q.y)) #[x, y]
						
						r = random.randint(0,254)
						g = random.randint(0,254)
						b = random.randint(0,254)
						
						
						for k in range(subDivisionLevel):
							unRayon.clear()
							unRayon.append(direction[0] * (distTotal/subDivisionLevel) * k)
							unRayon.append(direction[1] * (distTotal/subDivisionLevel) * k)
							unRayon[0] += p.x + random.randint(-5, 5)
							unRayon[1] += p.y + random.randint(-5, 5)
							lesRayons.append(list(unRayon))
						
						for k in range(subDivisionLevel):
							r+= random.randint(0,5)
							g+= random.randint(0,5)
							b+= random.randint(0,5)
							
							if k == subDivisionLevel-1:
								self.modes["planetes"][i].canevas.create_line(lesRayons[k][0], lesRayons[k][1], q.x, q.y , fill=self.rgbToHex(r, g, b), width=10,
												tags=(p.proprietaire, "rayonLazer", str(p.id), "effetsSpeciaux"))
							else:
								self.modes["planetes"][i].canevas.create_line(lesRayons[k][0], lesRayons[k][1], lesRayons[k+1][0], lesRayons[k+1][1], fill=self.rgbToHex(r, g, b), width=10,
												tags=(p.proprietaire, "rayonLazer", str(p.id), "effetsSpeciaux"))

							if k == subDivisionLevel-1:
								self.modes["planetes"][i].canevas.create_line(lesRayons[k][0], lesRayons[k][1], q.x, q.y , fill=self.rgbToHex(255, 255, 255), width=3, tags=(p.proprietaire, "rayonLazer", str(p.id), "effetsSpeciaux"))
							else:
								self.modes["planetes"][i].canevas.create_line(lesRayons[k][0], lesRayons[k][1], lesRayons[k+1][0], lesRayons[k+1][1], fill=self.rgbToHex(255,255, 255), width=3, tags=(p.proprietaire, "rayonLazer", str(p.id), "effetsSpeciaux"))
						
						for k in range(quantiteReflet):
							reflet = []
							reflet.append(direction[0] * (distTotal/subDivisionLevel) * subDivisionLevel-1)
							reflet.append(direction[1] * (distTotal/subDivisionLevel) * subDivisionLevel-1)
							
							reflet[0] += p.x + random.randint(0,20)
							reflet[1] += p.y + random.randint(0,20)
	
							self.modes["planetes"][i].canevas.create_line(lesRayons[subDivisionLevel-1][0], lesRayons[subDivisionLevel-1][1], reflet[0], reflet[1], fill=self.rgbToHex(255, 255, 255), width=3,
											tags=(p.proprietaire, "rayonLazer", str(p.id), "effetsSpeciaux"))   



	def effacerLazerBoi(self):
		for i in self.modes["planetes"].keys():
				self.modes["planetes"][i].canevas.delete("lazerboi")
				self.modes["planetes"][i].canevas.delete("rayonLazer")
				break;

	def fermerfenetre(self):
		# Ici, on pourrait mettre des actions a faire avant de fermer (sauvegarder, avertir etc)
		self.parent.fermefenetre()

	def deplacerCanevas(self, x, y):  # ------------------- centre la vue sur une position x y
		mode = self.modecourant

		ee = mode.canevas.winfo_width()
		ii = mode.canevas.winfo_height()
		eex = int(ee) / mode.largeur / 2
		eey = int(ii) / mode.hauteur / 2

		ratio = 1
		if mode == self.modes["galaxie"]:
			ratio = mode.AL2pixel
			print("G", ratio)
		elif mode in self.modes["planetes"]:
			ratio = mode.KM2pixel
			print("P")
		elif mode in self.modes["systemes"]:
			ratio = mode.UA2pixel
			print("S")

		mode.canevas.xview(MOVETO, (x * ratio / mode.largeur) - eex)
		mode.canevas.yview(MOVETO, (y * ratio / mode.hauteur) - eey)


	def vaisseaumort(self,v):
		print("efface",v.systeme_courant.id)
		if v.systeme_courant.id in self.modes["systemes"]:
			mode = self.modes["systemes"][v.systeme_courant.id]
			print(mode.maselection)
			if mode.maselection and v.id in mode.maselection:
				mode.maselection = None
				mode.canevas.delete("selecteur")

class Perspective(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent.cadrejeu)
		self.parent = parent
		self.modele = None
		self.cadreetatactif = None
		# !!!
		self.masque = (15, 63, 220)  # couleur de masque pour les images
		self.images = {}
		self.cadrevue = Frame(self, width=400, height=400, bg="lightgreen")
		self.cadrevue.pack(side=LEFT, expand=1, fill=BOTH)

		self.cadreinfo = Frame(self, width=200, height=200, bg="darkgrey")
		self.cadreinfo.pack(side=LEFT, fill=Y)
		self.cadreinfo.pack_propagate(0)
		self.cadreetat = Frame(self.cadreinfo, width=200, height=200, bg="grey20")
		self.cadreetat.pack()

		self.cadreetat.grid(row=0, column=0)
		self.cadreetat.pack(expand=TRUE)

		self.scrollX = Scrollbar(self.cadrevue, orient=HORIZONTAL)
		self.scrollY = Scrollbar(self.cadrevue)
		self.canevas = Canvas(self.cadrevue, width=800, height=600, bg="grey11",
							  xscrollcommand=self.scrollX.set,
							  yscrollcommand=self.scrollY.set)

		self.canevas.bind("<Button>", self.cliquervue)

		self.scrollX.config(command=self.canevas.xview)
		self.scrollY.config(command=self.canevas.yview)
		self.canevas.grid(column=0, row=0, sticky=N + E + W + S)
		self.cadrevue.columnconfigure(0, weight=1)
		self.cadrevue.rowconfigure(0, weight=1)
		self.scrollX.grid(column=0, row=1, sticky=E + W)
		self.scrollY.grid(column=1, row=0, sticky=N + S)

		# label id joueur nom
		self.labid = Label(self.cadreetat, text=self.parent.nom)
		self.labid.grid(row=20, column=0)

		# self.labid=Label(self.cadreinfo,width= 200,text=self.parent.nom) #!
		# self.labid.pack()

		self.cadreetataction = Frame(self.cadreetat, width=200, height=200, bg="grey20")

		self.cadreetatmsg = Frame(self.cadreetat, width=200, height=200, bg="grey20")

		self.cadreminimap = Frame(self.cadreinfo, width=200, height=200, bg="grey20")
		self.cadreminimap.pack(side=BOTTOM)
		self.minimap = Canvas(self.cadreminimap, width=200, height=200, bg="grey11")
		self.minimap.bind("<Button>", self.cliquerminimap)
		self.minimap.pack()

		self.afficherUI()

		#Message
		self.cadreMessage = Frame(self.cadreinfo, width=200, height=40, bg="white")
		self.cadreMessage.pack()
		self.message = StringVar();
		self.lblMessage = Label(self.cadreMessage, width=90, height=2,wraplength=180, bg="#f150a0", fg="white",
							 textvariable=self.message)
		self.lblMessage.pack(side=LEFT)
		self.updateMessage("Bienvenue!")
		
		# Afficher Ressources 
		self.cadreRessources = Frame(self.cadreinfo, width=200, height=50, bg="white")
		self.cadreRessources.pack()
		self.r1 = StringVar();
		self.r2 = StringVar();
		self.r3 = StringVar();

		rWidth = 9
		rHeight = 2
		self.ressources = Label(self.cadreRessources, width=rWidth, height=rHeight, bg="brown",
								textvariable=self.r1)  # !
		self.ressources.pack(side=LEFT)
		self.ressources = Label(self.cadreRessources, width=rWidth, height=rHeight, bg="yellow",
								textvariable=self.r2)  # !
		self.ressources.pack(side=LEFT)
		self.ressources = Label(self.cadreRessources, width=rWidth, height=rHeight, bg="green",
								textvariable=self.r3)  # !
		self.ressources.pack(side=LEFT)
		
	def updateMessage(self, message):
		self.message.set(message)
		
	def cliquervue(self, evt):
		pass

	def cliquerminimap(self, evt):
		pass

	def changecadreetat(self, cadre):

		if self.cadreetatactif:
			self.cadreetatactif.pack_forget()
			self.cadreetatactif = None
		if cadre:
			self.cadreetatactif = cadre
			self.cadreetatactif.grid()

	def afficherUI(self):
		for child in self.cadreetataction.winfo_children():
			child.destroy()
		for child in self.cadreetatmsg.winfo_children():
			child.destroy()

	def updateRessources(self, joueur):

		self.r1.set(str(joueur.ressourceM))
		self.r2.set(str(joueur.ressourceE))
		self.r3.set(str(joueur.ressourceN))


class VueGalaxie(Perspective):
	def __init__(self, parent):
		Perspective.__init__(self, parent)
		self.modele = self.parent.modele
		self.maselection = None
		self.AL2pixel = 100

		self.largeur = int(self.modele.diametre * self.AL2pixel)
		self.hauteur = self.largeur

		self.canevas.config(scrollregion=(0, 0, self.largeur, self.hauteur))

		self.afficherUI()

	def afficherUI(self):
		Perspective.afficherUI(self)

		self.cadreShop = None
		self.cadreJoueur = None
		self.cadreSelection = None
		self.cadreInfoShop = None

		boutonNext = Button(self.cadreetat, text="→", command=self.voirsysteme)
		boutonNext.grid(row=0, column=5, sticky=N + E)

		self.boutonShop = Button(self.cadreetat, text="Shop ˃", command=self.afficherShop)
		self.boutonShop.grid(row=2, column=0)

		self.cadreSelectionVaisseau = Frame(self.cadreetat, bg="grey20")  # MODIF début
		
		self.cadreSelection = Frame(self.cadreetat, width=200, height=400, bg="blue")
		self.cadreSelection.grid(row=10,column=0)
		btnCharger = Button(self.cadreSelection, text="Charger Vaisseau", wraplength=80) #, command= ICI FONCTION SARAH)
		btnDecharger = Button(self.cadreSelection, text="Decharger Vaisseau", wraplength=80) #, command= ICI FONCTION SARAH)
		btnCharger.grid(row=0,column=0)
		btnDecharger.grid(row=0,column=1)
		
#		 self.lbselectecible = Label(self.cadreSelectionVaisseau, text="Choisir cible", bg="darkgrey")
#		 self.lbselectecible.grid(row=0, column=0)
# 
#		 self.btndechargervaisseau = Button(self.cadreSelectionVaisseau, text="Décharger vaisseau",
#											command=self.dechargerVaisseauGalactique)
#		 self.btndechargervaisseau.grid(row=1, column=0)
# 
#		 self.btncreervaisseau = Button(self.cadreSelectionVaisseau, text="Upgrade vitesse vaisseau",
#										command=self.upgradeVitesseVaisseau)
#		 self.btncreervaisseau.grid(row=2, column=0)

#	 def afficherShop(self):
#		 self.boutonShop.config(text="Shop ˅")
#		 # self.cadreShop=Frame(self.cadreetat,width=200,height=200,bg="blue")
# 
#		 if self.cadreShop:
#			 self.cadreShop.grid_forget()
#			 self.boutonShop.config(text="Shop ˃")
#			 self.cadreShop = None
#		 else:
#			 self.cadreShop = Frame(self.cadreetat, width=200, height=200, bg="blue")
#			 self.cadreShop.grid(row=3, column=0, columnspan=5, rowspan=5)
#			 shopVaisseau = Button(self.cadreShop, text="Vaisseau", command=self.creervaisseauGalactique)
#			 shopVaisseau.grid(row=0, column=0)
#			 shopStation = Button(self.cadreShop, text="Station", command=self.creerstationGalactique)
#			 shopStation.grid(row=0, column=1)  # MODIF fin

	def afficherShop(self):
		self.boutonShop.config(text="Shop ˅")
		# enlever les autres cadres
		if self.cadreSelection:
			self.cadreSelection.grid_forget()
			self.boutonSelect.config(text="Selection >")
			self.cadreSelection = None
		else:
			pass

		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		else:
			self.cadreShop = Frame(self.cadreetat, width=200, height=400, bg="blue")
			self.cadreShop.grid(row=3, column=0, columnspan=5, rowspan=5)

			shopVTransport = Button(self.cadreShop, text="Vaisseau", wraplength=80, image=self.images["shopChasseur"], compound="top", command=self.shopVaisseau)
			shopVTransport.grid(row=0, column=1)
			
			shopVCombat = Button(self.cadreShop, text="Station",wraplength=90, image=self.images["shopStation"], compound="top", command=self.shopStation)
			shopVCombat.grid(row=0, column=0)
			
			
	def infoShop(self, typeBatiment):
		# couts
		c = Cout()

		# creer cadre
		if self.cadreInfoShop:
			self.cadreInfoShop.grid_forget()
			self.cadreInfoShop = None
		else:
			pass
		self.cadreInfoShop = Frame(self.cadreShop, width=200, height=100)
		self.cadreInfoShop.grid(row=3, column=0, columnspan=5, rowspan=5)
		# Infos batiment
		labelImage = Label(self.cadreInfoShop, image=self.images["shopChasseur"])
		labelNom = Label(self.cadreInfoShop, text="Vaisseau Galactique",wraplength=90,)
		labelLvl = Label(self.cadreInfoShop, text="Lvl. 1")
		# Cout batiment
		label = Label(self.cadreInfoShop, text="Cout")
		label.grid(row=0, column=2, columnspan=2)
		label = Label(self.cadreInfoShop, text="Metal")
		label.grid(row=1, column=2)
		label = Label(self.cadreInfoShop, text="Energie")
		label.grid(row=2, column=2)
		label = Label(self.cadreInfoShop, text="Food")
		label.grid(row=3, column=2)

		labelCoutMetal = Label(self.cadreInfoShop, text="")
		labelCoutEnergie = Label(self.cadreInfoShop, text="")
		labelCoutFood = Label(self.cadreInfoShop, text="")
		# Boutons
		boutonAcheter = Button(self.cadreInfoShop, text="Acheter")
		if typeBatiment is "vaisseau":
			labelCoutMetal.config(text=c.vaisseauG["metal"])
			labelCoutEnergie.config(text=c.vaisseauG["energie"])
			labelCoutFood.config(text=c.vaisseauG["nourriture"])
			boutonAcheter.config(command=self.creervaisseauGalactique)
		elif typeBatiment is "station":
			labelImage.config(image=self.images["shopStation"])
			labelNom.config(text="Station Galactique",wraplength=90)
			labelCoutMetal.config(text=c.stationG["metal"])
			labelCoutEnergie.config(text=c.stationG["energie"])
			labelCoutFood.config(text=c.stationG["nourriture"])
			boutonAcheter.config(command=self.creerstationGalactique)
		# grid tout
		# batiment
		labelImage.grid(row=0, column=0, columnspan=2, rowspan=2)
		labelNom.grid(row=2, column=0, columnspan=2)
		labelLvl.grid(row=3, column=0, columnspan=2)
		# ressources -
		labelCoutMetal.grid(row=1, column=3)
		labelCoutEnergie.grid(row=2, column=3)
		labelCoutFood.grid(row=3, column=3)
		# bouton
		boutonAcheter.grid(row=4, column=4)

	def shopVaisseau(self):
		self.infoShop("vaisseau")
	def shopStation(self):
		self.infoShop("station")
	def voirsysteme(self, systeme=None):
		if systeme == None:
			if self.maselection and self.maselection[0] == self.parent.nom and self.maselection[1] == "systeme":
				sid = self.maselection[2]
				for i in self.modele.joueurs[self.parent.nom].systemesvisites:
					if i.id == sid:
						s = i
						break

				self.parent.parent.visitersysteme(sid)
				self.parent.voirsysteme(s)  # normalement devrait pas planter
		else:
			sid = systeme.id
			for i in self.modele.joueurs[self.parent.nom].systemesvisites:
				if i.id == sid:
					s = i
					break
			# NOTE passer par le serveur est-il requis ????????????
			self.parent.parent.visitersysteme(sid)
			self.parent.voirsysteme(s)  # normalement devrait pas planter

	def chargeimages(self, mod):
		# self.images["chasseur"] = Image.open("./images/chasseur.png")
		self.images["chasseur"] = {}
		for j in mod.joueurscles:
			image = Image.open("./images/chasseur.png")

			pixel = image.load()
			couleur = image.convert("RGB")
			for i in range(image.size[0]):
				for k in range(image.size[1]):
					r, g, b = couleur.getpixel((i, k))
					if r == self.masque[0] and g == self.masque[1] and b == self.masque[2]:
						bouton = Button()
						r, g, b = bouton.winfo_rgb(mod.joueurs[j].couleur)
						r = int(r / 256)
						g = int(g / 256)
						b = int(b / 256)
						pixel[i, k] = (r, g, b)

			self.images["chasseur"][j] = image
		self.img = {}
		im = Image.open("./images/chasseurShop.png")
		self.images["shopChasseur"] = ImageTk.PhotoImage(im)
		#Modifier pour image Station
		im = Image.open("./images/station.png")
		self.images["shopStation"] = ImageTk.PhotoImage(im)
		

	def afficherdecor(self):
		self.creerimagefond()
		self.affichermodelestatique()

	def creerimagefond(
			self):  # NOTE - au lieu de la creer a chaque fois on aurait pu utiliser une meme image de fond cree avec PIL
		imgfondpil = Image.new("RGBA", (self.largeur, self.hauteur), "black")
		draw = ImageDraw.Draw(imgfondpil)
		for i in range(self.largeur * 2):
			x = random.randrange(self.largeur)
			y = random.randrange(self.hauteur)
			# draw.ellipse((x,y,x+1,y+1), fill="white")
			draw.ellipse((x, y, x + 0.1, y + 0.11), fill="white")
		self.images["fond"] = ImageTk.PhotoImage(imgfondpil)
		self.canevas.create_image(self.largeur / 2, self.hauteur / 2, image=self.images["fond"])

	def affichermodelestatique(self):
		mini = self.largeur / 200
		e = self.AL2pixel
		me = 200 / self.modele.diametre
		m = 3

		for i in self.modele.systemes:
			t = i.etoile.taille * 3
			if t < 3:
				t = 3

			self.canevas.create_oval((i.x * e) - t, (i.y * e) - t, (i.x * e) + t, (i.y * e) + t, fill=i.etoile.outline,
									 tags=("inconnu", "systeme", i.id, str(i.x), str(i.y)))

		# NOTE pour voir les id des objets systeme, decommentez la ligne suivantes
		# self.canevas.create_text((i.x*e)-t,(i.y*e)-(t*2),text=str(i.id),fill="white")

		# for i in self.modele.joueurscles:
		#	couleur=self.modele.joueurs[i].couleur

		#	for j in self.modele.joueurs[i].systemesvisites:
		#		s=self.canevas.find_withtag(j.id)
		#		self.canevas.addtag_withtag(i, s)
		#		self.canevas.itemconfig(s,fill="grey80")
		#
		#		self.minimap.create_oval((j.x*me)-m,(j.y*me)-m,(j.x*me)+m,(j.y*me)+m,fill="grey80",tags=("systeme",j.id))

		i = self.modele.joueurs[self.parent.parent.monnom]

		for j in i.systemesvisites:
			s = self.canevas.find_withtag(j.id)
			self.canevas.addtag_withtag(self.parent.parent.monnom, s)
			self.canevas.itemconfig(s, fill=j.etoile.type)

			self.minimap.create_oval((j.x * me) - m, (j.y * me) - m, (j.x * me) + m, (j.y * me) + m, fill=j.etoile.type,
									 tags=("systeme", j.id))

	# ************************ FIN DE LA SECTION D'AMORCE DE LA PARTIE

	def identifierplanetemere(self, evt):
		j = self.modele.joueurs[self.parent.nom]
		couleur = j.couleur
		x = j.systemeorigine.x * self.AL2pixel
		y = j.systemeorigine.y * self.AL2pixel
		id = j.systemeorigine.id
		t = 10
		self.canevas.create_oval(x - t, y - t, x + t, y + t, dash=(3, 3), width=2, outline=couleur,
								 tags=(self.parent.nom, "selecteur", id, ""))
		xx = x / self.largeur
		yy = y / self.hauteur
		ee = self.canevas.winfo_width()
		ii = self.canevas.winfo_height()
		eex = int(ee) / self.largeur / 2
		self.canevas.xview(MOVETO, xx - eex)
		eey = int(ii) / self.hauteur / 2
		self.canevas.yview(MOVETO, yy - eey)

	def creervaisseauGalactique(self):
		if self.maselection:
			self.parent.parent.creervaisseauGalactique(self.maselection[2])
			self.maselection = None
			self.canevas.delete("selecteur")

	def creerstation(self):
		print("Creer station EN CONSTRUCTION")

	def creerstationGalactique(self):
		if self.maselection:
			self.parent.parent.creerstationGalactique(self.maselection[2])
			self.maselection = None
			self.canevas.delete("selecteur")

	def afficherpartie(self, mod):
		self.canevas.delete("artefact")
		self.canevas.delete("pulsar")
		self.canevas.delete("stationGalactique")
		self.afficherselection()
		self.minimap.delete("vaisseauinterstellaire")
		self.minimap.delete("stationGalactique")

		mini=2
		UAmini=4

		e = self.AL2pixel
		me = 200 / self.modele.diametre
		m = 2

		for i in mod.pulsars:  # ------------------------- cree les pulsars en premier pour les afficher  sous les vaisseaux
			t = i.taille
			self.canevas.create_oval((i.x * e) - t, (i.y * e) - t, (i.x * e) + t, (i.y * e) + t, fill="orchid3",

									 dash=(1, 1),
									 outline="maroon1", width=2,
									 tags=("inconnu", "pulsar", i.id))

		for j in mod.joueurscles:################################################Modif Tristan
			a = mod.joueurs[j]
			for s in a.stationGalactiques:
				xl=s.systemeOrigine.x*e
				yl=s.systemeOrigine.y*e
				x,y=hlp.getAngledPoint(math.radians(s.angle),15,xl,yl)
				n=4
				self.canevas.create_oval(x-n,y-n,x+n,y+n,fill=a.couleur,outline="white",tags=(s.proprietaire,"StationGalactique",s.id,"artefact"))
				x,y=hlp.getAngledPoint(math.radians(s.angle),UAmini,100,100)
				self.minimap.create_oval(x-mini,y-mini,x+mini,y+mini,fill="red",tags=("stationGalactique"))


		for k in mod.joueurscles:
			i = mod.joueurs[k]
			self.img[k] = []
			index = 0
			for j in i.vaisseauxinterstellaires:
				jx = j.x * e
				jy = j.y * e

				# self.canevas.create_line(x,y,x0,y0,fill="yellow",width=3,
				#						 tags=(j.proprietaire,"vaisseauinterstellaire",j.id,"artefact"))
				# self.canevas.create_line(x0,y0,x1,y1,fill=i.couleur,width=4,
				#						 tags=(j.proprietaire,"vaisseauinterstellaire",j.id,"artefact"))
				# self.canevas.create_line(x1,y1,x2,y2,fill="red",width=2,
				#						 tags=(j.proprietaire,"vaisseauinterstellaire",j.id,"artefact"))
				#
				# self.img[k] = ImageTk.PhotoImage(self.images["chasseur"].rotate(j.degre -90))


				self.img[k].append(ImageTk.PhotoImage(self.images["chasseur"][k].rotate(j.degre - 90)))

				self.canevas.create_image(jx, jy, image=self.img[k][index],
										  tags=(j.proprietaire, "vaisseauinterstellaire", j.id, "artefact"))
				index += 1

				# Afficher vaisseaux sur minimap
				if i.nom == self.parent.nom:
					self.minimap.create_rectangle((j.x * me) - m, (j.y * me) - m, (j.x * me) + m, (j.y * me) + m,
												  fill=i.couleur,
												  tags=("vaisseauinterstellaire", j.id))



				# ------------------------ Afficher vaisseaux sur minimap
				if i.nom == self.parent.nom:
					self.minimap.create_rectangle((j.x * me) - m, (j.y * me) - m, (j.x * me) + m, (j.y * me) + m,
												  fill=i.couleur,
												  tags=("vaisseauinterstellaire", j.id))


	def changeetatsystem(self, nom, systeme):
		id = str(systeme.id)
		lp = self.canevas.find_withtag(id)
		self.canevas.addtag_withtag(nom, id)

		m = 3
		me = 200 / self.modele.diametre

		self.canevas.itemconfig(lp[0], fill=systeme.etoile.type)

		self.minimap.create_oval((systeme.x * me) - m, (systeme.y * me) - m, (systeme.x * me) + m, (systeme.y * me) + m,
								 fill=systeme.etoile.type, tags=("systeme", systeme.id))

	def changerproprietaire(self, prop, couleur, systeme):
		# lp=self.canevas.find_withtag(systeme.id)
		self.canevas.addtag_withtag(prop, systeme.id)

	def changerproprietaire1(self, prop, couleur, systeme):
		id = str(systeme.id)
		lp = self.canevas.find_withtag(id)
		self.canevas.itemconfig(lp[0], fill=couleur)
		t = (prop, "systeme", id, "systemevisite", str(len(systeme.planetes)), systeme.etoile.type)
		self.canevas.itemconfig(lp[0], tags=t)

	def afficherselection(self):
		self.canevas.delete("selecteur")
		if self.maselection != None:
			joueur = self.modele.joueurs[self.parent.nom]

			e = self.AL2pixel
			if self.maselection[1] == "systeme":
				for i in joueur.systemesvisites:
					if i.id == self.maselection[2]:
						x = i.x
						y = i.y
						t = 10
						self.canevas.create_oval((x * e) - t, (y * e) - t, (x * e) + t, (y * e) + t, dash=(2, 2),
												 outline=joueur.couleur,
												 tags=("select", "selecteur"))
			elif self.maselection[1] == "vaisseauinterstellaire":
				for i in joueur.vaisseauxinterstellaires:
					if i.id == self.maselection[2]:
						x = i.x
						#print(x)
						y = i.y
						#print(y)
						t = 10
						self.canevas.create_rectangle((x * e) - t, (y * e) - t, (x * e) + t, (y * e) + t, dash=(2, 2),
													  outline=joueur.couleur,
													  tags=("select", "selecteur"))

			elif self.maselection[1] == "StationGalactique":
				for i in joueur.stationGalactiques:
					if i.id == self.maselection[2]:
						xl=i.systemeOrigine.x*e
						yl=i.systemeOrigine.y*e
						x,y=hlp.getAngledPoint(math.radians(i.angle),15,xl,yl)
						n=8
						self.canevas.create_oval(x-n,y-n,x+n,y+n, dash=(2, 2),outline=joueur.couleur,
												 tags=("select", "selecteur"))


	def cliquervue(self, evt):
		# self.changecadreetat(None)
		t = self.canevas.gettags("current")
		if t and t[0] != "current":

			if t[1] == "vaisseauinterstellaire":
				print("IN VAISSEAUINTERSTELLAIRE", t)
				self.maselection = [self.parent.nom, t[1], t[2]]
				self.montrevaisseauxselection()

			elif t[1] == "systeme":
				print("IN SYSTEME", t)
				if self.maselection and self.maselection[1] == "vaisseauinterstellaire":
					print("IN systeme + select VAISSEAUINTERSTELLAIRE")
					self.parent.parent.ciblerdestination(self.maselection[2], t[2])
				elif self.parent.nom in t:
					print("IN systeme  PAS SELECTION")
					self.maselection = [self.parent.nom, t[1], t[2]]
					self.montresystemeselection()
				else:
					print("IN systeme + RIEN")
					self.maselection = None
					self.lbselectecible.pack_forget()
					self.canevas.delete("selecteur")
				# self.changecadreetat(None)

			elif t[1] == "StationGalactique":
				self.maselection = [self.parent.nom, t[1], t[2]]

			elif t[1] == "pulsar":
				print("IN PULSAR", t)
				if self.maselection and self.maselection[1] == "vaisseauinterstellaire":
					print("IN pulsar + select select VAISSEAUINTERSTELLAIRE")
					self.parent.parent.ciblerdestination(self.maselection[2], t[2])

			else:
				print("Objet inconnu")
		else:
			print("Region inconnue")
			self.maselection = None
			self.lbselectecible.pack_forget()
			self.canevas.delete("selecteur")
		# self.changecadreetat(None)

	def changecadreetat(self, cadre):
		if self.cadreSelection:
			self.cadreSelection.grid_forget()
		# print("FORGET")
		if cadre:
			self.cadreSelection = cadre
			self.cadreSelection.grid(row=10, column=0)

	def montresystemeselection(self):
		self.changecadreetat(None)

	def montrevaisseauxselection(self):
		self.changecadreetat(self.cadreSelectionVaisseau)

	def afficherartefacts(self, joueurs):
		pass  # print("ARTEFACTS de ",self.nom)

	def cliquerminimap(self, evt):
		x = evt.x
		y = evt.y
		xn = self.largeur / int(self.minimap.winfo_width())
		yn = self.hauteur / int(self.minimap.winfo_height())

		ee = self.canevas.winfo_width()
		ii = self.canevas.winfo_height()
		eex = int(ee) / self.largeur / 2
		eey = int(ii) / self.hauteur / 2

		self.canevas.xview(MOVETO, (x * xn / self.largeur) - eex)
		self.canevas.yview(MOVETO, (y * yn / self.hauteur) - eey)

	def dechargerVaisseauGalactique(self):
		print("DEMANDE DECHARGEMENT")
		e = self.AL2pixel
		if self.maselection:
			v = self.maselection[2]
			print(v)
			for j in self.parent.modele.joueurs[self.parent.nom].vaisseauxinterstellaires:
				if j.id == v:
					v = j
					break
			print(v)
			item = self.canevas.find_overlapping(v.x * e - 20, v.y * e - 20, v.x * e + 20, v.y * e + 20)
			t = None
			s = None
			for i in item:
				# print(i)
				t = self.canevas.gettags(i)
				# print(t)
				for j in range(len(t)):
					if t[j] == "systeme":
						print("IN SYSTEM", t[j], t[j + 1])
						s = t[j + 1]
						break

			if s:
				print("DECHARGEMENT")
				self.parent.parent.dechargerVaisseauGalactique(self.maselection[2], s)
			else:
				print(self.maselection, " PAS A UN SYSTEME")
			# self.maselection = None
			# self.canevas.delete("selecteur")
		pass

	def upgradeVitesseVaisseau(self):
		print("CLIQUER UPGRADE VITESSE VAISSEAU GALACTIQUE")

		if self.maselection:
			# print(self.maselection)
			self.parent.parent.upgradeVitesseVaisseau(self.maselection[2], 0.003)

		pass


class VueSysteme(Perspective):
	def __init__(self, parent):
		Perspective.__init__(self, parent)
		self.modele = self.parent.modele
		self.planetes = {}
		self.systeme = None
		self.maselection = None

		self.UA2pixel = 20  # Grandeur soleil # ainsi la terre serait a 100 pixels du soleil et Uranus a 19 Unites Astronomiques
		self.largeur = 1000
		self.hauteur = self.largeur
		self.img = {}

		self.chargeimages(parent.parent.modele)

		self.afficherUI()

	def afficherUI(self):
		Perspective.afficherUI(self)

		self.cadreShop = None
		self.cadreJoueur = None
		self.cadreSelection = None
		self.cadreShopVaisseau = None
		self.cadreInfoShop = None
		

		boutonBack = Button(self.cadreetat, text="←", command=self.voirgalaxie)
		boutonBack.grid(row=0, column=0, sticky=N + W)
		boutonNext = Button(self.cadreetat, text="→", command=self.voirplanete)
		boutonNext.grid(row=0, column=5, sticky=N + E)

		self.boutonShop = Button(self.cadreetat, text="Shop ˃", command=self.afficherShop)
		self.boutonShop.grid(row=1, column=0, sticky=W)
		
		self.cadreSelection = Frame(self.cadreetat, width=200, height=400, bg="blue")
		self.cadreSelection.grid(row=10,column=0)
		btnCharger = Button(self.cadreSelection, text="Charger Vaisseau", wraplength=80) #, command= ICI FONCTION SARAH)
		btnDecharger = Button(self.cadreSelection, text="Decharger Vaisseau", wraplength=80) #, command= ICI FONCTION SARAH)
		btnCharger.grid(row=0,column=0)
		btnDecharger.grid(row=0,column=1)
# 
#	 def afficherShop(self):
#		 self.boutonShop.config(text="Shop ˅")
#		 # self.cadreShop=Frame(self.cadreetat,width=200,height=200,bg="blue")
#		 if self.cadreShop:
#			 self.cadreShop.grid_forget()
#			 self.boutonShop.config(text="Shop ˃")
#			 self.cadreShop = None
#		 else:
#			 self.cadreShop = Frame(self.cadreetat, width=200, height=200, bg="gray")
#			 self.cadreShop.grid(row=3, column=0, columnspan=5, rowspan=5)
#			 shopVaisseau = Button(self.cadreShop, text="Vaisseau Transport", command=self.creervaisseauTransport)
#			 shopVaisseau.grid(row=0, column=0, sticky=W)
#			 shopVaisseau = Button(self.cadreShop, text="Vaisseau Combat", command=self.creervaisseauCombat)
#			 shopVaisseau.grid(row=1, column=0, sticky=W)
#			 #shopStation = Button(self.cadreShop, text="Station", command=self.creerstation)
#			 #shopStation.grid(row=2, column=0, sticky = W)
#			 
#			 btnchangeretatvaisseau = Button(self.cadreShop, text="Changer mode agressif", command=self.changeretatvaisseau)

	def afficherShop(self):
		self.boutonShop.config(text="Shop ˅")
		# enlever les autres cadres
		if self.cadreSelection:
			self.cadreSelection.grid_forget()
			self.boutonSelect.config(text="Selection >")
			self.cadreSelection = None
		else:
			pass

		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		else:
			self.cadreShop = Frame(self.cadreetat, width=200, height=400, bg="blue")
			self.cadreShop.grid(row=3, column=0)
			shopVTransport = Button(self.cadreShop, text="Vaisseau Transport", wraplength=80, image=self.images["shopTransport"], compound="top", command=self.shopTransport)
			shopVTransport.grid(row=0, column=0)
			
			shopVCombat = Button(self.cadreShop, text="Vaisseau Combat",wraplength=90, image=self.images["shopCombat"], compound="top", command=self.shopCombat)
			shopVCombat.grid(row=0, column=1)

			shopStation = Button(self.cadreShop, text="Station",wraplength=90, image=self.images["shopCombat"], compound="top", command=self.shopStation)
			shopStation.grid(row=0, column=3)
			
			shopStation = Button(self.cadreShop, text="Station Solaire",wraplength=90, image=self.images["shopCombat"], compound="top", command=self.shopStation)
			shopStation.grid(row=0,column=2)
			
			shopStation = Button(self.cadreShop, text="Station Solaire",wraplength=90, image=self.images["shopStation"], compound="top", command=self.shopStation)
			shopStation.grid(row=0,column=2)
			
	def infoShop(self, typeBatiment):
		# couts
		c = Cout()

		# creer cadre
		if self.cadreInfoShop:
			self.cadreInfoShop.grid_forget()
			self.cadreInfoShop = None
		else:
			pass
		self.cadreInfoShop = Frame(self.cadreShop, width=200, height=100)
		self.cadreInfoShop.grid(row=1, column=0, columnspan=5, rowspan=5)
		# Infos batiment
		labelImage = Label(self.cadreInfoShop, image=self.images["shopTransport"])
		labelNom = Label(self.cadreInfoShop, text="Vaisseau Transport",wraplength=90)
		labelLvl = Label(self.cadreInfoShop, text="Lvl. 1")
		# Cout batiment
		label = Label(self.cadreInfoShop, text="Cout")
		label.grid(row=0, column=2, columnspan=2)
		label = Label(self.cadreInfoShop, text="Metal")
		label.grid(row=1, column=2)
		label = Label(self.cadreInfoShop, text="Energie")
		label.grid(row=2, column=2)
		label = Label(self.cadreInfoShop, text="Food")
		label.grid(row=3, column=2)

		labelCoutMetal = Label(self.cadreInfoShop, text="")
		labelCoutEnergie = Label(self.cadreInfoShop, text="")
		labelCoutFood = Label(self.cadreInfoShop, text="")
		# Boutons
		boutonAcheter = Button(self.cadreInfoShop, text="Acheter")
		if typeBatiment is "transport":
			labelCoutMetal.config(text=c.vSTransport["metal"])
			labelCoutEnergie.config(text=c.vSTransport["energie"])
			labelCoutFood.config(text=c.vSTransport["nourriture"])
			boutonAcheter.config(command=self.creervaisseauTransport)
		elif typeBatiment is "combat":
			labelImage.config(image=self.images["shopCombat"])
			labelNom.config(text="Vaisseau Combat",wraplength=90)
			labelCoutMetal.config(text=c.vSCombat["metal"])
			labelCoutEnergie.config(text=c.vSCombat["energie"]) 
			labelCoutFood.config(text=c.vSCombat["nourriture"])
			boutonAcheter.config(command=self.creervaisseauCombat)
		elif typeBatiment is "station":
			labelImage.config(image=self.images["shopStation"])
			labelNom.config(text="Station Solaire",wraplength=90)
			labelCoutMetal.config(text=c.stationS["metal"])
			labelCoutEnergie.config(text=c.stationS["energie"]) 
			labelCoutFood.config(text=c.stationS["nourriture"])

			boutonAcheter.config(command=self.creerstation)
		# grid tout
		# batiment
		labelImage.grid(row=0, column=0, columnspan=2, rowspan=2)
		labelNom.grid(row=2, column=0, columnspan=2)
		labelLvl.grid(row=3, column=0, columnspan=2)
		# ressources -
		labelCoutMetal.grid(row=1, column=3)
		labelCoutEnergie.grid(row=2, column=3)
		labelCoutFood.grid(row=3, column=3)
		# bouton
		boutonAcheter.grid(row=4, column=4)

	def shopTransport(self):
		self.infoShop("transport")

	def shopCombat(self):
		self.infoShop("combat")

	def shopStation(self):
		self.infoShop("station")			
		
	def changeretatvaisseau	(self):
		if self.maselection and "vaisseauinterplanetaires" in self.maselection:
			self.parent.parent.changeretatvaisseau(self.maselection[1])

	def voirplanete(self):
		self.parent.voirplanete(self.maselection)

	def voirgalaxie(self):
		self.parent.voirgalaxie()

	def chargeimages(self, mod):
		self.images["transport"] = {}
		for j in mod.joueurscles:
			image = Image.open("./images/v_transport.png")
			pixel = image.load()
			couleur = image.convert("RGB")
			for i in range(image.size[0]):
				for k in range(image.size[1]):
					r, g, b = couleur.getpixel((i, k))
					if r == self.masque[0] and g == self.masque[1] and b == self.masque[2]:
						bouton = Button()
						r, g, b = bouton.winfo_rgb(mod.joueurs[j].couleur)
						r = int(r / 256)
						g = int(g / 256)
						b = int(b / 256)
						pixel[i, k] = (r, g, b)

			self.images["transport"][j] = image

		self.images["combat"] = {}
		for j in mod.joueurscles:
			image = Image.open("./images/v_combat.png")

			pixel = image.load()
			couleur = image.convert("RGB")
			for i in range(image.size[0]):
				for k in range(image.size[1]):
					r, g, b = couleur.getpixel((i, k))
					if r == self.masque[0] and g == self.masque[1] and b == self.masque[2]:
						bouton = Button()
						r, g, b = bouton.winfo_rgb(mod.joueurs[j].couleur)
						r = int(r / 256)
						g = int(g / 256)
						b = int(b / 256)
						pixel[i, k] = (r, g, b)

			self.images["combat"][j] = image
		self.img = {}
		im = Image.open("./images/v_transportShop.png")
		self.images["shopTransport"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/v_combatShop.png")
		self.images["shopCombat"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/station.png")
		self.images["shopStation"] = ImageTk.PhotoImage(im)
		

	#	 def chargeimages(self):
	#		 im = Image.open("./images/v_attaque.png")
	#		 self.images["attaque"] = ImageTk.PhotoImage(im)
	#		 im = Image.open("./images/v_collonie.png")
	#		 self.images["collonie"] = ImageTk.PhotoImage(im)
	#		 im = Image.open("./images/v_tranport.png")
	#		 self.images["transport"] = ImageTk.PhotoImage(im)

	def initsysteme(self, i):
		self.systeme = i
		self.canevas.config(scrollregion=(0, 0, self.largeur, self.hauteur))
		self.afficherdecor(i)

	def affichermodelestatique(self, i):
		xl = self.largeur / 2
		yl = self.hauteur / 2
		n = i.etoile.taille * self.UA2pixel / 2

		couleur = i.etoile.type
		outcolor = i.etoile.outline
		mini = 2
		UAmini = 4
		self.canevas.create_oval(xl - n, yl - n, xl + n, yl + n, fill=couleur, dash=(1, 2), width=4, outline=outcolor,
								 tags=("systeme", i.id, "etoile", str(n),))
		self.minimap.create_oval(100 - mini, 100 - mini, 100 + mini, 100 + mini, fill=couleur)

		# for p in i.planetes:
		#	x,y=hlp.getAngledPoint(math.radians(p.angle),p.distance*self.UA2pixel,xl,yl)
		#	n=p.taille*self.UA2pixel
		#	self.canevas.create_oval(x-n,y-n,x+n,y+n,fill="red",tags=(i.proprietaire,"planete",p.id,"inconnu",i.id,int(x),int(y)))
		#	x,y=hlp.getAngledPoint(math.radians(p.angle),p.distance*UAmini,100,100)
		#	self.minimap.create_oval(x-mini,y-mini,x+mini,y+mini,fill="red",tags=("planete"))

		# NOTE Il y a un probleme ici je ne parviens pas a centrer l'objet convenablement comme dans la fonction 'identifierplanetemere'
		canl = int(self.canevas.cget("width")) / 2
		canh = int(self.canevas.cget("height")) / 2
		self.canevas.xview(MOVETO, ((self.largeur / 2) - canl) / self.largeur)
		self.canevas.yview(MOVETO, ((self.hauteur / 2) - canh) / self.hauteur)

	def creerimagefond(self, i):
		imgfondpil = Image.new("RGBA", (self.largeur, self.hauteur), "black")
		draw = ImageDraw.Draw(imgfondpil)
		xl = self.largeur / 2
		yl = self.hauteur / 2
		for p in i.planetes:
			d = p.distance * self.UA2pixel
			draw.ellipse((xl - d, yl - d, xl + d, yl + d), outline="white")

		self.images["fond"] = ImageTk.PhotoImage(imgfondpil)
		self.canevas.create_image(self.largeur / 2, self.hauteur / 2, image=self.images["fond"])

	def afficherdecor(self, i):
		self.creerimagefond(i)
		self.affichermodelestatique(i)

	def creervaisseauCombat(self):
		if self.maselection:
			# print(self.maselection)
			self.parent.parent.creervaisseauSolaire(self.maselection[5], self.maselection[2], 1)
			self.maselection = None
			self.canevas.delete("selecteur")

	def creervaisseauTransport(self):
		if self.maselection:
			# print(self.maselection)
			self.parent.parent.creervaisseauSolaire(self.maselection[5], self.maselection[2], 0)
			self.maselection = None
			self.canevas.delete("selecteur")

	def creerstation(self):
		if self.maselection:
			print("creertation: ", self.maselection[5], self.maselection[2])
			self.parent.parent.creerstationSolaire(self.maselection[5], self.maselection[2])
			self.maselection = None
			self.canevas.delete("selecteur")

	def afficherpartie(self, mod):
		self.canevas.delete("planete")
		self.canevas.delete("vaisseauinterplanetaires")
		self.canevas.delete('laser')
		self.canevas.delete("stationSolaire")
		self.minimap.delete("planete")
		self.minimap.delete("vaisseauinterplanetaires")

		xl = self.largeur / 2
		yl = self.hauteur / 2
		mini = 2
		UAmini = 4


		for p in self.systeme.planetes:
			x, y = hlp.getAngledPoint(math.radians(p.angle), p.distance * UAmini, 100, 100)
			self.minimap.create_oval(x - mini, y - mini, x + mini, y + mini, fill=p.couleurPlanete, tags=("planete"))
			x, y = hlp.getAngledPoint(math.radians(p.angle), p.distance * self.UA2pixel, xl, yl)
			n = p.taille * self.UA2pixel
			self.canevas.create_oval(x - n, y - n, x + n, y + n, fill=p.couleurPlanete, tags=(
				self.systeme.proprietaire, "planete", p.id, "inconnu", self.systeme.id, int(x), int(y)))

			if self.maselection != None:
				if p.id == self.maselection[2]:
					self.canevas.delete("select")
					n += 2
					self.canevas.create_oval((x) - n - 1, (y) - n - 1, (x) + n, (y) + n - 1, dash=(2, 2),
											 outline=self.modele.joueurs[self.parent.nom].couleur,
											 tags=("select", "selecteur"))

		for k in mod.joueurscles:
			i = mod.joueurs[k]
			self.img[k] = []
			index = 0
			for j in i.vaisseauxinterplanetaires:
				if j.systeme_courant.id == self.systeme.id:
					jx = int(j.x * self.UA2pixel + xl)
					jy = int(j.y * self.UA2pixel + yl)
					if j.type == 'combat' and j.cibleattaque:
						cx = int(j.cibleattaque.x * self.UA2pixel + xl)
						cy = int(j.cibleattaque.y * self.UA2pixel + yl)
						self.canevas.create_line(jx, jy, cx, cy, fill='red', tags=('laser'))

					self.img[k].append(ImageTk.PhotoImage(self.images[j.type][k].rotate(j.degre - 90)))

					self.canevas.create_image(jx, jy, image=self.img[k][index],
											  tags=(
											  j.proprietaire, "vaisseauinterplanetaires", j.id, j.type, "artefact"))
					index += 1

					# Afficher selection vaisseau
					# print(j.id)
					if self.maselection != None:
						if j.id == self.maselection[1]:
							self.canevas.delete("select")
							n = 10  # Gere la taille de la selection
							self.canevas.create_oval((jx) - n - 1, (jy) - n - 1, (jx) + n, (jy) + n - 1, dash=(2, 2),
													 outline=self.modele.joueurs[self.parent.nom].couleur,
													 tags=("select", "selecteur"))

						# Afficher vaisseaux sur minimap
					if i.nom == self.parent.nom:
						jx = int(jx * 200 / self.largeur)
						jy = int(jy * 200 / self.hauteur)
						# print(jx,jy)
						self.minimap.create_rectangle((jx - mini), (jy - mini), (jx + mini), (jy + mini),
													  fill=i.couleur,tags=(j.proprietaire, "vaisseauinterplanetaires", j.id,j.type, "artefact"))

			#ROATION STATION

			#NOTE MINI-MAP A FAIRE
			for s in i.stationSolaire:
				if s.systemeOrigine.id == self.systeme.id:
					for p in self.systeme.planetes:
						
						
						if p == s.parent:
							x, y = hlp.getAngledPoint(math.radians(p.angle), p.distance * self.UA2pixel,
														  self.largeur / 2, self.largeur / 2)
							x, y = hlp.getAngledPoint(math.radians(s.angle), self.UA2pixel,
														  x, y)
							s.pointOrbite(x,y)
							s.orbiter()
							n = p.taille * self.UA2pixel * 0.7
							
							#DESSINE STATION
							self.canevas.create_oval(s.x - n - 1, s.y - n - 1, s.x + n,  s.y + n - 1, fill=i.couleur, tags=(
							i.nom, "stationSolaire", p.id, "inconnu", self.systeme.id, int(x), int(y)))
							#SELECTION STATION
							if self.maselection != None:
								if i.nom == self.maselection[0] and self.maselection[1] == 'stationSolaire' and self.maselection[3] == p.id:
									self.canevas.delete("select")
									n = 9  # Gere la taille de la selection
									self.canevas.create_oval(s.x - n - 1, s.y - n - 1, s.x + n,  s.y + n - 1, dash=(2, 2),
							                         outline=self.modele.joueurs[self.parent.nom].couleur,
							                         tags=("select", "selecteur"))


	def changerproprietaire(self):
		pass

	def afficherselection(self):

		print('afficherselection')
		self.canevas.delete("selecteur")
		if self.maselection != None:
			systemes = self.modele.systemes
			e = self.UA2pixel

			print(self.maselection)

			# Pas obligé de faire la selection initiale mais plus satisfesant
			if self.maselection[1] == "planete":
				for j in systemes:
					for p in j.planetes:
						if p.id == self.maselection[2]:
							t = (p.taille * e) * 5
							x, y = hlp.getAngledPoint(math.radians(p.angle), p.distance * self.UA2pixel,
													  self.largeur / 2, self.largeur / 2)

							self.canevas.create_oval((x) - t, (y) - t, (x) + t, (y) + t, dash=(2, 2),
													 outline=self.modele.joueurs[self.parent.nom].couleur,
													 tags=("select", "selecteur"))

							p.selectionne = True
			elif self.maselection[1] == "vaisseauinterplanetaires":
				for k in self.parent.joueurscles:
					pass
			elif self.maselection[1] == "stationSolaire":
				print("test")
				joueur = self.modele.joueurs[self.parent.nom]
				for i in joueur.stationSolaire:
					if i.id == self.maselection[2]:
						x, y = hlp.getAngledPoint(math.radians(i.parent.angle), i.parent.distance * self.UA2pixel,
												  self.largeur / 2, self.largeur / 2)
						x, y = hlp.getAngledPoint(math.radians(i.angle), self.UA2pixel,
												  x, y)
						n=i.parent.taille * self.UA2pixel
						self.canevas.create_oval(x-n,y-n,x+n,y+n, dash=(2, 2),outline=joueur.couleur,
												 tags=("select", "selecteur"))

	def cliquervue(self, evt):
		self.changecadreetat(None)

		print('cliquervue!')
		t = self.canevas.gettags("current")
		print(t)
		if t and "etoile" in t:
			print("IN_ETOILE")
			pass
		elif t and "planete" in t:
			if self.maselection and "vaisseauinterplanetaires" in self.maselection:
				print("IN PLANETE + VAISSEAU")
				self.parent.parent.ciblerdestination(self.maselection[1], t[2])

			else:
				print("IN PLANETE")
				nom = t[0]
				idplanete = t[2]
				idsysteme = t[4]
				print(idplanete, idsysteme)
				self.maselection = [self.parent.nom, t[1], t[2], t[5], t[6],
									t[4]]  # prop, type, id; self.canevas.find_withtag(CURRENT)#[0]

			# !!! Modifie Paola 19-10-17
			# if t[1] == "planete" and t[3]=="inconnu":
			#   self.montreplaneteselection()

			# ici je veux envoyer un message comme quoi je visite cette planete
			# et me mettre en mode planete sur cette planete, d'une shot
			# ou est-ce que je fais selection seulement pour etre enteriner par un autre bouton

			# self.parent.parent.atterrirdestination(nom,idsysteme,idplanete)


		elif t and "vaisseauinterplanetaires" in t:
			if not self.maselection and t[0] == self.parent.nom:
				print("IN VAISSEAU")
				self.maselection = [t[0], t[2], t[3], t[1]]

			elif self.maselection:
				if t[0] != self.parent.nom:
					print("ATTAQUE VAISSEAU ENNEMIE")
					self.parent.parent.ciblerdestination(self.maselection[1], t[2])

		elif t and "stationSolaire" in t:
			print("IN STATION")
			print(t)
			self.maselection = [t[0], t[1], t[3], t[2]]
			print(self.maselection)

		else:
			print("Region inconnue")
			self.maselection = None
			self.canevas.delete("selecteur")

	def montreplaneteselection(self):
		self.changecadreetat(self.cadreetataction)

	def afficherartefacts(self, joueurs):
		pass  # print("ARTEFACTS de ",self.nom)

	def cliquerminimap(self, evt):
		x = evt.x
		y = evt.y
		xn = self.largeur / int(self.minimap.winfo_width())
		yn = self.hauteur / int(self.minimap.winfo_height())

		ee = self.canevas.winfo_width()
		ii = self.canevas.winfo_height()
		eex = int(ee) / self.largeur / 2
		eey = int(ii) / self.hauteur / 2

		self.canevas.xview(MOVETO, (x * xn / self.largeur) - eex)
		self.canevas.yview(MOVETO, (y * yn / self.hauteur) - eey)

	def chargedansvaisseaugalactique(self):
		if self.maselection:
			print("DEMANDE CHARGER DANS VAISSEAU GALACTIQUE")
			print(self.maselection)

			x = self.systeme.x
			y = self.systeme.y
			e = self.parent.modes["galaxie"].Al2pixel

			item = self.parent.modes["galaxie"].canevas.find_overlapping(x * e - 20, y * e - 20, x * e + 20, y * e + 20)

			vaisseau = None

			for i in range(len(item)):
				if "vaisseauinterstellaire" == item[i]:
					id = item[i + 1]
					joueurs = self.parent.parent.modele.joueurs
					for j in joueurs:
						for v in j.vaisseauinterstellaires:
							if v.id == id:
								vaisseau = item[i + 1]
								break

			if vaisseau:
				print("CHARGEMENT DANS VAISSEAU GALACTIQUE", vaisseau)
				self.parent.parent.chargedansvaisseaugalactique(vaisseau, self.maselection[2])

			else:
				print("AUCUN VAISSEAU GALACTIQUE PRESENT À CE SYSTEME")

		pass


class VuePlanete(Perspective):
	def __init__(self, parent, syste, plane):
		Perspective.__init__(self, parent)
		self.modele = self.parent.modele

		self.planeteid = plane
		self.planete = None
		self.systeme = syste
		self.infrastructures = {}
		self.maselection = None
		self.prevSelection = None
		self.macommande = None

		self.KM2pixel = 100  # ainsi la terre serait a 100 pixels du soleil et Uranus a 19 Unites Astronomique
		self.largeur = int(self.modele.diametre * self.KM2pixel)
		self.hauteur = self.largeur

		# recherche l'object planet actuel via planetid
		for s in self.modele.systemes:
			if s.id == self.systeme:
				for p in s.planetes:
					if p.id == self.planeteid:
						self.planete = p
		self.canevas.config(scrollregion=(0, 0, self.largeur * 5, self.hauteur * 5))
		self.canevas.config(bg="black")

		self.tailleTile = self.largeur * 5 / self.planete.terrainTailleCarre

		self.tailleterrainpixel = self.tailleTile * self.planete.terrainTailleCarre  # ! AJOUTER VARIABLE

		# ajouter appliquer les couleurs de la carte
		for i in range(self.planete.terrainTailleCarre):
			for j in range(self.planete.terrainTailleCarre):
				self.canevas.create_rectangle(i * self.tailleTile, j * self.tailleTile,
											  i * self.tailleTile + self.tailleTile,
											  j * self.tailleTile + self.tailleTile,
											  fill=self.planete.terrainColor[i][j],
											  outline="")

		self.afficherUI()

	def afficherUI(self):
		Perspective.afficherUI(self)
		self.cadreShop = None
		self.cadreInfoShop = None
		self.cadreJoueur = None
		self.cadreSelection = None
		self.cadreJoueur = None
		self.cadreShopBarrack = None
		
		self.chargeimages()

		boutonBack = Button(self.cadreetat, text="←", command=self.voirsysteme)
		boutonBack.grid(row=0, column=0, sticky=N + W)
		# boutonNext=Button(self.cadreetat,text="→",command=self.voirsysteme)
		# boutonNext.grid(row=0,column=5)

		self.boutonShop = Button(self.cadreetat, text="Shop ˃", command=self.afficherShop)
		self.boutonShop.grid(row=1, column=0, sticky=W)

		self.boutonSelect = Button(self.cadreetat, text="Selection >", command=self.afficherSelection)
		self.boutonSelect.grid(row=10, column=0, sticky=W)
		
		

	def afficherShop(self):
		self.boutonShop.config(text="Shop ˅")
		# enlever les autres cadres
		if self.cadreSelection:
			self.cadreSelection.grid_forget()
			self.boutonSelect.config(text="Selection >")
			self.cadreSelection = None
		else:
			pass

		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		else:
			self.cadreShop = Frame(self.cadreetat, width=200, height=400, bg="blue")
			self.cadreShop.grid(row=3, column=0, columnspan=5, rowspan=5)

			shopVille = Button(self.cadreShop, text="Ville", image=self.images["miniVille"], compound="top",
							   command=self.infoVille)
			shopVille.grid(row=0, column=0)
			shopMine = Button(self.cadreShop, text="Mine", image=self.images["miniMine"], compound="top",
							  command=self.infoMine)
			shopMine.grid(row=0, column=1)
			shopGeneratrice = Button(self.cadreShop, text="Generatrice", image=self.images["miniGen"], compound="top",
									 command=self.infoGeneratrice)
			shopGeneratrice.grid(row=0, column=2)
			shopFerme = Button(self.cadreShop, text="Ferme", image=self.images["miniFerm"], compound="top",
							   command=self.infoFerme)
			shopFerme.grid(row=1, column=0)
			shopBarrack = Button(self.cadreShop, text="Barrack", image=self.images["miniBarra"], compound="top",
								 command=self.infoBarrack)
			shopBarrack.grid(row=1, column=1)

		
#			 # À EFFACER, TEMPORAIRE
#			 shopLazerboi = Button(self.cadreShop, text="Lazerboi", image=self.images["lazerboi"], compound="top",
#								   command=self.infoLazerboi)
#			 shopLazerboi.grid(row=1, column=2)

	def infoShop(self, typeBatiment):
		# couts
		c = Cout()

		# creer cadre
		if self.cadreInfoShop:
			self.cadreInfoShop.grid_forget()
			self.cadreInfoShop = None
		else:
			pass
		self.cadreInfoShop = Frame(self.cadreShop, width=200, height=100)
		self.cadreInfoShop.grid(row=3, column=0, columnspan=5, rowspan=5)
		# Infos batiment
		labelImage = Label(self.cadreInfoShop, image=self.images["miniVille"])
		labelNom = Label(self.cadreInfoShop, text="Ville")
		labelLvl = Label(self.cadreInfoShop, text="Lvl. 1")
		# Cout batiment
		label = Label(self.cadreInfoShop, text="Cout")
		label.grid(row=0, column=2, columnspan=2)
		label = Label(self.cadreInfoShop, text="Metal")
		label.grid(row=1, column=2)
		label = Label(self.cadreInfoShop, text="Energie")
		label.grid(row=2, column=2)
		label = Label(self.cadreInfoShop, text="Food")
		label.grid(row=3, column=2)

		labelCoutMetal = Label(self.cadreInfoShop, text="")
		labelCoutEnergie = Label(self.cadreInfoShop, text="")
		labelCoutFood = Label(self.cadreInfoShop, text="")
		# Boutons
		boutonAcheter = Button(self.cadreInfoShop, text="Acheter")
		if typeBatiment is "ville":
			labelImage.config(image=self.images["miniVille"])
			labelNom.config(text="Ville")
			labelCoutMetal.config(text=c.ville["metal"])
			labelCoutEnergie.config(text=c.ville["energie"])
			labelCoutFood.config(text=c.ville["nourriture"])
			boutonAcheter.config(command=self.creerville)
		elif typeBatiment is "mine":
			labelImage.config(image=self.images["miniMine"])
			labelNom.config(text="Mine")
			labelCoutMetal.config(text=c.mine["metal"])
			labelCoutEnergie.config(text=c.mine["energie"])
			labelCoutFood.config(text=c.mine["nourriture"])
			boutonAcheter.config(command=self.creermine)
		elif typeBatiment is "generatrice":
			labelImage.config(image=self.images["miniGen"])
			labelNom.config(text="Generatrice")
			labelCoutMetal.config(text=c.generatrice["metal"])
			labelCoutEnergie.config(text=c.generatrice["energie"])
			labelCoutFood.config(text=c.generatrice["nourriture"])
			boutonAcheter.config(command=self.creergeneratrice)
		elif typeBatiment is "ferme":
			labelImage.config(image=self.images["miniFerm"])
			labelNom.config(text="Ferme")
			labelCoutMetal.config(text=c.generatrice["metal"])
			labelCoutEnergie.config(text=c.generatrice["energie"])
			labelCoutFood.config(text=c.generatrice["nourriture"])
			boutonAcheter.config(command=self.creeferme)
		elif typeBatiment is "barrack":
			labelImage.config(image=self.images["miniBarra"])
			labelNom.config(text="Barrack")
			labelCoutMetal.config(text=c.generatrice["metal"])
			labelCoutEnergie.config(text=c.generatrice["energie"])
			labelCoutFood.config(text=c.generatrice["nourriture"])
			boutonAcheter.config(command=self.creeBarrack)
		elif typeBatiment is "lazerboi":
			labelImage.config(image=self.images["miniBarra"])
			labelNom.config(text="Barrack")
			labelCoutMetal.config(text=c.generatrice["metal"])
			labelCoutEnergie.config(text=c.generatrice["energie"])
			labelCoutFood.config(text=c.generatrice["nourriture"])
			boutonAcheter.config(command=self.creeLazerboi)
		# grid tout
		# batiment
		labelImage.grid(row=0, column=0, columnspan=2, rowspan=2)
		labelNom.grid(row=2, column=0, columnspan=2)
		labelLvl.grid(row=3, column=0, columnspan=2)
		# ressources -
		labelCoutMetal.grid(row=1, column=3)
		labelCoutEnergie.grid(row=2, column=3)
		labelCoutFood.grid(row=3, column=3)
		# bouton
		boutonAcheter.grid(row=4, column=4)


	
	def infoVille(self):
		self.macommande = None
		self.infoShop("ville")

	def infoMine(self):
		self.macommande = None
		self.infoShop("mine")

	def infoGeneratrice(self):
		self.macommande = None
		self.infoShop("generatrice")

	def infoFerme(self):
		self.macommande = None
		self.infoShop("ferme")

	def infoBarrack(self):
		self.macommande = None
		self.infoShop("barrack")

	# A EFFACER! TEMPORAIRE
	def infoLazerboi(self):
		self.macommande = None
		self.infoShop("lazerboi")

	def creermine(self):
		self.macommande = "mine"

	def creerville(self):
		self.macommande = "ville"

	def creergeneratrice(self):
		self.macommande = "generatrice"
		print('WOW une génératrice')

	def creeferme(self):
		self.macommande = "ferme"
		print('MOOOooooo')

	def creeBarrack(self):
		self.macommande = "barrack"
		print('Fo\' the emperor!')

	def creeLazerboi(self):
		self.macommande = "lazerboi"
		print("pew pew pew")

	def voirsysteme(self):
		for i in self.modele.joueurs[self.parent.nom].systemesvisites:
			if i.id == self.systeme:
				self.parent.voirsysteme(i)

	def initplanete(self, sys, plane):
		s = None
		p = None
		for i in self.modele.joueurs[self.parent.nom].systemesvisites:
			if i.id == sys:
				s = i
				for j in i.planetes:
					if j.id == plane:
						p = j
						break
		self.systemeid = sys
		self.planeteid = plane
		self.affichermodelestatique(s, p)
		for i in self.planete.infrastructures:
			self.parent.afficherBatiment(i)

	def affichermodelestatique(self, s, p):
		self.chargeimages()
		xl = self.largeur / 2
		yl = self.hauteur / 2
		mini = 2
		UAmini = 4
		t = 200 / p.terrainTailleCarre  # 200 c'Est la taille du du minimap

		self.canevas.create_image(p.posXatterrissage, p.posYatterrissage, image=self.images["ville"])

		for i in range(p.terrainTailleCarre):
			for j in range(p.terrainTailleCarre):
				self.minimap.create_rectangle(i * t, j * t, i * t + t, j * t + t, fill=p.terrainColor[i][j],
											  outline="");

		canl = int(p.posXatterrissage - 100) / self.largeur
		canh = int(p.posYatterrissage - 100) / self.hauteur
		self.canevas.xview(MOVETO, canl)
		self.canevas.yview(MOVETO, canh)

	def chargeimages(self):
		im = Image.open("./images/ville_100.png")
		self.images["ville"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/mine_100.png")
		self.images["mine"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/generatrice_100.png")
		self.images["generatrice"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/ferme_100.png")
		self.images["ferme"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/mine_100.png")
		self.images["barrack"] = ImageTk.PhotoImage(im)

		im = Image.open("./images/ville_50.png")
		self.images["miniVille"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/mine_50.png")
		self.images["miniMine"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/generatrice_50.png")
		self.images["miniGen"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/ferme_50.png")
		self.images["miniFerm"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/mine_50.png")
		self.images["miniBarra"] = ImageTk.PhotoImage(im)
		im = Image.open("./images/Fichier_2.png")
		self.images["lazerboi"] = ImageTk.PhotoImage(im)

	def afficherdecor(self):
		pass

	def afficherpartie(self, mod):
		for k in mod.joueurscles:
			joueur = mod.joueurs[k]
			self.parent.effacerLazerBoi()
			for at in joueur.attaquantTerre:
				self.parent.afficherLazerBoi(at)

		pass

	def changerproprietaire(self, prop, couleur, systeme):
		pass

	# UI
	def afficherSelection(self):  # si on clique sur le bouton Selection
		self.boutonSelect.config(text="Selection ˅")
		# Fermer les autres cadres
		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		else:
			pass
		# Si Selection est ouvert, fermer
		if self.cadreSelection != None:
			self.cadreSelection.grid_forget()
			self.boutonSelect.config(text="Selection ˃")
			self.cadreSelection = None
		else:
			# Sinon, on ouvre le cadre selection
			self.cadreSelection = Frame(self.cadreetat, width=200, height=300, bg="blue")
			self.cadreSelection.grid(row=11, column=0, columnspan=5, rowspan=5)
			if self.maselection is None:
				# Mais, si on a rien selectionne, demander de selectionner
				label = Label(self.cadreSelection, text="Veillez selectionner un objet")
				label.grid()
			else:
				# Si on a selectionne qqch, le montrer
				self.selectBatiment()

	def selectBatiment(self):  # Si on clique sur un batiment, montrer selection
		self.boutonSelect.config(text="Selection ˅")
		# Fermer les autres cadres
		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		# S'assurer que le conteneur est ouvert
		if self.cadreSelection is None:
			self.cadreSelection = Frame(self.cadreetat, width=300, height=300, bg="blue")
			self.cadreSelection.grid(row=11, column=0, columnspan=5, rowspan=5)
		else:
			for widget in self.cadreSelection.winfo_children():
				widget.destroy()
		# Cadre selection
		if self.maselection and self.maselection[0] != "current":
			self.cadreShopBarrack = None
			
			if self.maselection[2] == "batiment":
				# peupler le cadre
				labelImage = Label(self.cadreSelection)
				labelNom = Label(self.cadreSelection)
				labelLvl = Label(self.cadreSelection)
				if self.maselection[1] == "barrack":
					labelImage.config(image=self.images["miniBarra"])
					labelNom.config(text="Barracks")
					for i in self.planete.infrastructures:
							if i.type == "barrack":
								labelLvl.config(text="lvl " + str(i.niveau))
					label = Label(self.cadreSelection, text="Unites")
					label.grid(row=0, column=2)
					unit1 = Button(self.cadreSelection, text="Lazer boiz", command=self.infoShopLazer)
					unit1.grid(row=1, column=2)
#					 unit2 = Button(self.cadreSelection, text="Fist boiz")
#					 unit2.grid(row=2, column=2)
#					 unit3 = Button(self.cadreSelection, text="Tank boiz")
#					 unit3.grid(row=3, column=2)
#					 unit1 = Button(self.cadreSelection, text="Upgrade")
#					 unit1.grid(row=0, column=3)
				elif self.maselection[1] == "lazerboi":
					print("yes")
					self.shopSelection("lazer")
				else:
					label = Label(self.cadreSelection, text="Ressources")
					label.grid(row=0, column=2, columnspan=2)
					label = Label(self.cadreSelection, text="Metal")
					label.grid(row=1, column=2)
					label = Label(self.cadreSelection, text="Energie")
					label.grid(row=2, column=2)
					label = Label(self.cadreSelection, text="Food")
					label.grid(row=3, column=2)
					labelMetal = Label(self.cadreSelection)
					labelEnergie = Label(self.cadreSelection)
					labelFood =Label(self.cadreSelection)

					# recup ressources generees
					idSelect = self.maselection[0]
					if self.maselection[1] == "mine":
						labelImage.config(image=self.images["miniMine"])
						labelNom.config(text="Mine")  # a modifier
						for i in self.planete.infrastructures:
							if i.id == idSelect:
								labelLvl.config(text="lvl " + str(i.niveau))
								labelMetal = Label(self.cadreSelection, text=str(round(i.metauxgen * i.controleRessource,2))+"/sec")
								labelEnergie = Label(self.cadreSelection, text=str(round(i.energiegen * i.controleRessource,2))+"/sec")
								labelFood = Label(self.cadreSelection, text=str(round(i.foodgen * i.controleRessource,2))+"/sec")
								break
					elif self.maselection[1] == "generatrice":
						labelImage.config(image=self.images["miniGen"])
						labelNom.config(text="Generatrice")  # a modifier
						for i in self.planete.infrastructures:
							if i.id == idSelect:
								labelLvl.config(text="lvl " + str(i.niveau))
								labelMetal = Label(self.cadreSelection, text=str(round(i.metauxgen * i.controleRessource,2))+"/sec")
								labelEnergie = Label(self.cadreSelection, text=str(round(i.energiegen * i.controleRessource,2))+"/sec")
								labelFood = Label(self.cadreSelection, text=str(round(i.foodgen * i.controleRessource,2))+"/sec")
								break
					elif self.maselection[1] == "ferme":
						labelImage.config(image=self.images["miniFerm"])
						labelNom.config(text="Ferme")  # a modifier
						for i in self.planete.infrastructures:
							if i.id == idSelect:
								labelLvl.config(text="lvl " + str(i.niveau))
								labelMetal = Label(self.cadreSelection, text=str(round(i.metauxgen * i.controleRessource,2))+"/sec")
								labelEnergie = Label(self.cadreSelection, text=str(round(i.energiegen * i.controleRessource,2))+"/sec")
								labelFood = Label(self.cadreSelection, text=str(round(i.foodgen * i.controleRessource,2))+"/sec")
								break
					elif self.maselection[1] == "ville":
						labelImage.config(image=self.images["miniVille"])
						labelNom.config(text="Ville")  # a modifier
						for i in self.planete.infrastructures:
							if i.id == idSelect:
								labelLvl.config(text="lvl " + str(i.niveau))
								labelMetal = Label(self.cadreSelection, text=str(round(i.metauxgen * i.controleRessource,2))+"/sec")
								labelEnergie = Label(self.cadreSelection, text=str(round(i.energiegen * i.controleRessource,2))+"/sec")
								labelFood = Label(self.cadreSelection, text=str(round(i.foodgen * i.controleRessource,2))+"/sec")
								break
					labelMetal.grid(row=1, column=3)
					labelEnergie.grid(row=2, column=3)
					labelFood.grid(row=3, column=3)
				# batiment
				labelImage.grid(row=0, column=0, columnspan=2, rowspan=2)
				labelNom.grid(row=2, column=0, columnspan=2)
				labelLvl.grid(row=3, column=0, columnspan=2)
	def infoShopLazer(self):
		self.shopSelection("lazer")
	def infoShopFist(self):
		self.shopSelection("fist")
	def infoShopTank(self):
		self.shopSelection("tank")
	def selectUnit(self, unitName):
		print("ok")
		self.boutonSelect.config(text="Selection ˅")
		# Fermer les autres cadres
		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		# S'assurer que le conteneur est ouvert
		if self.cadreSelection is None:
			self.cadreSelection = Frame(self.cadreetat, width=300, height=300, bg="blue")
			self.cadreSelection.grid(row=11, column=0, columnspan=5, rowspan=5)
		else:
			for widget in self.cadreSelection.winfo_children():
				widget.destroy()
		# Cadre selection
		self.cadreShopBarrack = None
		if unitName == "lazerboi":
			# peupler le cadre
			labelImage = Label(self.cadreSelection)
			labelNom = Label(self.cadreSelection, text="Lazerboi")
			labelLvl = Label(self.cadreSelection, text="lvl 1")
			labelImage.config(image=self.images["lazerboi"])
			labelImage.grid(row=0, column=0, columnspan=2, rowspan=2)
			labelNom.grid(row=2, column=0, columnspan=2)
			labelLvl.grid(row=3, column=0, columnspan=2)
#			 label = Label(self.cadreSelection, text="Position")
#			 label.grid(row=1, column=2)
			label = Label(self.cadreSelection, text="HP ")
			label.grid(row=0, column=2)
			
			label = Label(self.cadreSelection, text="")
			label.grid(row=0, column=3)
			label = Label(self.cadreSelection, text="Target")
			label.grid(row=1, column=2)
			label = Label(self.cadreSelection, text="X " + str(self.moveX))
			label.grid(row=2, column=2)
			label = Label(self.cadreSelection, text="Y " + str(self.moveY))
			label.grid(row=3, column=2)
			btnCharger = Button(self.cadreSelection, text="Charger Units", wraplength=80)
			btnCharger.grid(row=4,column=4)
				
			
	def shopSelection(self, type):
		# couts
		c = Cout()

		# creer cadre
		if self.cadreShopBarrack:
			self.cadreShopBarrack.grid_forget()
			self.cadreShopBarrack = None
		else:
			pass
		self.cadreShopBarrack = Frame(self.cadreSelection, width=200, height=100, bg="red")
		self.cadreShopBarrack.grid(row=4, column=0, columnspan=5, rowspan=5)
		# Infos batiment
		labelImage = Label(self.cadreShopBarrack)
		labelNom = Label(self.cadreShopBarrack)
		labelLvl = Label(self.cadreShopBarrack)
		# Cout batiment
		label = Label(self.cadreShopBarrack, text="Cout")
		label.grid(row=0, column=2, columnspan=2)
		label = Label(self.cadreShopBarrack, text="Metal")
		label.grid(row=1, column=2)
		label = Label(self.cadreShopBarrack, text="Energie")
		label.grid(row=2, column=2)
		label = Label(self.cadreShopBarrack, text="Food")
		label.grid(row=3, column=2)

		labelCoutMetal = Label(self.cadreShopBarrack, text="")
		labelCoutEnergie = Label(self.cadreShopBarrack, text="")
		labelCoutFood = Label(self.cadreShopBarrack, text="")
		# Boutons
		boutonAcheter = Button(self.cadreShopBarrack, text="Acheter")
		if type is "lazer":
			labelImage.config(image=self.images["lazerboi"])
			labelNom.config(text="Lazer boiz")
			labelCoutMetal.config(text=c.lazerboi["metal"])
			labelCoutEnergie.config(text=c.lazerboi["energie"])
			labelCoutFood.config(text=c.lazerboi["nourriture"])
			for i in self.planete.infrastructures:
				if i.type == "barrack":
					#lvlLazer = i.dictUnitTemplate["AT_TYPE.LAZERBOI"]["ATP.LVL"]
					#lvlLazer = i.dictUnitTemplate[0][14]
					#lvlLazer = i.dictUnitTemplate["AT_TYPE.LAZERBOI: 0"]
					#print(lvlLazer)
					labelLvl.config(text="lvl " + str(i.niveau))
					lvlLazer = i.niveau
					if lvlLazer == 1:
						boutonAcheter.config(command=self.creeLazerboi)
					else:
						boutonAcheter.config(text="Upgrade")
		# grid tout
		# batiment
		labelImage.grid(row=0, column=0, columnspan=2, rowspan=2)
		labelNom.grid(row=2, column=0, columnspan=2)
		labelLvl.grid(row=3, column=0, columnspan=2)
		# ressources -
		labelCoutMetal.grid(row=1, column=3)
		labelCoutEnergie.grid(row=2, column=3)
		labelCoutFood.grid(row=3, column=3)
		# bouton
		boutonAcheter.grid(row=4, column=4)
		
	def cliquervue(self, evt):
		t = self.canevas.gettags("current")
		# afficherSelection
		if t and t[0] != "current":

			self.maselection = None
			if t[0] == self.parent.nom:
				pass

			elif t[1] == "mine":
				print("mine mine mine")  # !!!
				pass
			elif self.prevSelection != None:
				if t[1] == "lazerboi" and self.prevSelection[1]:
					self.parent.parent.attackLazerBoi(self.prevSelection[0], t[0]);
					self.prevSelection = None
					
			elif t[1] == "lazerboi":
				self.maselection = "lazerboi"
				self.selectUnit("lazerboi")
				print("lazerboi at your service, pew pew.")  # !!!
				self.prevSelection = t
			elif t[2] == "batiment":
				self.maselection = t
				self.selectBatiment()



		else:
			x = self.canevas.canvasx(evt.x) / self.tailleTile
			y = self.canevas.canvasy(evt.y) / self.tailleTile
			
			globalX = self.canevas.canvasx(evt.x)
			globalY = self.canevas.canvasy(evt.y)
			self.moveX = globalX
			self.moveY = globalY
			# print(x,y)
			# if not clicked on Object
			self.maselection = None
			# Reset all selection
			if self.cadreSelection != None:
				self.cadreSelection.grid_forget()
				self.boutonSelect.config(text="Selection ˃")
				self.cadreSelection = None

			if self.macommande == "mine":
				self.parent.parent.creermine(self.parent.nom, self.systemeid, self.planeteid, x, y)
			elif self.macommande == "generatrice":
				self.parent.parent.creergeneratrice(self.parent.nom, self.systemeid, self.planeteid, x, y)
				print("image generatrice")
			elif self.macommande == "ferme":
				self.parent.parent.creerferme(self.parent.nom, self.systemeid, self.planeteid, x, y)
				print("image ferme")
				self.macommande = None
			elif self.macommande is "ville":
				self.parent.parent.creerville(self.parent.nom, self.systemeid, self.planeteid, x, y)
				self.macommande = None
			elif self.macommande is "barrack":
				self.parent.parent.creerbarrack(self.parent.nom, self.systemeid, self.planeteid, x, y)
				self.macommande = None
			elif self.macommande is "lazerboi":
				print("hey!")
				self.parent.parent.creerLazerboi(self.parent.nom, self.systemeid, self.planeteid, globalX, globalY)
				self.macommande = None
				self.selectUnit("lazerboi")
			elif self.prevSelection and self.prevSelection[1] == "lazerboi":
				self.selectUnit("lazerboi")
				self.parent.parent.moveAttaquant(self.prevSelection[0], globalX, globalY)
				self.prevSelection = None
				
	def montresystemeselection(self):
		self.changecadreetat(self.cadreetataction)

	def montrevaisseauxselection(self):
		self.changecadreetat(self.cadreetatmsg)

	def afficherartefacts(self, joueurs):
		pass  # print("ARTEFACTS de ",self.nom)

	def cliquerminimap(self, evt):
		x = evt.x
		y = evt.y
		largeur = self.tailleterrainpixel
		hauteur = self.tailleterrainpixel
		xn = largeur / int(self.minimap.winfo_width())
		yn = hauteur / int(self.minimap.winfo_height())

		ee = self.canevas.winfo_width()
		ii = self.canevas.winfo_height()
		eex = int(ee) / largeur / 2
		eey = int(ii) / hauteur / 2

		self.canevas.xview(MOVETO, (x * xn / largeur) - eex)
		self.canevas.yview(MOVETO, (y * yn / hauteur) - eey)


if __name__ == '__main__':
	m = Vue(0, "jmd", "127.0.0.1")
	m.root.mainloop()
