# PyGame Physics Engine
------- 
### Description:
This is my OCR A Level Cousework. It is a simple, lightweight 2D physics solver written in [Python](https://www.python.org) using the [PyGame](https://www.pygame.org/wiki/about) library. It will have functionality to Pause, Play and Save keyframes from the simulation, allowing for collaboration on projects by multiple people.

------- 
### Classes:
- `UDim2`: A lightweight class that allows positioning of UI elements using percentages and a pixel offset.
------
- `Vector2`: [PyGame](https://www.pygame.org/wiki/about)'s 2D vector class that is used to position vertices and every element on the screen.
-----
- `UIBase`: A UI Wrapper that simplifies creation and management of UI. Has several internal SubClasses that affect rendering. 
 ------- 
 i. `Workspace`⭢ The ancestor of all `RigidBodies`.
 
 ------- 
 ii. `Rectangle`⭢ A basic rectangle.
 
 ------- 
  iii. `Ellipse`⭢ An ellipse.
  
  
------
  iv. `Polygon`⭢ A polygon that must be convex that allows for `Rotation` and the setting of `Vertices` as `UDim2` values.
  
------- 
- `Interface`: Inherits from UIBase and has several internal SubClasses that affect rendering. It adds functionality for BackgroundColour, OutlineColour and TextColour where applicable. SubClasses are:
 ------- 
  iii. `ImageLabel`⭢ A label that displays an image. Introduces new attribute:
   
    a. "Image"⭢ The file to be displayed.
 ------- 
  iv. `ImageButton`⭢ A label that displays an image and has a callback for clicks. Introduces new attributes:
    
    a. "Image"⭢ The file to be displayed.
    b. "Callback"⭢ The function to be ran every time the image is clicked.
------- 
- `RigidBody`: Inherits from UIBase. It allows for the efficient creation and manipulation of RigidBodies and allows for Physics interactions with them. They must be a descendant of the `Workspace` when they are parented. Has one internal SubClass:
 ------- 
  i. `Polygon`⭢ A polygon that must be convex and allow for `Rotation`, setting `Vertices`. Due to it being a RigidBody Physics is applied to it. Introduces several new attributes:
  
    a. "Position"⭢ The Velocity of the RigidBody, as a Vector2
    
    b. "Velocity"⭢ The Velocity of the RigidBody.
    
    c. "Acceleration"⭢ The Acceleration of the RigidBody.
    
    d. "AngularVelocity"⭢ The Velocity of the RigidBody.
    
    e. "AngularAcceleration"⭢ The Acceleration of the RigidBody.
    
    f. "AddForce"⭢ Allows for you to manipulate the acceleration.
    
    g. "AddImpulse"⭢ Allows for you to manipulate the acceleration (for one frame).
    
    h. "Mass"⭢ An optional attribute that affects collisions.
### Timeline
Redoing the SAT and polygon clipping for the third time while working around UCAS.
