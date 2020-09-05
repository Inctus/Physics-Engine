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
	return [(vertices[(i+1)%numVertices] - vertices[i]).perpendicular_normal() for i in range(numVertices)]

def collided(normal, shapeOne, shapeTwo):
	shapeOneProjected, shapeTwoProjected = [normal.dot(vertex) for vertex in shapeOne], [normal.dot(vertex) for vertex in shapeTwo]
	maxOne, minOne, maxTwo, minTwo = max(shapeOneProjected), min(shapeOneProjected), max(shapeTwoProjected), min(shapeTwoProjected)
	if (minTwo > maxOne) or (maxTwo < minOne):
		return False, Vector2()
	return True, normal * ((maxOne-minTwo) if maxOne>maxTwo else (maxTwo-minOne))

def checkCollision(shapeOne, shapeTwo):
	normals = set(getNormals(shapeOne) + getNormals(shapeTwo))
	mtvs = []
	for normal in normals:
		hasCollided, mtv = collided(normal, shapeOne, shapeTwo)
		if not hasCollided:
			return hasCollided, mtv # Return false because there's a gap and no collision.
		else:
			mtvs.append(mtv)
	mtvs.sort(key=lambda x: x.length)
	return True, mtvs[0] # Return minimum translation vector and trueee

# BROAD PHASE COLLISION HERE; RETURNS LIST OF POSSIBLE COLLISIONS

# COLLISION FILTERING HERE; TAKES LIST OF POSSIBLE COLLISIONS AND RETURNS ACTUAL COLLISIONS

# MAIN FUNCTION DOES BROAD PHASE AND NARROW PHASE COLLISION USING SAT AND RETURNS ALL COLLISIONS WITH MTVS

# RESOLUTION WILL BE HANDLED INTERNALLY VIA THE RIGIDBODY CLASS