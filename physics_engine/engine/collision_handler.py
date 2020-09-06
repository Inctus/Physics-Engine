# >> CREDITS << # >> CREDITS << 
# Collision_Handler.py written by Haashim Hussain

# >> DESCRIPTION <<
# This module will handle Separating Axis Theorem collisions.
# It attempts to do so in a very efficient way to minimise frame loss.

# >> MODULES <<
import math

from classes.vector2d import Vector2

def getNormalsFromVertices(vertices):
	points = len(vertices) # Amount of vertices to make processing efficient
	edges = [(vertices[(i+1)%numVertices] - vertices[i]) for i in range(points)] # Edges are differences between vertices
	normals = [edge.perpendicular_normal() for edge in edges] # Perpendicular normals found
	return normals # Return normals in case we need them. Remove duplicates for efficiency later

def projectVerticesOntoNormal(vertices, normal):
	return [(normal.dot(vertex), vertex) for vertex in vertices] # Keep a link between vertices and their projection
	# So that I can find the deepest vertex easily.

def getMaxAndMinVertices(projections): # Projections has list of tuples [ (float projection, Vec2 vertex) ]
	maxs, mins = [] # Make an array for max and min values. Reminder we could have multiple in which case average each vertex.
	extractProjection = lambda x: x[0] # We want the projection not the vertex
	maxProjection = max(projections, key=extractProjection)[0] # We find the maximum projection value
	minProjection = min(projections, key=extractProjection)[0] # And the minimum projection value
	for projection in projections:
		if projection[0] == maxProjection: # A maximum has been found.
			maxs.append(projection)
		if projection[0] == minProjection:
			mins.append(projection)
	return maxs, mins # Returns max and min dot products and the vertices assosciated with said projections.

def isSeparatingAxis(normal, verticesOne, verticesTwo):
	oneMax, oneMin = getMaxAndMinVertices( projectVerticesOntoNormal(verticesOne, normal) ) # [ (projection, vertex), (projection, vertex) ]
	twoMax, twoMin = getMaxAndMinVertices( projectVerticesOntoNormal(verticesTwo, normal) )
	if (twoMin[0][0] > oneMax[0][0]) or (oneMin[0][0] > twoMax[0][0]): # If there is no collision along this axis
		return False, 0, Vector2(), Vector2() # Return no collision, empty MTV and empty coordinate of collision
	if oneMax[0][0] > twoMax[0][0]: # We know there is collision, now filter to see which shape is dominant
		depth = twoMax[0][0]-oneMin[0][0]
		amountOfMinima = len(oneMin)
		vertex = oneMin[0][1] # Vectors of collision will be stored in oneMin I choose oneMin where shapeOne is dominant
		if amountOfMinima > 1:
			vertex = sum([projection[1] for projection in oneMin])/amountOfMinima # Average position of vertices of collision (middle of edge)
		return True, depth, normal, vertex
	else:
		depth = oneMax[0][0]-twoMin[0][0]
		amountOfMinima = len(twoMin)
		vertex = twoMin[0][1] # Vectors of collision will be stored in twoMin I choose twoMin where shapeTwo is dominant
		if amountOfMinima > 1:
			vertex = sum([projection[1] for projection in twoMin])/amountOfMinima
		return True, depth, normal, vertex

def areShapesColliding(shapeOne, shapeTwo):
	verticesOne, verticesTwo = shapeOne.Vertices, shapeTwo.Vertices
	normals = set(getNormalsFromVertices(verticesOne)+getNormalsFromVertices(verticesTwo)) # Combine normals and make set
	relativeVelocity = shapeTwo.Velocity - shapeOne.Velocity # How shapeOne is moving relative to shapeTwo
	mtvs = [] # minimal translation vectors: List of tuples [ (depth, tv, vertex) ]
	for normal in normals:
		velocityAlongNormal = normal.dot(relativeVelocity)
		if velocityAlongNormal > 0: # If the shapes are already separating themselves
			continue # Skip to next iteration
		collision, depth, mtv, vertex = isSeparatingAxis(normals, shapeOne.Vertices, shapeTwo.Vertices)
		if not collision:
			return collision, mtv, vertex # Return empty stuff
		mtvs.append((depth, mtv, vertex))
	mtv = sorted(mtvs, key=lambda x: x[0]) # Sort by depth (lowest to highest)
	return True, mtv[1]*mtv[0], mtv[2] # Return collision, translation normal * depth, and vertex of collision






''' OLD COLLISIONS WERE GLITCHY SO REDOING THEM FROM THE GROUND UP.

def getNormals(vertices):
	numVertices = len(vertices)
	return [(vertices[(i+1)%numVertices] - vertices[i]).perpendicular_normal() for i in range(numVertices)]

def projected(normal, vertices):
	return [normal.dot(vertex) for vertex in vertices]

def minMaxProjections(normal, vertices):
	project = projected(normal, vertices)
	return max(project), min(project), project

def collided(normal, shapeOne, shapeTwo):
	maxOne, minOne, p1 = minMaxProjections(normal, shapeOne) 
	maxTwo, minTwo, p2 = minMaxProjections(normal, shapeTwo)
	if (minTwo > maxOne) or (maxTwo < minOne):
		return False, Vector2()
	return True, normal * ((maxOne-minTwo) if maxOne>maxTwo else (maxTwo-minOne))

def checkCollision(shapeOne, shapeTwo, centerOne, centerTwo):
	normals = set(getNormals(shapeOne) + getNormals(shapeTwo))
	centerDifference = centerOne-centerTwo
	deltaProjection = lambda y: (centerDifference).projection(y)
	multiplier = lambda x: -x + deltaProjection(x)*2 if ((centerDifference).dot(x) > 0) else x - deltaProjection(x)*2
	mtvs = []
	for normal in normals:
		hasCollided, mtv = collided(normal, shapeOne, shapeTwo)
		if not hasCollided:
			return hasCollided, mtv, Vector2() # Return false because there's a gap and no collision.
		else:
			mtvs.append(multiplier(mtv))
	mtvs.sort(key=lambda x: x.length)
	return True, mtvs[0], centerOne + centerDifference/2 # Return minimum translation vector and trueee

def broadScaleCollisions(shapes):
	projections = []
	possibilities = []
	for shape in shapes:
		ys = [vertex.y for vertex in shape] # Use y axis to detect collisions because gravity means most things are *falling down*
		projections.append((min(ys), max(ys))) # So it makes sense to check y axis for collisions, to avoid unnecessary ones.
	projections.sort(key=lambda x: x[0])
	for i in range(len(projections)):
		bottomOfLower = projections[i][1]
		for j in range(i+1, len(projections)):
			if bottomOfLower >= projections[j][0]:
				possibilities.append((i, j))
	return possibilities

def filterCollisions(shapes, possibilities, centers):
	confirmed = []
	for possibility in possibilities:
		shapeOne, shapeTwo = possibility
		result, mtv, vertex = checkCollision(shapes[shapeOne], shapes[shapeTwo], centers[shapeOne], centers[shapeTwo])
		if result:
			confirmed.append((shapeOne, shapeTwo, mtv, vertex))
	return confirmed

def checkCollisions(shapes, centers):
	possibilities = broadScaleCollisions(shapes)
	if possibilities:
		print(len(possibilities))
	filtered = filterCollisions(shapes, possibilities, centers) 
	return filtered
'''