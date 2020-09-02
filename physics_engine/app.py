# >> CREDITS << 
# Main.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES <<
import pygame
import math

from engine.engine_model import createModel,render,createRigidBody,createRigidBodyFromVertices

# >> FUNCTIONS <<

def run():
	# Engine initialisation
	engine= createModel() # Engine.Workspace, Engine.UserInterface

	# PyGame Initialisation
	pygame.init()
	surface = pygame.display.set_mode((engine.AbsoluteSize.x, engine.AbsoluteSize.y))
	clock = pygame.time.Clock()
	
	body = createRigidBody(4, 10)
	body.Name = "RigidSquare"
	body.Rotation = math.pi/4
	body.Parent = engine["Workspace"]

	print(engine.Tree)

	while True:
		render(engine, surface)
		pygame.display.update()
		clock.tick(30)

run()
pygame.display.quit()
pygame.quit()