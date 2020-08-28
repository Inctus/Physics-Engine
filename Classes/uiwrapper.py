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
from udim2 import UDim2 # UDim2 >> Allows me to quickly position UI elements using a mixture of % and px
from copy import deepcopy as deepCopy # Copy >> Allows me to deepCopy whole classes (Useful for Cloning)
from uuid import uuid1 as UUID # ID Generation

# >> GLOBAL VARIABLES <<
screenSize = Vector2(0,0) # A global variable which will be used to store the ScreenSize as a Vector

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
			self._Parent = parent
		# >> Attributes
		self.Name = ""
		self.Visible = True
		self.Colour = Colour(255,255,255)
		self.Anchored = True
		self.ZIndex = 0
		self.ID = UUID()
		# >> Private Attributes
		self._Parent = None
		self._Position = UDim2()
		self._Size = UDim2()
		self._Vertices = [] # List of UDim2 Values for easy manipulation
		self._Children = []

	def __del__(self): # Deletion Behaviour
		if self._Parent:
			self._Parent._RemoveChild(self)
		for child in self._Children:
			del(child)

	def _AddChild(self, newChild):
		if not newChild in self._Children:
			self._Children.append(newChild)

	def _RemoveChild(self, oldChild):
		if oldChild in self._Children:
			self._Children.remove(oldChild)

	def GetChildren(self):
		orderedChildren = copy.deepcopy(self._Children)
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
		clone._Position = self.Position
		clone._Size = self._Size
		clone._Vertices = deepCopy(self._Vertices)
		clone._Children = []
		for child in self.Children:
			subChild = child.Clone()
			subChild.Parent = clone
		return clone

	def FindFirstChild(self, name):
		for child in self._Children:
			if child.Name == name:
				return child
		return False

	def FindFirstChildOfClass(self, className):
		for child in self._Children:
			if child.ClassName == className:
				return child
		return False

	def FindFirstChildOfID(self, ID):
		for child in self._Children:
			if child.ID == ID:
				return child
		return False

	def AddVertex(self, newVertex): 
		self._Vertices.append(newVertex)

	def RemoveVertex(self, oldVertex):
		self._Vertices.remove(oldVertex)

	def ChangeVertex(self, index, newValue):
		self._Vertices[index] = newValue

	@property
	def Parent(self):
		return self._Parent

	@Parent.setter
	def Parent(self, newParent):
		if self._Parent:
			self._Parent._RemoveChild(self)
		self._Parent = newParent
		if newParent:
			newParent._AddChild(self)
			while not newParent.FindFirstChildOfID(self.ID):
				pass
	@property
	def AbsoluteSize(self):
		if self.Parent:
			return self.Size.ToVector2(self.Parent.AbsoluteSize)
		else:
			return screenSize

	@property
	def AbsolutePosition(self):
		if self.Parent:
			return self.Position.ToVector2(self.Parent.AbsoluteSize) + self.Parent.AbsolutePosition
		else:
			return self.Position.ToVector2(screenSize)

	@property
	def Vertices(self):
		newVertices = []
		parentSize = screenSize
		if self.Parent:
			parentSize = self.Parent.AbsoluteSize
		for vertex in self._Vertices:
			newVertices.append(self.AbsolutePosition + vertex.ToVector2(parentSize))
		return newVertices

	@property
	def LocalVertices(self):
		parentSize = screenSize
		if self.Parent:
			parentSize = self.Parent.AbsoluteSize
		newVertices = [vertex.ToVector2(parentSize) for vertex in self._Vertices]
		return newVertices

	@property
	def Center(self):
		mid = Vector2()
		print(self.LocalVertices)
		for vertex in self.LocalVertices:
			mid = mid + vertex
		print(mid)
		mid = mid / len(self._Vertices)
		return mid

	@property
	def PlanarVertices(self):
		newVertices = []
		center = self.Center
		for vertex in self.LocalVertices:
			newVertices.append(vertex-center)
		return newVertices

	@property
	def Size(self):
		return self._Size

	@Size.setter
	def Size(self, newSize):
		self.Size = newSize

	@property
	def Position(self):
		return self._Position

	@Position.setter
	def Position(self, newPosition):
		self.Position = newPosition
	
	@property
	def Rectangle(self):
		return pygame.Rect(
			self.AbsolutePos.x, self.AbsolutePos.y,
			self.AbsoluteSize.x, self.AbsoluteSize.y
			)