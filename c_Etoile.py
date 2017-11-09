from orion_empire_modele import *


class Etoile():
	def __init__(self, parent, x, y):
		self.parent = parent
		self.id = Id.prochainid()
		self.type = random.choice(["red", "red", "red",
								   "white", "white",
								   "yellow", "yellow", "yellow",
								   "DodgerBlue"])
		outline = {"white": "gray40",
				   "red": "DarkRed",
				   "yellow": "DarkGoldenrod4",
				   "DodgerBlue": "midnight blue",}
		self.outline = outline[self.type]
		self.taille = random.randrange(25) / 10 + 0.1  # en masse solaire
