# >> CREDITS << 
# UIBase.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES << 
from pygame import Rect as Rectangle # I like longer variable names
from pygame import Color as Colour # UK > US

from classes.vector2d import Vector2 # 2D Vector Class from pygame
from classes.udim2 import UDim2 # UDim2 >> Allows me to quickly position UI elements using a mixture of % and px
from shared.settings import screenSize,classNames # Grab settings like gravity, drag, friction, elasticity

from copy import deepcopy,copy # Copy >> Allows me to deepCopy whole classes (Useful for Cloning)
from uuid import uuid1 as UUID # ID Generation

# >> CLASS <<
class UIBase: # No Inheritance necessary.

	__slots__ = ["Name", "Visible", "Colour", "ZIndex", "ID", "ClassName", "_Rotation", "_Parent", "_Position", "_Size", "_Vertices", "_Children"]


	def __init__(self, className, parent=None):
		# >> Class Names
		if className in classNames:
			self.ClassName = className
		else:
			raise ValueError(f"Unknown className, {className}")
		# >> Attributes
		self.Name = ""
		self.Visible = True
		self.Colour = Colour(255,255,255)
		self.ZIndex = 0
		self.ID = UUID()
		if self.ClassName == "Polygon":
			self._Rotation = 0 # In radians to simplify calculations
		# >> Private Attributes
		self._Parent = parent
		self._Position = UDim2(0,0,0,0)
		self._Size = UDim2(1,0,1,0)
		self._Vertices = [] # List of UDim2 Values for easy manipulation
		self._Children = []

	def __del__(self): # Deletion Behaviour
		if self._Parent:
			self._Parent._RemoveChild(self)
		if self._Children:
			for child in self._Children:
				del(child)

	def __eq__(self, other):
		if isinstance(other, UIBase):
			return self.ID == other.ID
		else:
			return False

	def __str__(self):
		return f"UIBase({self.ClassName}) {self.Name}"

	__repr__=__str__

	def __getitem__(self, index):
		if self._Children:
			for child in self._Children:
				if child.Name == index:
					return child
		raise ValueError(f"{str(self)} has no such child {index}")

	def __getattr__(self, index):
		if self.__getattribute__("_Children"):
			for child in self.__getattribute__("_Children"):
				if child.Name == index:
					return child
		raise AttributeError(f"{str(self)} has no such attribute {index}")
	
	def IsDescendantOfClass(self, className):
		if self.ClassName == className:
			return True
		elif self.Parent:
			return self.Parent.IsDescendantOfClass(className)
		else:
			return False

	def _AddChild(self, newChild):
		if not newChild in self._Children:
			self._Children.append(newChild)

	def _RemoveChild(self, oldChild):
		if oldChild in self._Children:
			self._Children.remove(oldChild)

	def GetChildren(self):
		orderedChildren = copy(self._Children)
		orderedChildren.sort(key=lambda n: n.ZIndex) # Order children by ZIndex for rendering.
		return orderedChildren

	def GetDescendants(self):
		descendantList = self.GetChildren()
		for i in range(len(descendantList)):
			for subChild in descendantList[i].GetDescendants():
				descendantList.append(subChild)
		return descendantList

	def RemoveChildren(self):
		if self._Children:
			for child in self._Children:
				del(child)

	def Clone(self):
		# >> Attributes
		clone = UIBase(self.ClassName)
		clone.Name = self.Name
		clone.Visible = True
		clone.Colour = self.Colour
		clone.ZIndex = self.ZIndex
		if self.ClassName == "Polygon":
			clone.Rotation = self.Rotation
		# >> Private Attributes
		clone._Position = self.Position
		clone._Size = self._Size
		clone._Vertices = deepcopy(self._Vertices)
		clone._Children = []
		for child in self._Children:
			subChild = child.Clone()
			subChild.Parent = clone
		return clone

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

	def SetVertices(self, newVertices):
		self._Vertices = newVertices

	@property
	def Parent(self):
		return self._Parent

	@Parent.setter
	def Parent(self, newParent): # reParenting instances yields. Set attributes before parenting.
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
			return Vector2(screenSize[0], screenSize[1])

	@property
	def AbsolutePosition(self):
		if self.Parent:
			return self.Position.ToVector2(self.Parent.AbsoluteSize) + self.Parent.AbsolutePosition
		else:
			return self.Position.ToVector2(Vector2(screenSize[0], screenSize[1]))

	@property
	def SpriteVertices(self):
		parentSize = screenSize
		if self.Parent:
			parentSize = self.Parent.AbsoluteSize
		return [vertex.ToVector2(parentSize) for vertex in self._Vertices]

	@property
	def SpriteCenter(self): # Works for all CONVEX POLYGONS
		mid = Vector2()
		for vertex in self.SpriteVertices:
			mid = mid + vertex
		mid = mid / len(self._Vertices)
		return mid

	@property
	def Vertices(self):
		if self._Vertices:
			center = self.SpriteCenter
			return [(vertex-center).rotatedRadians(self.Rotation) + self.AbsolutePosition for vertex in self.SpriteVertices]
		else:
			return []
	
	@property
	def Size(self):
		return self._Size

	@Size.setter
	def Size(self, newSize):
		self._Size = newSize

	@property
	def Position(self):
		return self._Position

	@Position.setter
	def Position(self, newPosition):
		self._Position = newPosition
	
	@property
	def Rectangle(self):
		return Rectangle(
			self.AbsolutePosition.x, self.AbsolutePosition.y,
			self.AbsoluteSize.x, self.AbsoluteSize.y
			)

	@property
	def Rotation(self):
		if self.ClassName == "Polygon":
			return self._Rotation
		else:
			raise AttributeError(f"{str(self)} doesn't have a Rotation.")

	@Rotation.setter
	def Rotation(self, newRotation):
		if self.ClassName == "Polygon":
			self._Rotation = newRotation
		else:
			raise AttributeError(f"{str(self)} doesn't have a Rotation.")

	@property
	def Tree(self):
		string = str(self)
		if self._Children:
			for idx,child in enumerate(self._Children):
				string = string +f"\n{idx+1}."+ child._DescendantTree(1)
		return string

	def _DescendantTree(self, depth=0):
		string = "".join("\t" for i in range(0, depth)) + str(self)
		if self._Children:
			for idx,child in enumerate(self._Children):
				string = string +f"\n{idx+1}."+ child._DescendantTree(depth+1)
		return string