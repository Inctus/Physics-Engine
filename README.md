# PyGame Physics Engine
### Description:
This is my OCR A Level Cousework. It is a simple, lightweight 2D physics solver written in [Python](https://www.python.org) using the [PyGame](https://www.pygame.org/wiki/about) library. It will have functionality to Pause, Play and Save keyframes from the simulation, allowing for collaboration on projects by multiple people.
### Classes:
- `UDim2`: A lightweight class that allows positioning of UI elements using percentages and a pixel offset.
- `Vector2`: [PyGame](https://www.pygame.org/wiki/about)'s 2D vector class that is used to position vertices and every element on the screen.
- `UIBase`: A UI Wrapper that simplifies creation and management of UI. Has several internal SubClasses that affect rendering. These are `Workspace`, a UI Element that acts as the ancestor for all `RigidBody` instances, a `Rectangle`, an `Ellipse` and a `Polygon`.
  - `Interface`: Inherits from UIBase and has several internal SubClasses that affect rendering. Allows for easy manipulation and creation of UI Elements, including `TextLabels`, `TextButtons`, `ImageButtons` and `ImageLabels`.
  - `RigidBody`: Inherits from UIBase. Has one internal SubClass, `Polygon`. It allows for the efficient creation and manipulation of RigidBodies and allows for Physics interactions with them. They must be a descendant of the `Workspace` when they are parented.

### Timeline
The majority of the project will be completed within a week.
