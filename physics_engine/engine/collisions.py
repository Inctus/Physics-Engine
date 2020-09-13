# >> CREDITS << # >> CREDITS << 
# Collisions.py written by Haashim Hussain

# >> DESCRIPTION <<
# This module will handle Separating Axis Theorem collisions.
# It attempts to do so in a very efficient way to minimise frame loss.
# It uses clipping to determine vertices/polygons of collision.
# It builds upon my previous implementation of SAT.

# >> MODULES <<
import math

from classes.vector2d import Vector2
from shared.settings import elasticity # Used to compute impulse vector

# >> PSEUDOCODE <<
'''
ShapeA, ShapeB

relativePosition = ShapeB-ShapeA
relativeVelocity = shapea.vel - shapeb.vel

All Normals will point in the direction A-B (by doing dot of vector) 
simplifies our logic since we will only need to check if min(b) > max(a) for each normal
since dot is commutative and normal is a unit vector the projection is obtained from all possible combinations of each
Normal = Normal if (Normal.dot(relativePosition)>=0) else Normal*-1

for each normal in the shapes, 
	make sure its in the right direction using above algorithm
	if the relativeVelocity.dot(normal) is positive then its in same direction as normal then check for collision
	// if they are already moving away from each other then ignore the possible collision because it will resolve itself.
	then project a and b onto it and keep reference from projection to the vertex's index
	// since normals always from a-b 
	if max(a) > min(b) collision // NO OTHER CASES
	else there no collision // RETURN OFC
	append depth as max(a)-min(b) and mtv normal as normal and vertex index from each shape
	(mtvnormal, vertexa, vertexb) // vertices are indices

after mtv normal and depth are obtained, get contact manifold by:

	for vertex in vertexa, vertexb do
		vertex, vertex.next, vertex.prev
		edge1 = vertex - vertex.next
		edge2 = vertex - vertex.prev
		get projections of edges along mtv normal, and if negative ignore
		if both are positive then grab smaller one and treat as the edge of collision
		append (edge, mtvprojection) to edges
	
	now that you have both edges, calculate the incident edge, and reference edge.
		reference edge is most perpendicular or most wonky edge to the separation normal
		incident edge is most parallel edge to the separation normal.
		therefore reference edge has a smaller dot product with the separation normal.
		we already calculated the mtvprojection for the edge earlier so just check which has a smaller absolute value
		if abs(edge1) > abs(edge2)
			ref = edge1
			inc = edg2
		else
			ref = edge2
			inc = edge1
			// set a flag so that we know the axes have been flipped
	
	now that we have the reference, incident and a flag do
		incident edge, clip by reference edge's first vector 
		incident edge, clip by reference edge's second vector
		if flag then
			reference normal is flipped
		max is reference normal dot reference vector (either will return same value)
		for point in incident edge,
			if projection of point onto reference normal is bigger than the
			max then
				discard the point
			else
				keep the point as (point, depth)

	return points as [(point, depth)] and mtv

	finally return the incident edge points that remain as the contact manifold. 
	if there are two, i will average their positions and apply a force there.
'''

# >> UTILITY FUNCTIONS <<

def getNormalsFromVertices(vertexList):
	n = len(vertexList)
	return [(vertexList[(i+1)%n] - vertexList[i]).perpendicular_normal() for i in range(n)] # Returns normals for each edge.

def projectVerticesOntoNormal(vertexList, normal, sortFunction=False):
	if sortFunction:
		return sortFunction([(i, normal.dot(vertex)) for i,vertex in enumerate(vertexList)], key=lambda x: x[1]) # Returns (index, projection, vertex) for each vertex.
	else:
		return [(i, normal.dot(vertex)) for i,vertex in enumerate(vertexList)]

def isSeparatingAxis(normal, verticesA, verticesB):
	maxA = projectVerticesOntoNormal(verticesA, normal, max)
	minB = projectVerticesOntoNormal(verticesB, normal, min)
	if maxA[1] <= minB[1]:
		return False, Vector2(), 0, 0, 0
	return True, normal, maxA[1]-minB[1], maxA[0], minB[0]


