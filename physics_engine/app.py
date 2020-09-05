# >> CREDITS << 
# Main.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES <<
from pygame import init, display, time, event, quit
from pygame import Color as Colour # UK > US
from pygame import QUIT # ENUMS

from math import pi

from engine.engine_model import createModel,render,createRigidBody,createRigidBodyFromVertices
from engine.collision_handler import checkCollision
from classes.uihelper import Interface,UIBase
from classes.vector2d import Vector2
from classes.udim2 import UDim2

# >> FUNCTIONS <<

def run():
	# Engine initialisation
	engine = createModel() # Engine.Workspace, Engine.UserInterface
	engine.Colour = Colour(50,50,50)

	# PyGame Initialisation >> stays in this module
	init()
	surface = display.set_mode((engine.AbsoluteSize.x, engine.AbsoluteSize.y))
	display.set_caption("Phsics Engine - Haashim Hussain")
	clock = time.Clock()

	# Object Creation >> moved out of this module
	body = createRigidBody(8, 100)
	body.Name = "RigidSquare"
	body.Parent = engine.Workspace
	body.Colour = Colour(30,30,30)
	body.Position = Vector2(400, 225)
	body.Mass = 50

	boundary = createRigidBodyFromVertices(Vector2(-400, 1), Vector2(400, 1), Vector2(400, 0), Vector2(-400, 0))
	boundary.Anchored = True
	boundary.Name = "BottomBoundary"
	boundary.Colour = Colour(255,0,0)
	boundary.Position = Vector2(400, engine.Workspace.AbsoluteSize.y-1)
	boundary.Parent = engine.Workspace

	interfaceBar = UIBase("Rectangle")
	interfaceBar.Name = "Border"
	interfaceBar.Size = UDim2(1,0,0.05,0)
	interfaceBar.Colour = Colour(30,30,30)
	interfaceBar.Parent = engine.UserInterface

	clone = interfaceBar.Clone()
	clone.Position = UDim2(0, 0, 0.95, 0)
	clone.Parent = engine.UserInterface

	image = Interface("ImageLabel")
	image.Name = "PlayButton"
	image.Image = "resources/Play.png"
	image.Size = UDim2(0.2,0,0.8,0)
	image.Position = UDim2(0.4,0,0.1,0)
	image.Parent = engine.UserInterface
	image.ConstrainAxes = True
	image.ImageColour = Colour(30,30,30)
	image.DominantAxis = "y"

	print(engine.Tree)

	while True:
		for eventInstance in event.get():
			if eventInstance.type == QUIT:
				return
		body.Update(1/30)
		render(engine, surface)
		display.update(engine.Workspace.Rectangle) # Use update RECT to specify WORKSPACE to render WORKSPACE for EFFICIENCY
		clock.tick(30)

run()
