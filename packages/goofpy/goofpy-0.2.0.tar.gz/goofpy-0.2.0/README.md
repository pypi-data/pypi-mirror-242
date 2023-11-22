# GoofPy
A library for creating objects and game sims in Python, more things coming soon

## Currently supports:
- Pygame
- GameObjects
- Players
- Games

## Current limitations:
- 3D objects are somewhat limited and may be broken, movement on the z-axis, especially for the `Player` class is not fully supported
- Pygame window is buggy, runs at 1x1 scale by default, but even when changed, is impossible to close using the "X" in the top right or `Alt + F4`
- No renders, and no built-in rendering capabilities planned, however, Pygame support would help users make renders

## Docs:
- `goof` class:
Takes ID(int) and meta(any)
  ```
  import goofpy
  
  obj = goofpy.goof(0, "TestMeta")
  
  ```
  Class functions:
  `getID()`, `getMeta()`, and `setMeta(value)`, are properties of any `goof` class, self-explanatory
  The below are not part of the `goof` class but relate to it.
  - `getObjectByClass(class)` returns all instances of a certain class
  - `getMetaById(id)` is self-explanatory
  - `compareMeta(originalID, newID)` gets the meta of the object based on id, returns `True` if the 2 are equal
  - `getObjsWithMeta(meta)` returns all objects with a particular meta value

- `GameObject` class:
Takes an ID, x, y, z, data, type, can take zIndex(default is 0)
  ```
  import goofpy

  obj = goofpy.goof(0, "TestMeta")
  gObj = goofpy.GameObject(obj.goofid, 
  ```
  Class functions:
  There are class functions, but most are either self-explanatory or are useless to the user, because there are much simpler ways with the `Creator` class
  
- `Creator` class:
Takes no parameters
  ```
  import goofpy

  c = goofpy.Creator()
  ```
  Class functions:
  - `givePosition2D(obj: goof, x, y, zIndex)` takes these variables and creates a GameObject with them, with a set z of 0.0, a data of "", and a type of "2D"
  - `givePosition3D(obj: goof, x, y, z)` same as `givePosition2D` but gives a z of `z` and a type of "3D", and doesn't change zIndex
  - `new2D(x, y, zIndex, data)` same as `givePosition2D` but passes in data and doesn't pass in an object
  - `new3D(x, y, z, data)` same as `new2D` but passes in a float of z and not zIndex
  
- `Player` class:
Takes a x, y, z, facing, and fov
  ```
  import goofpy

  p = goofpy.Player(0.0, 0.0, 0.0, 0, 90)
  ```
  Class functions:
  - `isColliding(obj)` tests if the player is colliding with an object
  - `canSee(obj)` tests if `obj` is being faced at by the player,
  ### uses __THE BEST FUNCTION IN ALL OF PYTHON, math.atan2(y, x)__

  - `move(d)` moves `d` units in the direction the player is facing
  - `turn(deg)` turns the player `deg` degrees(positve or negative, loops from 0-360, cannot be > 360)
  
- `Game` class
Optionally takes width and height, if you want an actual window/render, and the module for the engine, default and __ONLY CURRENTLY SUPPORTED__ engine is pygame
  ```
  import goofpy

  g = goofpy.Game()
  ```
  Class functions:
  - `initEngine()` starts the engine, required for using other `Game` class functions
  - `keyPressed(key)` tests if the key named `key`
  - `runAtFPS(fps)` ticks the game at `fps` frames per second
  - `getEvents()` returns all events from the last tick
  - `run(gameFunction, fps)` runs the game, using `gameFunction()` as the code and setup for the game, and running it at `fps` frames per second, easier alternitve to custom setup, but more limited and standard
---
## Support:
- Email `business.endergames@gmail.com` for additional help or feedback
