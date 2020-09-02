# >> CREDITS << 
# Main.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES <<
import pygame
from engine.engine_model import createModel,render,createRigidBody,createRigidBodyFromVertices
import math

engine = createModel() # Engine.Workspace, Engine.UserInterface
body = createRigidBody(4, 10)
print(body.Vertices)
body.Rotation = math.pi/4
print(body.Vertices)