# >> CREDITS << 
# UIWrapper.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES << 
from pygame import Rect as Rectangle # I like longer variable names
from pygame import Color as Colour # UK > US
from vector2d import Vec2d as Vector2 # 2D Vector Class from pygame
#from udim2 import udim as UDim2 # UDim2 >> Allows me to quickly position UI elements using a mixture of % and px
from copy import deepcopy as deepCopy # Copy >> Allows me to deepCopy whole classes (Useful for Cloning)

# >> GLOBAL VARIABLES <<
screenSize = Vector2() # A global variable which will be used to store the ScreenSize as a Vector

classNames = [
"rectangle",
"ellipse",
"polygon",
"workspace" # workspace = physics parent
]

# >> FUNCTIONS <<
def initialise(ss): # ss -> Vector2
	global screenSize
	screenSize = ss

# >> CLASSES <<
class UIObject: # No Inheritance necessary.

	def __init__(self, className, parent=None):
		# >> ClassName
		if className in classNames:
			self.ClassName = className
		else:
			raise ValueError(f"Unknown className, {className}")
		# >> Attributes
		self.Name = ""
		self.Visible = True
		self.Colour = Colour(255,255,255)
		self.Anchored = True
		self.ZIndex = 0
		# >> Private Attributes
		self.__Position = UDim2()
		self.__Size = UDim2()
		self.__Vertices = []
		self.__Children = []

	def __del__(self): # Deletion Behaviour
		if self.__Parent:
			self.__Parent.__RemoveChild(self)
		for child in self.__Children:
			del(child)

	def __AddChild(self, newChild):
		if not newChild in self.__Children:
			self.__Children.append(newChild)

	def __RemoveChild(self, oldChild):
		if oldChild in self.__Children:
			self.__Children.remove(oldChild)
