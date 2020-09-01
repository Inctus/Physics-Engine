# >> CREDITS << 
# Main.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES <<
import pygame

import engine.engine_model

engine = engine.engine_model.CreateModel()
print(engine.Tree)
print(engine["Workspace"])
print(engine.Workspace.Parent.UserInterface.Parent.GetChildren())