from orion_empire_modele import *

#  DEBUT IA
class IA(Joueur):
	def __init__(self,parent,nom,systemeorigine,couleur):
		Joueur.__init__(self,parent,nom,systemeorigine,couleur)
		self.contexte="galaxie"
		self.delaiaction=random.randrange(5,10)*20  # le delai est calcule pour chaque prochaine action en seconde
		#self.derniereaction=time.time()
		
	# NOTE sur l'analyse de la situation   
	#		  on utilise le temps (time.time() retourne le nombre de secondes depuis 1970) pour le delai de 'cool down'
	#		  la decision dependra du contexte (modes de la vue)
	#		  aussi presentement - on s'occupe uniquement d'avoir un vaisseau et de deplacer ce vaisseau vers 
	#		  le systeme le plus proche non prealablement visite.
	def analysesituation(self):
		#t=time.time()
		if self.delaiaction==0:
			if self.contexte=="galaxie":
				if len(self.vaisseauxinterstellaires)==0:
					c=self.parent.parent.cadre+5
					if c not in self.parent.actionsafaire.keys(): 
						self.parent.actionsafaire[c]=[] 
					self.parent.actionsafaire[c].append([self.nom,"creervaisseauGalactique",self.systemeorigine.id])
					print("AJOUTER VAISSEAU ",self.systemeorigine.x,self.systemeorigine.y)
				else:
					for i in self.vaisseauxinterstellaires:
						sanscible=[]
						if i.cible==None:
							sanscible.append(i)
						if sanscible:
							vi=random.choice(sanscible)
							systtemp=None
							systdist=1000000000000
							for j in self.parent.systemes:
								d=hlp.calcDistance(vi.x,vi.y,j.x,j.y)
								print ("DISTANCE ",i,d)
								if d<systdist and j not in self.systemesvisites:
									systdist=d
									systtemp=j
							if systtemp:
								vi.ciblerdestination(systtemp)
								print("CIBLER ",systtemp,systtemp.x,systtemp.y)
							else:
								print("JE NE TROUVE PLUS DE CIBLE")
								
				self.delaiaction=random.randrange(5,10)*20
		else:
			self.delaiaction-=1
				#print("CIV:" ,self.nom,self.couleur, self.delaiaction)
		
# FIN IA
