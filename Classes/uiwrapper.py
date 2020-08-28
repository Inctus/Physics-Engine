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
from uuid import uuid1 as UUID # ID Generation

# >> GLOBAL VARIABLES <<
screenSize = Vector2() # A global variable which will be used to store the ScreenSize as a Vector

classNames = [
"rectangle", # Again, just for UI elements
"ellipse", # This is just for UI elements
"polygon", # for all shapes I'll use this
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
		if parent:
			self.Parent = parent
		# >> Attributes
		self.Name = ""
		self.Visible = True
		self.Colour = Colour(255,255,255)
		self.Anchored = True
		self.ZIndex = 0
		self.ID = UUID()
		# >> Private Attributes
		self.__Parent = None
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

	def GetChildren(self):
		orderedChildren = copy.deepcopy(self.__Children)
		orderedChildren.sort(key=lambda n: n.ZIndex) # Order children by ZIndex for rendering.
		return orderedChildren

	def Clone(self):
		# >> Attributes
		clone = UIObject(self.ClassName)
		clone.Name = self.Name
		clone.Visible = True
		clone.Colour = self.Colour
		clone.Anchored = self.Anchored
		clone.ZIndex = self.ZIndex
		# >> Private Attributes
		clone.__Position = self.Position
		clone.__Size = self.__Size
		clone.__Vertices = deepCopy(self.__Vertices)
		clone.__Children = []
		for child in self.Children:
			subChild = child.Clone()
			subChild.Parent = clone
		return clone

	def FindFirstChild(self, name):
		for child in self.__Children:
			if child.Name == name:
				return child
		return False

	def FindFirstChildOfClass(self, className):
		for child in self.__Children:
			if child.ClassName == className:
				return child
		return False

	def FindFirstChildOfID(self, ID):
		for child in self.__Children:
			if child.ID == ID:
				return child
		return False

	def AddVertex(self, newVertex): 
		self.__Vertices.append(newVertex)

	def RemoveVertex(self, oldVertex):
		self.__Vertices.remove(oldVertex)

	def ChangeVertex(self, index, newValue):
		self.__Vertices[index] = newValue

	@property
	def Parent(self):
		return self.__Parent

	@Parent.setter
	def Parent(self, newParent):
		if self.__Parent:
			self.__Parent.__RemoveChild(self)
		self.__Parent = newParent
		if newParent:
			newParent.__AddChild(self)
			while not newParent.FindFirstChildOfID(self.ID):
				pass
	@property
	def AbsoluteSize(self):
		if self.Parent:
			return UDim2.toVector2(self.Size, self.Parent.AbsoluteSize)
		else:
			return screenSize

	@property
	def AbsolutePosition(self):
		if self.Parent:
			return UDim2.toVector2(self.Position, self.Parent.AbsoluteSize) + self.Parent.AbsolutePos
		else:
			return Vector2()