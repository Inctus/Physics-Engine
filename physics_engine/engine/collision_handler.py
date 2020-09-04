# >> CREDITS << 
# Collision_Handler.py written by Haashim Hussain

# >> DESCRIPTION <<
# This module will handle Separating Axis Theorem collisions.
# It attempts to do so in a very efficient way to minimise frame loss.

# >> MODULES <<
import math

from classes.vector2d import Vector2

#from classes.vector2d import Vector2

def getNormals(vertices):
	numVertices = len(vertices)
	return [(vertices[(i+1)%numVertices] - vertices[i]).normalized * Vector2(-1,0) for i in range(numVertices)]

def isSeparatingAxis(normal, shapeOne, shapeTwo):
	shapeOneProjected, shapeTwoProjected = [normal.dot(vertex) for vertex in shapeOne], [normal.dot(vertex) for vertex in shapeTwo]
	maxOne, minOne, maxTwo, minTwo = max(shapeOneProjected), min(shapeOneProjected), max(shapeTwoProjected), min(shapeTwoProjected)
	if (minTwo > maxOne) or (maxTwo < minOne):
		return False, Vector2()
	return True, normal * ((maxOne-minTwo) if maxOne>maxTwo else (maxTwo-minOne))

def CheckCollision(shapeOne, shapeTwo):
	normals = set(getNormals(shapeOne) + getNormals(shapeTwo))
	mtvs = []
	for normal in normals:
		collided, mtv, normalNumber = isSeparatingAxis(normal, shapeOne, shapeTwo)
		if not collided:
			return collided, mtv, axis # Return false because there's a gap and no collision.
		else:
			mtvs.append(mtv)
	return True, mtvs.sort(key=x: x.length)[0] # Return minimum translation vector and trueee