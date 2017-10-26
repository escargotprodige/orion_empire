from orion_empire_modele import *

class Joueur():
    def __init__(self,parent,nom,systemeorigine,couleur):
        self.parent=parent
        self.id= Id.prochainid()
        #self.id=parent.createurId.prochainid()
        self.artificiel=0   # IA
        self.nom=nom
        self.systemeorigine=systemeorigine
        self.couleur=couleur
        self.systemesvisites=[systemeorigine]
        self.vaisseauxinterstellaires=[]
        self.vaisseauxinterplanetaires=[]
        self.actions={"creervaisseauGalactique":self.creervaisseauGalactique,
                      "ciblerdestination":self.ciblerdestination,
                      "atterrirplanete":self.atterrirplanete,
                      "visitersysteme":self.visitersysteme,
                      "creermine":self.creermine,
                      "creerville":self.creerville,
                      "creergeneratrice":self.creergeneratrice,
                      "creerferme":self.creerferme,
                      "dechargervausseaugalactique":self.dechargervaisseaugalactique, #! MODIF ICI
                      }
        
        
        self.planeteOrigine=random.choice(self.systemeorigine.planetes)
        self.planeteOrigine.proprietaire=self.nom
        #self.creerVilleOrigine()
        
        
        self.ressourcesTEMP=100
        
         
        self.ressource1=100
        self.ressource2=100
        self.ressource3=100
        
    def creerVilleOrigine(self):
        ville=Ville(self,self.nom,self.systemeorigine,self.planeteOrigine, 25, 25) ### TEST ICI  ###
        self.planeteOrigine.infrastructures.append(ville)
        
        #Choisir X Y pour ville
        #coords[]
        
        self.parent.parent.afficherBatiment(ville)  ### TEST ICI  ###
        
        #return coords
        
    def creermine(self,listeparams):
        nom,systemeid,planeteid,x,y=listeparams
        for i in self.systemesvisites:
            if i.id==systemeid:
                for j in i.planetes:
                    if j.id==planeteid:
                        mine=Mine(self,nom,systemeid,planeteid,x,y)
                        j.infrastructures.append(mine)
                        #self.parent.parent.affichermine(nom,systemeid,planeteid,x,y)
                        self.parent.parent.afficherBatiment(mine)
     
    def creerville(self,listeparams):
        nom,systemeid,planeteid,x,y=listeparams
        for i in self.systemesvisites:
            if i.id==systemeid:
                for j in i.planetes:
                    if j.id==planeteid:
                        ville=Ville(self,nom,systemeid,planeteid,x,y)
                        j.infrastructures.append(ville)
                        #self.parent.parent.afficherville(nom,systemeid,planeteid,x,y)
                        self.parent.parent.afficherBatiment(ville)
                        
                        
    def creerferme(self,listeparams):
        nom,systemeid,planeteid,x,y=listeparams
        for i in self.systemesvisites:
            if i.id==systemeid:
                for j in i.planetes:
                    if j.id==planeteid:
                        ferme=Ferme(self,nom,systemeid,planeteid,x,y)
                        j.infrastructures.append(ferme)
                        #self.parent.parent.afficherferme(nom,systemeid,planeteid,x,y)
                        self.parent.parent.afficherBatiment(ferme)
    
    def creergeneratrice(self,listeparams):
        nom,systemeid,planeteid,x,y=listeparams
        for i in self.systemesvisites:
            if i.id==systemeid:
                for j in i.planetes:
                    if j.id==planeteid:
                        generatrice=Generatrice(self,nom,systemeid,planeteid,x,y)
                        j.infrastructures.append(generatrice)
                        #self.parent.parent.afficherferme(nom,systemeid,planeteid,x,y)
                        self.parent.parent.afficherBatiment(generatrice)                    
    
    """ Version avant    
    def creermine(self,listeparams):
        nom,systemeid,planeteid,x,y=listeparams
        for i in self.systemesvisites:
            if i.id==systemeid:
                for j in i.planetes:
                    if j.id==planeteid:
                        mine=Mine(self,nom,systemeid,planeteid,x,y)
                        j.infrastructures.append(mine)
                        self.parent.parent.affichermine(nom,systemeid,planeteid,x,y)
                             
    def creerville(self,listeparams):
        nom,systemeid,planeteid,x,y=listeparams
        for i in self.systemesvisites:
            if i.id==systemeid:
                for j in i.planetes:
                    if j.id==planeteid:
                        ville=Ville(self,nom,systemeid,planeteid)
                        j.infrastructures.append(ville)
                        self.parent.parent.afficherville(nom,systemeid,planeteid,x,y)
                        
                        
    def creergeneratrice(self,listeparams):
        nom,systemeid,planeteid,x,y=listeparams
        for i in self.systemesvisites:
            if i.id==systemeid:
                for j in i.planetes:
                    if j.id==planeteid:
                        ferme=Ferme(self,nom,systemeid,planeteid,x,y)
                        j.infrastructures.append(ferme)
                        self.parent.parent.afficherferme(nom,systemeid,planeteid,x,y)
    
    def creerferme(self,listeparams):
        nom,systemeid,planeteid,x,y=listeparams
        for i in self.systemesvisites:
            if i.id==systemeid:
                for j in i.planetes:
                    if j.id==planeteid:
                        generatrice=Generatrice(self,nom,systemeid,planeteid,x,y)
                        j.infrastructures.append(generatrice)
                        self.parent.parent.afficherferme(nom,systemeid,planeteid,x,y) """
                        
    def atterrirplanete(self,d):
        nom,systeid,planeid=d
        for i in self.systemesvisites:
            if i.id==systeid:
                for j in i.planetes:
                    if j.id==planeid:
                        i.planetesvisites.append(j)
                        if nom==self.parent.parent.monnom:
                            self.parent.parent.voirplanete(i.id,j.id)
                        return 1
        
    def visitersysteme(self,systeme_id):
        for i in self.parent.systemes:
            if i.id==systeme_id:
                self.systemesvisites.append(i)
                
    def creervaisseauGalactique(self,id):
        for i in self.systemesvisites:
            if i.id==id:
                v=VaisseauGalactique(self,self.nom,i)
                self.vaisseauxinterstellaires.append(v)
                return 1
        
    def ciblerdestination(self,ids):
        idori,iddesti=ids
        for i in self.vaisseauxinterstellaires:
            if i.id== idori:
                for j in self.parent.systemes:
                    if j.id== iddesti:
                        #i.cible=j
                        i.ciblerdestination(j)
                        return
                for j in self.systemesvisites:
                    if j.id== iddesti:
                        #i.cible=j
                        i.ciblerdestination(j)
                        return
                for j in self.parent.pulsars:
                    if j.id==iddesti:
                        i.ciblerdestination(j)
                        return
        
    def prochaineaction(self): # NOTE : cette fonction sera au coeur de votre developpement
        for i in self.vaisseauxinterstellaires:
            if i.cible:
                rep=i.avancer()
                if rep: 
                    if rep in self.parent.systemes: # ------------------------ verifie si la cible est un systeme
                        #! ------------------------------------------------ DÉBUT MODIF
                        if rep not in self.systemesvisites:
                            self.systemesvisites.append(rep)
                            if self.nom == self.parent.parent.monnom:
                                self.parent.changeetatsystem(self.nom,rep) 
                        #! ------------------------------------------------- FIN MODIF
                    elif rep in self.parent.pulsars: # ---------------------------- verifie si la cible est une pulsar
                        # ----------------------------------------Teleporte vaisseau vers autre pulsar au hazard
                        teleport=random.choice(self.parent.pulsars)
                        while teleport==rep:
                            teleport=random.choice(self.parent.pulsars)
                        i.x=teleport.x
                        i.y=teleport.y
                        print(i.id," >> TELEPORTE VERS PULSAR ",teleport)
                        """if rep.proprietaire=="inconnu":
                        if rep not in self.systemesvisites:
                            self.systemesvisites.append(rep)
                            self.parent.changerproprietaire(self.nom,self.couleur,rep)"""
                        #! ------------------------------------------------------------------ DEBUT MODIF
                        if self.nom == self.parent.parent.monnom:
                            if self.parent.parent.vue.modecourant == self.parent.parent.vue.modes["galaxie"]:   
                                self.parent.parent.vue.deplacerCanevas(i.x,i.y)
                        #! ------------------------------------------------------------------- FIN MODIF
                        
    #! ------------------------------------------------------------ DEBUT MODIF  
    def dechargervaisseaugalactique(self,rep):
        v = None
        s= None
        for i in self.vaisseauxinterstellaires:
                if i.id == rep[0]:
                    v=i
                    break
        for i in self.parent.systemes:
            if i.id == rep[1]:
                s = i
                break
        
        if s and v:
            v.dechargervaisseaugalactique(s)    
    #! ------------------------------------------------------------- FIN MODIF
    
    def dechargervaisseaugalactique(self,rep):
        v = None
        s= None
        for i in self.vaisseauxinterstellaires:
                if i.id == rep[0]:
                    v=i
                    break
        for i in self.parent.systemes:
            if i.id == rep[1]:
                s = i
                break
        
        if s and v:
            v.dechargervaisseaugalactique(s)
            
    def upgradeVitesseVaisseau(self,rep):
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
    #! DEBUT MODIF     
    def chargementdansvaisseaugalactique(self,rep):
        vg = rep[0]
        vs = rep[1]
        
        print("CHARGEMENT VAISSEAU",vs,"DANS",vg)
        
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
    #! FIN MODIF
