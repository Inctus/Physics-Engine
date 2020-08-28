# >> CREDITS << 
# UIWrapper.py written by Haashim Hussain 

# >> DESCRIPTION <<
# This is a module that contains a wrapper class for PyGame UI objects
# It allows me to quickly and easily create and change what I need for my UI Objects
# It simplifies the process of instanciating screen objects in PyGame

# >> MODULES <<
from pygame import Vec2D,Rect
import udim2 # UDim2 >> Allows me to quickly position UI elements using a mixture of % and px
import copy # Copy >> Allows me to deepCopy whole classes (Useful for Cloning)

# >> GLOBAL VARIABLES <<
global screenSize # A global variable which will be used to store the ScreenSize as a Vector

# >> FUNCTIONS <<
def initialise(ss): # ss -> Vec2D
	

# >> CLASSES <<

class UIObject: # No Inheritance necessary.
