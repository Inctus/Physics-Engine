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
from shared.settings import screenSize 

# >> FUNCTIONS <<
def CreateModel():
	game = UIBase("EngineModel") # This is the parent of all things within the engine
	game.Name = "PhysicsEngine"
	workspace = UIBase("Workspace")
	workspace.Name = "Workspace"
	workspace.Parent = game
	userInterface = UIBase("UserInterface")
	userInterface.Name = "UserInterface"
	userInterface.Parent = game
	return game # Constructed tree structure

# def RenderChildren(object):

# def CreateRigidBody(nSides):

# def CreateRigidBodyFromVertices(vertices):