# >> CREDITS << 
# UIBase.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES << 
from classes.vector2d import Vector2 # 2D Vector Class from pygame
from classes.udim2 import UDim2 # UDim2 >> Allows me to quickly position UI elements using a mixture of % and px
from classes.uibase import UIBase # UIBase >> allows me to inherit
from shared.settings import gravity,drag,screenSize,classNames,slop,angularSlop # Grab settings like gravity, drag, friction, elasticity

from copy import deepcopy,copy # Copy >> Allows me to deepCopy whole classes (Useful for Cloning)
from math import pi, sin, floor # For rigidbody math

# >> GLOBALS <<

gravityVector = Vector2(0, gravity)
dragCoeff = 1-drag

# >> CLASS <<
class RigidBody(UIBase):

	__slots__ = ["Position", "Velocity", "Acceleration", "Rotation", "AngularVelocity", "AngularAcceleration", "_Forces", "_Impulses", "Anchored", "Mass", "SafeAnchored"]

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