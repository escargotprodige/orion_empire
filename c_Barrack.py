from c_Batiment import *
from c_AttaquantTerre import *

from enum import Enum


class ATP(Enum):  # ATTAQUANT_TERRE PARAMETRE
	NOM = 0
	X = 1
	Y = 2
	NEAR_RANGE = 3
	FAR_RANGE = 4
	ATK = 5
	HP = 6
	SPEED = 7
	DEFENSE = 8
	SYSTEMID = 9
	PLANETEID = 10
	PROPRIETAIRE = 11
	TYPE = 12
	PRIX = 13
	LVL = 14


class AT_TYPE(Enum):
	LAZERBOI = 0
	FISTBOI = 1


class Barrack(Batiment):
	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "barrack")
		self.dictUnitTemplate = {AT_TYPE.LAZERBOI: {ATP.NOM: 'lazerBoi',
											   ATP.X: self.x,
											   ATP.Y: self.y,
											   ATP.NEAR_RANGE: 100,
											   ATP.FAR_RANGE: 300,
											   ATP.ATK: 10,
											   ATP.HP: 100,
											   ATP.SPEED: 5,
											   ATP.DEFENSE: 5,
											   ATP.SYSTEMID: self.systemeid,
											   ATP.PLANETEID: self.planeteid,
											   ATP.PROPRIETAIRE: self.proprietaire,
											   ATP.TYPE: AT_TYPE.LAZERBOI,
											   ATP.PRIX: 100,
											   ATP.LVL: 1
											   },
							AT_TYPE.FISTBOI: {ATP.NOM: 'fistBoi',
											  ATP.X: self.x,
											  ATP.Y: self.y,
											  ATP.NEAR_RANGE: 0,
											  ATP.FAR_RANGE: 10,
											  ATP.ATK: 30,
											  ATP.HP: 150,
											  ATP.SPEED: 7,
											  ATP.DEFENSE: 6,
											  ATP.SYSTEMID: self.systemeid,
											  ATP.PLANETEID: self.planeteid,
											  ATP.PROPRIETAIRE: self.proprietaire,
											  ATP.TYPE: AT_TYPE.FISTBOI,
											  ATP.PRIX: 100,
											  ATP.LVL: 1
											  }
							}

	def setBarrackMere(self, barrackMere):
		print(self.dictUnitTemplate.keys())
		b = self.dictUnitTemplate[AT_TYPE.LAZERBOI]
		bm = barrackMere.dictUnitTemplate[AT_TYPE.LAZERBOI]
		
		b[ATP.NEAR_RANGE] = bm[ATP.NEAR_RANGE]
		b[ATP.FAR_RANGE] = bm[ATP.FAR_RANGE]
		b[ATP.ATK] = bm[ATP.ATK]
		b[ATP.HP] = bm[ATP.HP]
		b[ATP.SPEED] = bm[ATP.SPEED]
		b[ATP.DEFENSE] = bm[ATP.DEFENSE]
		b[ATP.PRIX] = bm[ATP.PRIX]
		
		b = self.dictUnitTemplate[AT_TYPE.FISTBOI]
		bm = barrackMere.dictUnitTemplate[AT_TYPE.FISTBOI]
		
		b[ATP.NEAR_RANGE] = bm[ATP.NEAR_RANGE]
		b[ATP.FAR_RANGE] = bm[ATP.FAR_RANGE]
		b[ATP.ATK] = bm[ATP.ATK]
		b[ATP.HP] = bm[ATP.HP]
		b[ATP.SPEED] = bm[ATP.SPEED]
		b[ATP.DEFENSE] = bm[ATP.DEFENSE]
		b[ATP.PRIX] = bm[ATP.PRIX]
    
		#dictUnitTemplate = barrackMere.dictUnitTemplate

	def creerLazerBoi(self, proprietaire = None):
		t = self.dictUnitTemplate[AT_TYPE.LAZERBOI]
		soldat = AttaquantTerre(t[ATP.NOM], t[ATP.X], t[ATP.Y], t[ATP.NEAR_RANGE], t[ATP.FAR_RANGE], t[ATP.ATK],
		                        t[ATP.HP], t[ATP.SPEED], t[ATP.DEFENSE], t[ATP.SYSTEMID], t[ATP.PLANETEID],
		                        proprietaire, t[ATP.TYPE])
		return soldat

	def creerFistBoi(self, proprietaire = None):
		t = self.dictUnitTemplate[AT_TYPE.FISTBOI]
		soldat = AttaquantTerre(t[ATP.NOM], t[ATP.X], t[ATP.Y], t[ATP.NEAR_RANGE], t[ATP.FAR_RANGE], t[ATP.ATK],
		                        t[ATP.HP], t[ATP.SPEED], t[ATP.DEFENSE], t[ATP.SYSTEMID], t[ATP.PLANETEID],
		                        proprietaire, t[ATP.TYPE])
		return soldat
	
	def upgradeLazerBoi(self, scale):
		t = self.dictUnitTemplat[AT_TYPE.LAZERBOI]
		t[ATP.FAR_RANGE] *= scale
		t[ATP.NEAR_RANGE] *= scale
		t[ATP.ATK] *= scale
		t[ATP.HP] *= scale * 2
		t[ATP.SPEED] *= scale / 2
		t[ATP.DEFENSE] *= scale
		t[ATP.NOM] += 'i'
		t[ATP.PRIX] *= scale
		t[ATP.LVL] += 1

	def upgradeFistBoi(self, scale):
		t = self.dictUnitTemplat[AT_TYPE.FISTBOI]
		t[ATP.FAR_RANGE] *= scale
		t[ATP.NEAR_RANGE] *= scale
		t[ATP.ATK] *= scale
		t[ATP.HP] *= scale / 2
		t[ATP.SPEED] *= scale * 2
		t[ATP.DEFENSE] *= scale
		t[ATP.NOM] += 'i'
		t[ATP.PRIX] *= scale
		t[ATP.LVL] += 1
