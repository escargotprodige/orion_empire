# -*- coding: utf-8 -*-
from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import os, os.path
import random
import math
from helper import Helper as hlp
from mathPlus import *


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
		self.canevasplash = Canvas(self.cadresplash, width=640, height=480, bg="red")
		self.canevasplash.pack()
		self.nomsplash = Entry(bg="pink")
		self.nomsplash.insert(0, nom)
		self.ipsplash = Entry(bg="pink")
		self.ipsplash.insert(0, ip)
		labip = Label(text=ip, bg="red", borderwidth=0, relief=RIDGE)
		btncreerpartie = Button(text="Creer partie", bg="pink", command=self.creerpartie)
		btnconnecterpartie = Button(text="Connecter partie", bg="pink", command=self.connecterpartie)
		self.canevasplash.create_window(200, 200, window=self.nomsplash, width=100, height=30)
		self.canevasplash.create_window(200, 250, window=self.ipsplash, width=100, height=30)
		self.canevasplash.create_window(200, 300, window=labip, width=100, height=30)
		self.canevasplash.create_window(200, 350, window=btncreerpartie, width=100, height=30)
		self.canevasplash.create_window(200, 400, window=btnconnecterpartie, width=100, height=30)

	def creercadrelobby(self):
		self.cadrelobby = Frame(self.root)
		self.canevaslobby = Canvas(self.cadrelobby, width=640, height=480, bg="lightblue")
		self.canevaslobby.pack()
		self.listelobby = Listbox(bg="red", borderwidth=0, relief=FLAT)
		self.diametre = Entry(bg="pink")
		self.diametre.insert(0, 5)
		self.densitestellaire = Entry(bg="pink")
		self.densitestellaire.insert(0, 2)
		self.qteIA = Entry(bg="pink")
		self.qteIA.insert(0, 0)
		self.btnlancerpartie = Button(text="Lancer partie", bg="pink", command=self.lancerpartie, state=DISABLED)
		self.canevaslobby.create_window(440, 240, window=self.listelobby, width=200, height=400)
		self.canevaslobby.create_window(200, 200, window=self.diametre, width=100, height=30)
		self.canevaslobby.create_text(20, 200, text="Diametre en annee lumiere")

		self.canevaslobby.create_window(200, 250, window=self.densitestellaire, width=100, height=30)
		self.canevaslobby.create_text(20, 250, text="Nb systeme/AL cube")

		self.canevaslobby.create_window(200, 300, window=self.qteIA, width=100, height=30)
		self.canevaslobby.create_text(20, 300, text="Nb d'IA")

		self.canevaslobby.create_window(200, 450, window=self.btnlancerpartie, width=100, height=30)

	def creercadreloading(self):
		self.cadreloading = Frame(self.root)
		self.canevasloading = Canvas(self.cadreloading, width=640, height=480, bg="white")
		self.canevasloading.create_text(320, 240, font=("Arial", 36), text="Chargement en cours...")
		self.canevasloading.pack()

	def voirgalaxie(self):
		# A FAIRE comme pour voirsysteme et voirplanete, tester si on a deja la vuegalaxie
		#         sinon si on la cree en centrant la vue sur le systeme d'ou on vient
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
		# 200 c'Est la taille du du minimap

		for i in self.modes["planetes"].keys():
			if i == Batiment.planeteid:
				p = 200 / self.modes["planetes"][i].planete.terrainTailleCarre
				couleur = self.modele.joueurs[Batiment.proprietaire].couleur
				t = 200 / self.modes["planetes"][i].largeur
				x = Batiment.x
				y = Batiment.y

				im = self.modes["planetes"][i].images[Batiment.type]
				self.modes["planetes"][i].canevas.create_image(Batiment.x, Batiment.y, image=im,
				                                               tags=(Batiment.id, Batiment.type))

				self.modes["planetes"][i].minimap.create_oval(x * t - p, y * t - p, x * t + p, y * t + p, fill=couleur,
				                                              tags=(Batiment.id, Batiment.type))

				break

	def effacerBatiment(self, Batiment):
		for i in self.modes["planetes"].keys():
			if i == Batiment.planeteid:
				self.modes["planetes"][i].canevas.delete(Batiment.id)
				self.modes["planetes"][i].minimap(Batiment.id)
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


