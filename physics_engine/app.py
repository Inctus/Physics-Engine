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

from engine.engine_model import createModel,render,createRigidBody,createRigidBodyFromVertices,updatePhysics
from engine.collision_handler import checkCollisions
from classes.interface import Interface
from classes.uibase import UIBase
from classes.vector2d import Vector2
from classes.udim2 import UDim2

from shared.settings import framerate

# >> FUNCTIONS <<

def run():
	# Engine initialisation
	engine = createModel() # Engine.Workspace, Engine.UserInterface
	engine.Colour = Colour(50,50,50)

	# PyGame Initialisation >> stays in this module
	init()
	surface = display.set_mode((engine.AbsoluteSize.x, engine.AbsoluteSize.y))
	display.set_caption("Physics Engine - Haashim Hussain")
	clock = time.Clock()

	# Object Creation >> moved out of this module
	body = createRigidBody(5, 100)
	body.Rotation = pi/2
	body.Name = "BodyOne"
	body.Colour = Colour(150,30,30)
	body.Position = Vector2(600, 225)
	body.AddImpulse(Vector2(0, -500))
	body.Mass = 100
	body.Parent = engine.Workspace

	bodyTwo = body.Clone()
	bodyTwo.Name = "BodyTwo"
	bodyTwo.Position = Vector2(140, 150)
	bodyTwo.Colour = Colour(200,100,100)
	bodyTwo._Impulses = []
	bodyTwo.Mass = 500
	bodyTwo.AddImpulse(Vector2(500,-300))
	bodyTwo.Parent = engine.Workspace

	bottomBoundary = createRigidBodyFromVertices(Vector2(-400, 100), Vector2(400, 100), Vector2(400, -100), Vector2(-400, -100))
	bottomBoundary.Anchored = True
	bottomBoundary.Name = "BottomBoundary"
	bottomBoundary.Colour = Colour(200,200,200)
	bottomBoundary.Position = Vector2(engine.Workspace.AbsoluteSize.x/2, engine.Workspace.AbsoluteSize.y+99)
	bottomBoundary.Parent = engine.Workspace
	bottomBoundary.Mass = 0

	topBoundary = bottomBoundary.Clone()
	topBoundary.Position = Vector2(engine.Workspace.AbsoluteSize.x/2, -101)
	topBoundary.Name = "TopBoundary"
	topBoundary.Parent = engine.Workspace

	rightBoundary = createRigidBodyFromVertices(Vector2(-100, 225), Vector2(100, 225), Vector2(100, -225), Vector2(-100, -225))
	rightBoundary.Anchored = True
	rightBoundary.Name = "RightBoundary"
	rightBoundary.Colour = Colour(200,200,200)
	rightBoundary.Position = Vector2(engine.Workspace.AbsoluteSize.x + 99, engine.Workspace.AbsoluteSize.y/2)
	rightBoundary.Parent = engine.Workspace

	leftBoundary = rightBoundary.Clone()
	leftBoundary.Anchored = True
	leftBoundary.Name = "LeftBoundary"
	leftBoundary.Position = Vector2(-100, engine.Workspace.AbsoluteSize.y/2)
	leftBoundary.Parent = engine.Workspace

	interfaceBar = UIBase("Rectangle")
	interfaceBar.Name = "Border"
	interfaceBar.Size = UDim2(1,0,0.05,0)
	interfaceBar.Colour = Colour(100,100,100)
	interfaceBar.Parent = engine.UserInterface
	interfaceBar.ZIndex = 5

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
	image.ImageColour = Colour(100,100,100)
	image.DominantAxis = "y"
	image.ZIndex = 5

	print(engine.Tree)
	render(engine, surface)

	frames = 1000

	while frames > 0:
		frames -= 1
		for eventInstance in event.get():
			if eventInstance.type == QUIT:
				return
		updatePhysics(engine.Workspace, 1/framerate)
		render(engine, surface)
		display.update(engine.Workspace.Rectangle) # Use update RECT to specify WORKSPACE to render WORKSPACE for EFFICIENCY
		clock.tick_busy_loop(framerate)

run()
