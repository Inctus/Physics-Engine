# >> CREDITS << 
# UIWrapper.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES << 
from pygame import Rect as Rectangle # I like longer variable names
from pygame import Color as Colour # UK > US
from pygame import image,transform,PixelArray # For image manipulation

from classes.vector2d import Vector2 # 2D Vector Class from pygame
from classes.udim2 import UDim2 # UDim2 >> Allows me to quickly position UI elements using a mixture of % and px
from shared.settings import gravity,drag,screenSize,classNames,slop,angularSlop # Grab settings like gravity, drag, friction, elasticity

from copy import deepcopy,copy # Copy >> Allows me to deepCopy whole classes (Useful for Cloning)
from uuid import uuid1 as UUID # ID Generation
from math import pi, sin, floor # For rigidbody math

# >> GLOBALS <<

gravityVector = Vector2(0, gravity)
dragCoeff = 1-drag

# >> CLASSES <<
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

class RigidBody(UIBase):

	__slots__ = ["_BoundingRectangle", "Position", "Velocity", "Acceleration", "Rotation", "AngularVelocity", "AngularAcceleration", "_Forces", "_Impulses", "Anchored", "Mass", "SafeAnchored"]

	def __init__(self, className="Polygon", parent=None):
		UIBase.__init__(self, className, parent)

		self.Position = Vector2() # Convert to Vector2. No need for UDim2 anymore.
		self.Velocity = Vector2() # Initial velocity has to be set while self.Velocity = Vector2()
		self.Acceleration = Vector2()
		self.Rotation = 0
		self.AngularVelocity = 0 
		self.AngularAcceleration = 0

		self._Forces = [] # Forces with a force and an origin (origins are local)
		self._Impulses = [] # Forces with a duration of 1 frame.
		self._BoundingRectangle = None

		self.SafeAnchored = False
		self.Anchored = False
		self.Mass = 1

	def __str__(self):
		return f"RigidBody({self.ClassName}) {self.Name}"

	@UIBase.Parent.setter
	def Parent(self, newParent): # reParenting instances yields. Set attributes before parenting.
		if newParent!=None and (not newParent.IsDescendantOfClass("Workspace")):
			raise ValueError(f"{str(newParent)} is not descended from a valid Workspace")
		if self._Parent:
			self._Parent._RemoveChild(self)
		self._Parent = newParent
		if newParent:
			newParent._AddChild(self)

	@UIBase.Vertices.getter # Change this because all rigidbodies will have vertices input as Vector2s
	def Vertices(self):
		return [vertex.rotatedRadians(self.Rotation) + self.AbsolutePosition for vertex in self._Vertices]

	@UIBase.SpriteVertices.getter
	def SpriteVertices(self): # Unnecessary with RigidBody
		return self._Vertices

	@UIBase.SpriteCenter.getter
	def SpriteCenter(self): # Unnecessary with RigidBody
		return Vector2()

	def AddForce(self, force, origin=False):
		if self.SafeAnchored:
			self.SafeAnchored = False
		self._Forces.append((force, origin-self.AbsolutePosition if origin else Vector2())) # Origin of force determines angular velocity component.

	def AddImpulse(self, impulse, origin=False):
		if self.SafeAnchored:
			self.SafeAnchored = False
		self._Impulses.append((impulse, origin-self.AbsolutePosition if origin else Vector2())) # Origin of force determines angular velocity component.

	def HandleForces(self): # TODO: add in drag
		acceleration = Vector2()
		angularAcceleration = 0
		impulseAcceleration = Vector2()
		impulseAngularAcceleration = 0
		for force in self._Forces:
			vector, origin = force
			acceleration += force[0]
			if not (force[1].length== 0):
				angularAcceleration += sin(vector.get_radians_between(origin)) * vector.length * origin.length
		for impulse in self._Impulses:
			vector, origin = impulse
			impulseAcceleration += impulse[0]
			if not (impulse[1].length == 0):
				impulseAngularAcceleration += sin(vector.get_radians_between(origin)) * vector.length * origin.length
		self._Impulses = []
		return acceleration/self.Mass + gravityVector, angularAcceleration/self.Mass, impulseAcceleration, impulseAngularAcceleration

	def Update(self, dt): # Delta time parameter. Help from https://en.wikipedia.org/wiki/Verlet_integration
		if not self.Anchored and not self.SafeAnchored:
			newPosition = self.Position + self.Velocity*dt + self.Acceleration*dt*dt*0.5
			newRotation = self.Rotation + self.AngularVelocity*dt + self.AngularAcceleration*dt*dt*0.5
			newAcceleration, newAngularAcceleration, impulseAcceleration, impulseAngularAcceleration = self.HandleForces()
			newVelocity = self.Velocity*(1-drag) + (self.Acceleration+newAcceleration)*dt*0.5 + impulseAcceleration*0.5
			newAngularVelocity = self.AngularVelocity + (self.AngularAcceleration+newAngularAcceleration)*dt*0.5 + impulseAngularAcceleration*0.5
			self.Position, self.Velocity, self.Acceleration = newPosition, newVelocity, newAcceleration
			self.Rotation, self.AngularVelocity, self.AngularAcceleration = newRotation, newAngularVelocity, newAngularAcceleration
			if self.Velocity.length <= slop and self.AngularVelocity <= angularSlop:
				self.SafeAnchored = True # Stop unnecessary sinkage or gliding

	@property # Polymorphism to conform with Vector2
	def AbsolutePosition(self):
		if self.Parent:
			return self.Position + self.Parent.AbsolutePosition
		else:
			return self.Position

	def Clone(self):
		# >> Attributes
		clone = RigidBody(self.ClassName)
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
		# RigidBody attributes
		clone.Position = self.Position
		clone.Velocity = self.Velocity
		clone.Acceleration = self.Acceleration
		clone.Rotation = self.Rotation
		clone.AngularVelocity = self.AngularVelocity
		clone.AngularAcceleration = self.AngularAcceleration
		clone._Forces = deepcopy(self._Forces)
		clone._Impulses = deepcopy(self._Impulses)
		clone.Anchored = self.Anchored
		clone.SafeAnchored = self.SafeAnchored
		clone.Mass = self.Mass
		return clone


