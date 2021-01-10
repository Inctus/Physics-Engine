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

from classes.uibase import UIBase
from classes.vector2d import Vector2 # 2D Vector Class from pygame
from classes.udim2 import UDim2 # UDim2 >> Allows me to quickly position UI elements using a mixture of % and px

from copy import deepcopy,copy # Copy >> Allows me to deepCopy whole classes (Useful for Cloning)
from math import floor # For maths

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
