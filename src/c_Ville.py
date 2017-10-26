from c_Batiment import *

class Ville(Batiment):
    def __init__(self,parent,proprietaire,systemeid,planeteid,x,y):
        Batiment.__init__(self,parent,proprietaire,systemeid,planeteid,x,y,"ville")
        
    def generer(self):
        pass