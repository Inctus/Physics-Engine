# Physics-Engine
### Description:
This is my OCR A Level Cousework. It is a simple, lightweight 2D physics solver written in [Python](https://www.python.org) using the [PyGame](https://www.pygame.org/wiki/about) library. It will have functionality to Pause, Play and Save keyframes from the simulation, allowing for collaboration on projects by multiple people.
### Classes:
- `UDim2`: A lightweight class that allows positioning of UI elements using percentages and a pixel offset.
- `Vector2`: [PyGame](https://www.pygame.org/wiki/about)'s 2D vector class that is used to position vertices and every element on the screen.
- `UIWrapper`: A UI wrapper for [PyGame](https://www.pygame.org/wiki/about) that allows for vertex manipulation and rotation of objects before they are drawn onto the PyGame screen. It also allows for efficient creation and management of said objects, via a tree structure. It allows for traversal via a Child-Parent heirachy stemming from a physics viewport, called the Workspace.
