# >> CREDITS << 
# Settings.py written by Haashim Hussain

# >> DESCRIPTION <<
# This module will contain various settings allowing them to be changed here easily
# as opposed to having to search through mutliple files.

gravity = 100 #300 # Acceleration due to gravity. px/s
drag = 0.001 # Coefficient of Drag %/s

screenSize = (800, 500) # Size of screen
fullScreen = False # If the simulation should be ran fullscreen. I think not.

classNames = [
	"Workspace", # workspace = physics parent
	"EngineModel", # Parent of everything
	"UserInterface", # Parent of interface objects
	"ImageLabel", # Image Label
	"ImageButton", # Image Label with callback
	"Rectangle", # Again, just for UI elements
	"Ellipse", # This is just for UI elements
	"Polygon", # for all shapes I'll use this
]

polygonNames = [
	"",
	"Dot",
	"Line",
	"Triangle",
	"Square",
	"Pentagon",
	"Hexagon",
	"Heptagon",
	"Octagon",
	"Nonagon",
	"Decagon",
	"Hendecagon",
	"Dodecagon",
	"Tridecagon"
]