class Interface(UIBase):

	__slots__ = ["_Image", "Callback", "_ConstrainAxes", "_DominantAxis", "_InternalImage", "_ImageColour"]

	def __init__(self, className, parent=None):
		UIBase.__init__(self, className, parent)

		self.Callback = None

		self._Image = None
		self._ConstrainAxes = False
		self._DominantAxis = "y"
		self._InternalImage = None
		self._ImageColour = Colour(255,255,255)

	def __str__(self):
		return f"Interface({self.ClassName}) {self.Name}"

	@UIBase.Rectangle.getter
	def Rectangle(self):
		if not self.ConstrainAxes:
			return Rectangle(
				self.AbsolutePosition.x, self.AbsolutePosition.y,
				self.AbsoluteSize.x, self.AbsoluteSize.y
				)
		elif self.DominantAxis == "y":
			return Rectangle(
				self.AbsolutePosition.x + (self.AbsoluteSize.x-self.AbsoluteSize.y)/2, self.AbsolutePosition.y,
				self.AbsoluteSize.y, self.AbsoluteSize.y
				)
		else:
			return Rectangle(
				self.AbsolutePosition.x, self.AbsolutePosition.y + (self.AbsoluteSize.y-self.AbsoluteSize.x)/2,
				self.AbsoluteSize.x, self.AbsoluteSize.x
				)

	@UIBase.Parent.setter
	def Parent(self, newParent): # reParenting instances yields. Set attributes before parenting.
		if newParent!=None and not newParent.IsDescendantOfClass("UserInterface"):
			raise ValueError(f"{str(newParent)} is not descended from a valid UserInterface")
		if self._Parent:
			self._Parent._RemoveChild(self)
		self._Parent = newParent
		if newParent:
			newParent._AddChild(self)
			while not newParent.FindFirstChildOfID(self.ID):
				pass

	def _UpdateImage(self, completeness):
		if completeness <= 1:
			self._InternalImage = image.load(self._Image).convert_alpha()
		if completeness <= 2:
			absoluteSize = floor(self.AbsoluteSize)
			if self.ConstrainAxes:
				if self.DominantAxis == "y":
					absoluteSize.x = absoluteSize.y
				else:
					absoluteSize.y = absoluteSize.x
			self._InternalImage = transform.smoothscale(self._InternalImage, (absoluteSize.x, absoluteSize.y))
		if completeness <= 3:
			pixArray = PixelArray(self._InternalImage)
			pixArray.replace(Colour(255,255,255), self.ImageColour, 0.8)

	@property
	def DominantAxis(self):
		return self._DominantAxis
	
	@DominantAxis.setter
	def DominantAxis(self, newValue):
		self._DominantAxis = newValue
		self._UpdateImage(2)
	

	@property
	def ConstrainAxes(self):
		return self._ConstrainAxes
	
	@ConstrainAxes.setter
	def ConstrainAxes(self, newValue):
		self._ConstrainAxes = newValue
		self._UpdateImage(2)

	@UIBase.Size.getter
	def Size(self):
		return self._Size

	@UIBase.Size.setter
	def Size(self, newSize):
		self._Size = newSize
		self._UpdateImage(1)

	@property
	def ImageColour(self):
		return self._ImageColour
	
	@ImageColour.setter
	def ImageColour(self, newColour):
		self._ImageColour = newColour
		self._UpdateImage(3)

	@property
	def Image(self):
		return self._Image

	@Image.setter
	def Image(self, fileName):
		if self.ClassName == "ImageLabel" or self.ClassName == "ImageButton":
			self._Image = fileName
			self._UpdateImage(1)

	def Draw(self, screen):
		screen.blit(self._InternalImage, self.Rectangle)

	def Clone(self):
		# >> Attributes
		clone = Interface(self.ClassName)
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
		# Interface attributes
		clone.Callback = None
		clone._Image = self._Image
		clone._ConstrainAxes = self._ConstrainAxes
		clone._DominantAxis = self._DominantAxis
		clone._InternalImage = self._InternalImage
		clone._ImageColour = self._ImageColour
		return clone