class Perspective(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent.cadrejeu)
		self.parent = parent
		self.modele = None
		self.cadreetatactif = None
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

		self.labid = Label(self.cadreetat, text=self.parent.nom)
		self.labid.grid(row=8, column=0)

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

		self.cadreRessources = Frame(self.cadreinfo, width=200, height=50, bg="white")
		self.cadreRessources.pack()

		# self.cadreRessources1=Frame(self.cadreRessources,width=100,height=30,bg="yellow")
		# self.cadreRessources1.pack()

		self.r1 = StringVar();
		self.r2 = StringVar();
		self.r3 = StringVar();

		rWidth = 9
		rHeight = 2
		self.ressources = Label(self.cadreRessources, width=rWidth, height=rHeight, bg="yellow",
		                        textvariable=self.r1)  # !
		self.ressources.pack(side=LEFT)
		self.ressources = Label(self.cadreRessources, width=rWidth, height=rHeight, bg="green",
		                        textvariable=self.r2)  # !
		self.ressources.pack(side=LEFT)
		self.ressources = Label(self.cadreRessources, width=rWidth, height=rHeight, bg="red", textvariable=self.r3)  # !
		self.ressources.pack(side=LEFT)

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

		self.r1.set(str(joueur.ressource1))
		self.r2.set(str(joueur.ressource2))
		self.r3.set(str(joueur.ressource3))


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

		boutonNext = Button(self.cadreetat, text="→", command=self.voirsysteme)
		boutonNext.grid(row=0, column=5)

		self.boutonShop = Button(self.cadreetat, text="Shop ˃", command=self.afficherShop)
		self.boutonShop.grid(row=2, column=0)

		self.cadreSelectionVaisseau = Frame(self.cadreetat, bg="grey20")  # MODIF début

		self.lbselectecible = Label(self.cadreSelectionVaisseau, text="Choisir cible", bg="darkgrey")
		self.lbselectecible.grid(row=0, column=0)

		self.btndechargervaisseau = Button(self.cadreSelectionVaisseau, text="Décharger vaisseau",
		                                   command=self.dechargerVaisseauGalactique)
		self.btndechargervaisseau.grid(row=1, column=0)

		self.btncreervaisseau = Button(self.cadreSelectionVaisseau, text="Upgrade vitesse vaisseau",
		                               command=self.upgradeVitesseVaisseau)
		self.btncreervaisseau.grid(row=2, column=0)

	def afficherShop(self):
		self.boutonShop.config(text="Shop ˅")
		# self.cadreShop=Frame(self.cadreetat,width=200,height=200,bg="blue")

		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		else:
			self.cadreShop = Frame(self.cadreetat, width=200, height=200, bg="blue")
			self.cadreShop.grid(row=3, column=0, columnspan=5, rowspan=5)
			shopVaisseau = Button(self.cadreShop, text="Vaisseau", command=self.creervaisseauGalactique)
			shopVaisseau.grid(row=0, column=0)
			shopStation = Button(self.cadreShop, text="Station", command=self.creerstationGalactique)
			shopStation.grid(row=0, column=1)  # MODIF fin

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
					if r == 255 and g == 255 and b == 255:
						bouton = Button()
						r, g, b = bouton.winfo_rgb(mod.joueurs[j].couleur)
						r = int(r / 256)
						g = int(g / 256)
						b = int(b / 256)
						pixel[i, k] = (r, g, b)

			self.images["chasseur"][j] = image
		self.img = {}

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
		#    couleur=self.modele.joueurs[i].couleur

		#    for j in self.modele.joueurs[i].systemesvisites:
		#        s=self.canevas.find_withtag(j.id)
		#        self.canevas.addtag_withtag(i, s)
		#        self.canevas.itemconfig(s,fill="grey80")
		#
		#        self.minimap.create_oval((j.x*me)-m,(j.y*me)-m,(j.x*me)+m,(j.y*me)+m,fill="grey80",tags=("systeme",j.id))

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
		print("station Galactique EN CONSTRUCTION")
		if self.maselection:
			self.parent.parent.creerstationGalactique(self.maselection[2])
			self.maselection = None
			self.canevas.delete("selecteur")

	def afficherpartie(self, mod):
		self.canevas.delete("artefact")
		self.canevas.delete("pulsar")
		self.afficherselection()
		self.minimap.delete("vaisseauinterstellaire")

		e = self.AL2pixel
		me = 200 / self.modele.diametre
		m = 2

		for i in mod.pulsars:  # ------------------------- cree les pulsars en premier pour les afficher  sous les vaisseaux
			t = i.taille
			self.canevas.create_oval((i.x * e) - t, (i.y * e) - t, (i.x * e) + t, (i.y * e) + t, fill="orchid3",
			                         dash=(1, 1),
			                         outline="maroon1", width=2,
			                         tags=("inconnu", "pulsar", i.id))

		for k in mod.joueurscles:
			i = mod.joueurs[k]
			self.img[k] = []
			index = 0
			for j in i.vaisseauxinterstellaires:
				jx = j.x * e
				jy = j.y * e

				# self.canevas.create_line(x,y,x0,y0,fill="yellow",width=3,
				#                         tags=(j.proprietaire,"vaisseauinterstellaire",j.id,"artefact"))
				# self.canevas.create_line(x0,y0,x1,y1,fill=i.couleur,width=4,
				#                         tags=(j.proprietaire,"vaisseauinterstellaire",j.id,"artefact"))
				# self.canevas.create_line(x1,y1,x2,y2,fill="red",width=2,
				#                         tags=(j.proprietaire,"vaisseauinterstellaire",j.id,"artefact"))
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

		for i in mod.joueurscles:
			i = mod.joueurs[i]
			for j in i.stationGalactiques:
				self.canevas.create_oval(j.x * e - 5, j.y * e - 5, j.x * e - 15, j.y * e - 15, fill=i.couleur,
				                         outline="white", tags=(j.proprietaire, "StationGalactique", j.id, "artefact"))

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
						y = i.y
						t = 10
						self.canevas.create_rectangle((x * e) - t, (y * e) - t, (x * e) + t, (y * e) + t, dash=(2, 2),
						                              outline=joueur.couleur,
						                              tags=("select", "selecteur"))

			elif self.maselection[1] == "StationGalactique":
				for i in joueur.stationGalactiques:
					if i.id == self.maselection[2]:
						x = i.x
						y = i.y
						t = 10
						self.canevas.create_oval((x * e), (y * e), (x * e - 20), (y * e - 20), dash=(2, 2),
						                         outline=joueur.couleur,
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

		self.afficherUI()

	def afficherUI(self):
		Perspective.afficherUI(self)

		self.cadreShop = None
		self.cadreJoueur = None
		self.cadreSelection = None

		boutonBack = Button(self.cadreetat, text="←", command=self.voirgalaxie)
		boutonBack.grid(row=0, column=0)
		boutonNext = Button(self.cadreetat, text="→", command=self.voirplanete)
		boutonNext.grid(row=0, column=5)

		self.boutonShop = Button(self.cadreetat, text="Shop ˃", command=self.afficherShop)
		self.boutonShop.grid(row=2, column=0)

	def afficherShop(self):
		self.boutonShop.config(text="Shop ˅")
		# self.cadreShop=Frame(self.cadreetat,width=200,height=200,bg="blue")

		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		else:
			self.cadreShop = Frame(self.cadreetat, width=200, height=200, bg="blue")
			self.cadreShop.grid(row=3, column=0, columnspan=5, rowspan=5)
			shopVaisseau = Button(self.cadreShop, text="Vaisseau", command=self.creervaisseau)
			shopVaisseau.grid(row=0, column=0)
			shopStation = Button(self.cadreShop, text="Station", command=self.creerstation)
			shopStation.grid(row=0, column=1)

	def voirplanete(self):
		self.parent.voirplanete(self.maselection)

	def voirgalaxie(self):
		self.parent.voirgalaxie()

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
		#    x,y=hlp.getAngledPoint(math.radians(p.angle),p.distance*self.UA2pixel,xl,yl)
		#    n=p.taille*self.UA2pixel
		#    self.canevas.create_oval(x-n,y-n,x+n,y+n,fill="red",tags=(i.proprietaire,"planete",p.id,"inconnu",i.id,int(x),int(y)))
		#    x,y=hlp.getAngledPoint(math.radians(p.angle),p.distance*UAmini,100,100)
		#    self.minimap.create_oval(x-mini,y-mini,x+mini,y+mini,fill="red",tags=("planete"))

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

	def creervaisseau(self):
		if self.maselection:
			print(self.maselection)
			self.parent.parent.creervaisseauSolaire(self.maselection[4],self.maselection[2],0)
			self.maselection = None
			self.canevas.delete("selecteur")

	def creerstation(self):
		print("Creer station EN CONSTRUCTION")

	def afficherpartie(self, mod):
		self.canevas.delete("planete")
		self.minimap.delete("planete")

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

	def changerproprietaire(self):
		pass

	def afficherselection(self):
		self.canevas.delete("selecteur")
		if self.maselection != None:
			systemes = self.modele.systemes

			e = self.UA2pixel

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
			'''
			elif self.maselection[1] == "vaisseauSolaire":
				for i in joueur.vaisseauxinterstellaires:
					if i.id == self.maselection[2]:
						x = i.x
						y = i.y
						t = 10
						self.canevas.create_rectangle((x * e) - t, (y * e) - t, (x * e) + t, (y * e) + t, dash=(2, 2),
						                              outline=joueur.couleur,
						                              tags=("select", "selecteur"))
			'''
	def cliquervue(self, evt):
		self.changecadreetat(None)

		t = self.canevas.gettags("current")
		print(t)
		if t and "etoile" in t:
			print("IN_ETOILE")
			pass
		elif t and "planete" in t:
			nom = t[0]
			idplanete = t[2]
			idsysteme = t[4]
			self.maselection = [self.parent.nom, t[1], t[2], t[5], t[6],
			                    t[4]]  # prop, type, id; self.canevas.find_withtag(CURRENT)#[0]
			# !!! Modifie Paola 19-10-17
			# if t[1] == "planete" and t[3]=="inconnu":
			#   self.montreplaneteselection()

			# ici je veux envoyer un message comme quoi je visite cette planete
			# et me mettre en mode planete sur cette planete, d'une shot
			# ou est-ce que je fais selection seulement pour etre enteriner par un autre bouton

			# self.parent.parent.atterrirdestination(nom,idsysteme,idplanete)
		else:
			print("Region inconnue")
			self.maselection = None
			# self.lbselectecible.pack_forget()
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

		tailleTile = self.largeur * 5 / self.planete.terrainTailleCarre

		self.tailleterrainpixel = tailleTile * self.planete.terrainTailleCarre  # ! AJOUTER VARIABLE

		# ajouter appliquer les couleurs de la carte
		for i in range(self.planete.terrainTailleCarre):
			for j in range(self.planete.terrainTailleCarre):
				self.canevas.create_rectangle(i * tailleTile, j * tailleTile, i * tailleTile + tailleTile,
				                              j * tailleTile + tailleTile, fill=self.planete.terrainColor[i][j],
				                              outline="")

		self.afficherUI()

	def afficherUI(self):
		Perspective.afficherUI(self)
		self.cadreShop = None
		self.cadreJoueur = None
		self.cadreSelection = None

		boutonBack = Button(self.cadreetat, text="←", command=self.voirsysteme)
		boutonBack.grid(row=0, column=0)
		# boutonNext=Button(self.cadreetat,text="→",command=self.voirsysteme)
		# boutonNext.grid(row=0,column=5)

		self.boutonShop = Button(self.cadreetat, text="Shop ˃", command=self.afficherShop)
		self.boutonShop.grid(row=2, column=0)

	def afficherShop(self):
		self.boutonShop.config(text="Shop ˅")
		# self.cadreShop=Frame(self.cadreetat,width=200,height=200,bg="blue")
		self.chargeimages()

		if self.cadreShop:
			self.cadreShop.grid_forget()
			self.boutonShop.config(text="Shop ˃")
			self.cadreShop = None
		else:
			self.cadreShop = Frame(self.cadreetat, width=200, height=400, bg="blue")
			self.cadreShop.grid(row=3, column=0, columnspan=5, rowspan=5)
			
			shopVille = Button(self.cadreShop, text="Ville", image=self.images["miniVille"], compound="top", command=self.infoVilleShop)
			shopVille.grid(row=0, column=0)
			shopMine = Button(self.cadreShop, text="Mine", image=self.images["miniMine"], compound="top",  command=self.creermine)
			shopMine.grid(row=0, column=1)
			shopGeneratrice = Button(self.cadreShop, text="Generatrice", image=self.images["miniGen"], compound="top",  command=self.creergeneratrice)
			shopGeneratrice.grid(row=0, column=2)
			shopFerme = Button(self.cadreShop, text="Ferme", image=self.images["miniFerm"], compound="top",  command=self.creeferme)
			shopFerme.grid(row=1, column=0)
			shopBarrack = Button(self.cadreShop, text="Barrack", image=self.images["miniBarra"], compound="top",  command=self.creeBarrack)
			shopBarrack.grid(row=1, column=1)

	def infoShop(self, typeBatiment):
		self.cadreInfoShop =  Frame(self.cadreShop, width=200, height=100, bg="white")
		self.cadreInfoShop.grid(row=3, column=0, columnspan=5, rowspan=5)
		#Infos batiment
		labelImage = Label(self.cadreInfoShop, image=self.images["miniVille"])
		labelNom = Label(self.cadreInfoShop, text="Ville")
		labelLvl = Label(self.cadreInfoShop, text="Lvl. 1")
		#Infos ressources Batiment
		labelInfo1 = Label(self.cadreInfoShop, text="+1/sec Metal")
		labelInfo2 = Label(self.cadreInfoShop, text="+1/sec Food")
		labelInfo3 = Label(self.cadreInfoShop, text="+1/sec Energie")
		#Cout batiment
		labelCout1 = Label(self.cadreInfoShop, text="-20 Metal")
		labelCout2 = Label(self.cadreInfoShop, text="-20 Food")
		labelCout3 = Label(self.cadreInfoShop, text="-20 Energie")
		#Boutons
		boutonAcheter = Button(self.cadreInfoShop, text="Acheter", command=self.creerville)
		
		if typeBatiment is "ville":
			labelImage.config(image=self.images["miniVille"])
			labelNom.config(text="Ville")
			labelInfo1.config(text="")
	
		#grid tout
			#batiment
		labelImage.grid(row=0, column=0, columnspan=2, rowspan=2)
		labelNom.grid(row=2,column=0, columnspan=2, rowspan=2)
		labelLvl.grid(row=3,column=0, columnspan=2, rowspan=2)
			#ressources +
		labelInfo1.grid(row=0, column=3)
		labelInfo2.grid(row=1, column=3)
		labelInfo3.grid(row=2, column=3)
			#ressources -
		labelCout1.grid(row=0, column=4)
		labelCout2.grid(row=1, column=4)
		labelCout3.grid(row=2, column=4)
			#bouton
		boutonAcheter.grid(row=3, column=4)
		
	def infoVilleShop(self):
		self.cadreInfoShop =  Frame(self.cadreShop, width=200, height=100, bg="lightgray")
		self.cadreInfoShop.grid(row=3, column=0, columnspan=5, rowspan=5)
		
		labelImage = Label(self.cadreInfoShop, image=self.images["miniVille"])
		labelImage.grid(row=0, column=0, columnspan=2, rowspan=2)
		labelNom = Label(self.cadreInfoShop, text="Ville")
		labelNom.grid(row=2,column=0)
		labelLvl = Label(self.cadreInfoShop, text="Lvl. 1")
		labelLvl.grid(row=3,column=0)
		
		#Infos Batiment
		labelInfo1 = Label(self.cadreInfoShop, text="+1/sec Metal")
		labelInfo1.grid(row=0, column=3)
		labelInfo1 = Label(self.cadreInfoShop, text="+1/sec Food")
		labelInfo1.grid(row=1, column=3)
		labelInfo1 = Label(self.cadreInfoShop, text="+1/sec Energie")
		labelInfo1.grid(row=2, column=3)
		
		#Cout batiment
		labelCout1 = Label(self.cadreInfoShop, text="-20 Metal")
		labelCout1.grid(row=0, column=4)
		labelCout1 = Label(self.cadreInfoShop, text="-20 Food")
		labelCout1.grid(row=1, column=4)
		labelCout1 = Label(self.cadreInfoShop, text="-20 Energie")
		labelCout1.grid(row=2, column=4)
		
		#Boutons
		boutonAcheter = Button(self.cadreInfoShop, text="Acheter", command=self.creerville)
		boutonAcheter.grid(row=3, column=4)
	
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
		
	def afficherdecor(self):
		pass

	def afficherpartie(self, mod):  # ! -----------------------------------------------------
		# t = 200 / self.largeur  # 200 c'Est la taille du du minimap
		#  p = 200/ self.planete.terrainTailleCarre

		#  self.canevas.delete("infrastructure")

		#   for i in self.planete.infrastructures:
		#      x=i.x
		#      y=i.y

		#      self.minimap.create_oval(x*t - p, y*t - p, x*t + p, y*t + p,  fill = "white",tags=["infrastructure"])
		# ! -----------------------------------------------------------------------
		pass

	def changerproprietaire(self, prop, couleur, systeme):
		pass

	def afficherselection(self):
		pass

	def cliquervue(self, evt):
		
		t = self.canevas.gettags("current")
		if t and t[0] != "current":
			if t[0] == self.parent.nom:
				pass
			elif t[1] == "mine":
				print("mine mine mine") #!!!
				pass
		else:
			x = self.canevas.canvasx(evt.x)
			y = self.canevas.canvasy(evt.y)

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
