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


class AT_TYPE(Enum):
	LAZERBOI = 0
	FISTBOI = 1


class Barrack(Batiment):
	dictUnitTemplate = {}

	def __init__(self, parent, proprietaire, systemeid, planeteid, x, y):
		Batiment.__init__(self, parent, proprietaire, systemeid, planeteid, x, y, "barrack")
		dictUnitTemplate = {AT_TYPE.LAZERBOI: {ATP.NOM: 'lazerBoi',
		                                       ATP.X: self.x,
		                                       ATP.Y: self.y,
		                                       ATP.NEAR_RANGE: 10,
		                                       ATP.FAR_RANGE: 100,
		                                       ATP.ATK: 10,
		                                       ATP.HP: 100,
		                                       ATP.SPEED: 5,
		                                       ATP.DEFENSE: 5,
		                                       ATP.SYSTEMID: self.systemeid,
		                                       ATP.PLANETEID: self.planeteid,
		                                       ATP.PROPRIETAIRE: self.proprietaire,
		                                       ATP.TYPE: AT_TYPE.LAZERBOI
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
		                                      ATP.TYPE: AT_TYPE.FISTBOI
		                                      }
		                    }

	def creerLazerBoi(self):
		t = self.dictUnitTemplat[AT_TYPE.LAZERBOI]
		soldat = AttaquantTerre(t[ATP.NOM], t[ATP.X], t[ATP.Y], T[ATP.NEAR_RANGE], t[ATP.FAR_RANGE], t[ATP.ATK],
		                        t[ATP.HP], t[ATP.SPEED], t[ATP.DEFENSE], t[ATP.SYSTEMID], t[ATP.PLANETEID],
		                        t[ATP.PROPRIETAIRE], t[ATP.TYPE])

	def creerFistBoi(self):
		t = self.dictUnitTemplat[AT_TYPE.FISTBOI]
		soldat = AttaquantTerre(t[ATP.NOM], t[ATP.X], t[ATP.Y], T[ATP.NEAR_RANGE], t[ATP.FAR_RANGE], t[ATP.ATK],
		                        t[ATP.HP], t[ATP.SPEED], t[ATP.DEFENSE], t[ATP.SYSTEMID], t[ATP.PLANETEID],
		                        t[ATP.PROPRIETAIRE], t[ATP.TYPE])
