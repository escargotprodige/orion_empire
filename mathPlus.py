import math


# retourne un tuple de taille 2 avec un point representant
# la distance entre deux point
def distancePoint(x, y, x2, y2):
	x = x - x2
	y = y - y2
	return (x, y)


# applique la formule pythagoras
def pythagore(x, y):
	return math.sqrt(x * x + y * y)


# normalize un point x,y entre 0 et 1
def normalize(x, y):
	if pythagore(x, y) != 0:
		x2 = x / pythagore(x, y)
		y2 = y / pythagore(x, y)
	else:
		x2 = 0
		y2 = 0
	return (x2, y2)


# retourne lunite minimal(entre 0 et 1) en direction x2, y2
def directionVers(x, y, x2, y2):
	point = distancePoint(x2, y2, x, y)
	x3 = point[0]
	y3 = point[1]
	return normalize(x3, y3)


# retourne la longeur entre deux points
def distance(x, y, x2, y2):
	point = distancePoint(x, y, x2, y2)
	x3 = point[0]
	y3 = point[1]
	return pythagore(x3, y3)
