# >> CREDITS << 
# UIWrapper.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES << 
from pygame import Rect as Rectangle # I like longer variable names
from pygame import Color as Colour # UK > US
from pygame import image, Rect

from classes.vector2d import Vector2 # 2D Vector Class from pygame
from classes.udim2 import UDim2 # UDim2 >> Allows me to quickly position UI elements using a mixture of % and px
from shared.settings import gravity,drag,screenSize # Grab settings like gravity, drag, friction, elasticity

from copy import deepcopy as deepCopy # Copy >> Allows me to deepCopy whole classes (Useful for Cloning)
from uuid import uuid1 as UUID # ID Generation
from math import pi, sin

# >> GLOBAL VARIABLES <<
classNames = [
"Rectangle", # Again, just for UI elements
"Ellipse", # This is just for UI elements
"Polygon", # for all shapes I'll use this
"Workspace", # workspace = physics parent
"GameModel", # Parent of everything
"ImageLabel",
"ImageButton"
]

# >> CLASSES <<
class UIBase: # No Inheritance necessary.

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
		self._Position = UDim2()
		self._Size = UDim2()
		self._Vertices = [] # List of UDim2 Values for easy manipulation
		self._Children = []

	__slots__ = ["Name", "Visible", "Colour", "ZIndex", "ID", "ClassName", "_Rotation", "_Parent", "_Position", "_Size", "_Vertices", "_Children"]

	def __del__(self): # Deletion Behaviour
		if self._Parent:
			self._Parent._RemoveChild(self)
		for child in self._Children:
			del(child)

	def __eq__(self, other):
		return self.ID == other.ID

	def __str__(self):
		return f"UIBase({self.ClassName}) {self.Name}"

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
		clone.ZIndex = self.ZIndex
		clone.Rotation = self.Rotation
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
			return screenSize

	@property
	def AbsolutePosition(self):
		if self.Parent:
			return self.Position.ToVector2(self.Parent.AbsoluteSize) + self.Parent.AbsolutePosition
		else:
			return self.Position.ToVector2(screenSize)

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
		center = self.SpriteCenter
		return [(vertex-center).rotatedRadians(self.Rotation) + self.AbsolutePosition for vertex in self.SpriteVertices]
	
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
		return Rect(
			self.AbsolutePosition.x, self.AbsolutePosition.y,
			self.AbsoluteSize.x, self.AbsoluteSize.y
			)

	@property
	def Rotation():
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

class RigidBody(UIBase):

	__slots__ = ["Position", "Velocity", "Acceleration", "Rotation", "AngularVelocity", "AngularAcceleration"]

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

		self.Anchored = False
		self.Mass = 1

	def addForce(self, newForce, newForceOrigin=Vector2()):
		self._Forces.append((newForce, newForceOrigin-self.AbsolutePosition)) # Origin of force determines angular velocity component.

	def addImpulse(self, newImpulse, newImpulseOrigin=Vector2()):
		self._Impulses.append((newImpulse, newImpulseOrigin-self.AbsolutePosition)) # Origin of force determines angular velocity component.

	def handleForces(self): # TODO: add in drag
		acceleration = Vector2()
		angularAcceleration = 0
		for force in self._Forces:
			acceleration += force[0]
			if not (force[1] == Vector2()):
				angularAcceleration += sin(force[0].get_radians_between(force[1])) * force[0].length * force[1].length / self.Mass
		for impulse in self._Impulses: # Multiply impulses by 2 to negate division by two later. They provide instant accel.
			acceleration += impulse[0]*2
			if not (impulse[1] == Vector2()):
				angularAcceleration += 2 * sin(impulse[0].get_radians_between(impulse[1])) * impulse[0].length * impulse[1].length / self.Mass
		angularAcceleration %= pi*2
		self._Impulses = []
		acceleration += Vector2(0, -gravity*2) # Apply gravity as an impulse.
		return acceleration, angularAcceleration

	def update(self, dt): # Delta time parameter. Help from https://en.wikipedia.org/wiki/Verlet_integration
		if not self.Anchored:
			newPosition = self.Position + self.Velocity*dt + self.Acceleration*dt*dt*0.5
			newRotation = self.Rotation + self.AngularVelocity*dt + self.Acceleration*dt*dt*0.5
			newAcceleration, newAngularAcceleration = self.handleForces()
			newVelocity = self.Velocity + (self.Acceleration+newAcceleration)*dt*0.5
			newAngularVelocity = self.AngularVelocity + (self.AngularAcceleration+newAngularAcceleration)*dt*0.5
			self.Position, self.Velocity, self.Acceleration = newPosition, newVelocity, newAcceleration
			self.Rotation, self.AngularVelocity, self.AngularAcceleration = newRotation, newAngularVelocity, newAngularAcceleration

	@property # Polymorphism to conform with Vector2
	def AbsolutePosition(self):
		if self.Parent:
			return self.Position + self.Parent.AbsolutePosition
		else:
			return self.Position

class Interface(UIBase):

	__slots__ = ["_Image", "Callback"]

	def __init__(self, className, parent=None):
		UIBase.__init__(self, className, parent)

		self._Image = None
		self.Callback = None

	@property
	def Image(self):
		return self._Image

	@Image.setter
	def Image(self, fileName):
		if self.ClassName == "ImageLabel" or self.ClassName == "ImageButton":
			self._Image = image.load(fileName).convert()

	def draw(self, screen):
		screen.blit(self.Image, self.Rectangle)