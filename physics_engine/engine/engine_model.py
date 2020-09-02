# >> CREDITS << 
# engine_model.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This module uses the uihelper classes to create an essential engine model.
# It also implements a recurisve rendering function.
# It simplifies the process of adding objects, such as UI elements, to the engine.
# It is the first module to be ran within engine, followed by ui_model.

# >> MODULES <<
from classes.vector2d import Vector2
from classes.udim2 import UDim2
from classes.uihelper import UIBase, RigidBody, Interface
from shared.settings import screenSize, polygonNames

from pygame import draw
from math import pi,sin,cos,floor

# >> UTILITY FUNCTIONS <<

def findPointsOnUnitCircle(n): # Generates regular polygon from n points.
	interiorAngle = pi*(1-2/n) # Internal angles
	exteriorAngle = 2*pi/n # Leaving it like this for legibility. Could factor out 2/n and reuse above.
	offset = (n+1)%2 * (interiorAngle/2) # All odd numbers need no offset
	vertices = []
	for i in range(0,n):# range(offset, 2pi-exteriorAngle+offset, exteriorAngle): Would've used this but floating point errors :/
		angle = offset + i*exteriorAngle
		vertices.append(Vector2(sin(angle), cos(angle))) # Could condense this into a list comprehension but want to keep it legibile
	return vertices

# >> FUNCTIONS <<
def createModel():
	game = UIBase("EngineModel") # This is the parent of all things within the engine
	game.Name = "PhysicsEngine"
	game.Size = UDim2(0, screenSize[0], 0, screenSize[1])
	workspace = UIBase("Workspace")
	workspace.Name = "Workspace"
	workspace.Parent = game
	userInterface = UIBase("UserInterface")
	userInterface.Name = "UserInterface"
	userInterface.Parent = game
	return game # Constructed tree structure

def render(object, display): # Recursively calls itself to render all object and object's descendants
	if object.ClassName == "EngineModel": # EngineModel sets game background of course.
		display.fill(object.Colour)
	if object.Visible:
		renderAfter = []
		for child in object.GetChildren(): # If they are a higher ZIndex, render them before the parent
			if child.ZIndex > object.ZIndex:
				Render(child, display) # Pass in display again
			else:
				renderAfter.append(child) # If they are lower than ZIndex of parent, render them after
		if object.ClassName == "Polygon": # All rendered classes done!
			draw.polygon(
				display,
				object.Colour,
				object.Vertices
			)
		elif object.ClassName == "Rectangle":
			draw.rect(
				display,
				object.Colour,
				object.Rectangle
			)
		elif object.ClassName == "Ellipse":
			draw.rect(
				display,
				object.Colour,
				object.Rectangle
			)
		elif object.ClassName == "ImageLabel" or object.ClassName == "ImageButton":
			object.Draw(display) # Custom render function for these objects
		(Render(child, display) for child in renderAfter)

# >> RIGID BODY HELPERS <<  (to speed up rigidbody creation and centralise them)

def createRigidBody(n, size):
	body = RigidBody()
	empty = [body.AddVertex(size/2 * vertex) for vertex in findPointsOnUnitCircle(n)]# Scale up vectors
	body.Name = polygonNames[n]
	return body

def createRigidBodyFromVertices(vertices):
	body = RigidBody()
	[body.AddVertex(vertex) for vertex in vertices]
	return body