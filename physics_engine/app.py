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
from classes.uihelper import Interface,UIBase
from classes.vector2d import Vector2

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
	body.Parent = engine["Workspace"]
	body.Colour = Colour(30,30,30)
	body.Position = Vector2(400, 225)
	body.Mass = 50

	interfaceBar = UIBase("Rectangle")
	interfaceBar.Parent = engine.UserInterface
	interfaceBar.Colour = Colour(30,30,30)

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
display.quit()