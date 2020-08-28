# >> CREDITS << 
# UDim2.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a UDim2 Class
# It allows for easy intuitive UI positioning

# >> MODULES <<
from vector2d import Vec2d as Vector2 # 2D Vector Class from pygame

# >> CLASSES <<
class UDim:
	def __init__(self, xs=0, x=0):
		self.Scale = xs
		self.Offset = x
	
class UDim2:
	def __init__(self, xs=0, x=0, ys=0, y=0):
		self.X = UDim(xs, x)
		self.Y = UDim(ys, y)

	def ToVector2(self, parentSize):
		return Vector2(self.X.Scale * parentSize.x + self.X.Offset, self.Y.Scale * parentSize.y + self.Y.Offset)