from IdMaker import *
from mathPlus import *

class AttaquantTerre:
    def __init__(self, nom, x, y, nearRange, farRange, atk, hp, speed, defense, systemid, planeteid, proprietaire, type):
        self.nearRange = nearRange
        self.farRange = farRange
        self.atk = atk
        self.defense = defense
        self.hp = hp
        sel.speed = speed
        self.x = x
        self.y = y
        self.id = ID.Id.prochainid()
        self.systemid = systemid
        self.planeteid = planeteid
        self.proprietaire = proprietaire
        self.nom = nom
        self.type = type
        self.target = None
    
    def setTarget(self):
        pass
    
    def attaquer(self):
        pass
    
    def avancer(self):
        #utilise isinstance
        pass
    
    def upgrade(self):
        pass
    
    def arboderBoat(self, target):
        pass