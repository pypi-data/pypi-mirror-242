import gc
import math
import random

import pygame
import json
from urllib.request import urlopen

# See if the current project version is allowed
url = urlopen("https://raw.githubusercontent.com/endert1099/GoofPy/main/versions.json")
versions = json.loads(url.read())
currentVer = "0.1.1"
canUse = [False, "Version does not exist!"]
for v in range(len(versions)):
    sv = versions[v]
    if sv["version"] == currentVer:
        if sv["support"] == "supported":
            canUse = [True, None]
        elif sv["support"] == "too-low-warn":
            canUse = [True, "Version is too low, but still supported. Some functionality may be limited."]
        elif sv["support"] == "too-low":
            canUse = [False, "Version is too low and unsupported"]
        elif sv["support"] == "beta":
            canUse = [True, "Version is still in beta, some things may not work, but thank you for your support!"]
        elif sv["support"] == "NFU":
            canUse = [False, "Version is not for use, are you sure you have permissions?"]
if not canUse[0]:
    raise SystemExit("Version is not accepted for the following reason:\n" + canUse[1])
if not canUse[1] == None:
    print("[WARN]: " + canUse[1])


# Goof objects
class goof:
    def __init__(self, goofID: int, goofMeta: str):
        """
        Defines goof objects, the building blocks of everything in goofpy!
        :param goofID: The ID of the object
        :param goofMeta: The meta or data value of the object
        """
        self.goofID = goofID
        self.goofMeta = goofMeta

    def getId(self):
        """
        Get the ID of the current object
        :return: Returns the ID
        """
        return self.goofID

    def getMeta(self):
        """
        Gets the meta value of the current object
        :return: Returns the meta
        """
        return self.goofMeta

    def setMeta(self, value):
        """
        Sets the meta of the current object
        :param value: The meta to be changed
        :return: Returns the success of the operation
        """
        try:
            self.goofMeta = value
        except:
            return False
        return True


# External functions that relate to goof objects
def getObjectByClass(c):
    """
    Gets all the objects in a certain class
    :param c: The class to take the objects from
    :return: Returns an array of all instances of `c` class
    """
    objs = []
    for obj in gc.get_objects():
        if isinstance(obj, c):
            objs.append(obj)
    return objs


def getMetaByID(gid):
    """
    Gets the meta of an object with a certain ID
    :param gid: The ID of the object
    :return: The meta value of the object
    """
    objs = getObjectByClass(goof)
    for o in objs:
        if o.goofID == gid:
            return o.goofMeta
    return False


def compareMeta(originalID, newID):
    """
    Compares the meta values of 2 objects, by ID
    :param originalID: The ID of the first object
    :param newID: The ID of the second object
    :return: Returns true if `originalID` is equal to `newID`
    """
    try:
        ometa = getMetaByID(originalID)
        nmeta = getMetaByID(newID)
    except:
        raise ValueError("ID was not valid")
    if ometa == nmeta:
        return True
    else:
        return False


def getObjWithID(gid):
    """
    Returns the first object with a certain ID(Might break if your IDs are bad)
    :param gid: The ID to be used
    :return: The object gotten
    """
    objs = getObjectByClass(goof)
    for o in objs:
        if o.goofID == gid:
            return o


def getObjsWithMeta(meta):
    """
    Gets all objects with a certain meta value
    :param meta: The meta to be used
    :return: An array of all objects with a meta of `meta`
    """
    objs = getObjectByClass(goof)
    robjs = []
    for o in objs:
        if o.goofMeta == meta:
            robjs.append(o)
    return robjs


# Translate goof objects into other objects
class Creator:
    def __init__(self):
        """
        Converts goof objects (goof class) into other objects
        """

    def givePosition2D(self, obj: goof, x: float, y: float, zIndex: int):
        """
        Gives a new, blank object with a position from a goof object
        :param obj: The object to base it on
        :param x: The x position of the new object
        :param y: The y position of the new object
        :param zIndex: The index of the object, allows for layering without using 3D
        :return: Returns the newly created object
        """
        gobj = GameObject(obj.goofID, x, y, 0.0, "", "2D", zIndex)
        return gobj

    def givePosition3D(self, obj: goof, x: float, y: float, z: float):
        """
        Gives a new, blank object with a 3D position from a goof object
        :param obj: The object to base it on
        :param x: The x position of the new object
        :param y: The y position of the new object
        :param z: The z position of the new object
        :return: Returns the newly created object
        """
        gobj = GameObject(obj.goofID, x, y, z, "", "3D")
        return gobj

    def new2D(self, x: float, y: float, zIndex: int, data):
        """
        Creates a blank 2D object
        :param x: The x position of the new object
        :param y: The y position of the new object
        :param zIndex: The index of the object, allows for layering without using 3D
        :param data: The data to be sent to the object for creation, see the GameObject.formatData documentation for more info
        :return: Returns the new object
        """
        all_objs = getObjectByClass(goof)
        m = 0
        for obj in all_objs:
            if obj.goofID > m:
                m = obj.goofID
        m = m + 1

        gobj = GameObject(m, x, y, 0.0, data, "2D", zIndex)
        return gobj

    def new3D(self, x: float, y: float, z: float, data):
        """
        Creates a blank 3D object
        :param x: The x position of the new object
        :param y: The y position of the new object
        :param z: The z position of the new object
        :param data: The data to be sent to the object for creation, see the GameObject.formatData documentation for more info
        :return: Returns the new object
        """
        all_objs = getObjectByClass(goof)
        m = 0
        for obj in all_objs:
            if obj.goofID > m:
                m = obj.goofID
        m = m + 1

        gobj = GameObject(m, x, y, z, data, "3D")
        return gobj


# Game objects to be converted by the creator
class GameObject:
    def __init__(self, gid, x, y, z, data, gtype, zIndex=0):
        """
        GameObjects to be used in games
        :param gid: The ID of the object
        :param x: The x position of the new object
        :param y: The y position of the new object
        :param z: The z position of the new object
        :param data: The data to be sent to the object, see the GameObject.formatData documentation for more info
        :param gtype: The type of the object, 2D or 3D
        :param zIndex: Optional, the Z index instead of 2D objects
        """
        self.gid = gid
        self.x = x
        self.y = y
        self.z = z
        self.data = data
        self.gtype = gtype
        self.zIndex = zIndex

    def formatData(self):
        """
        Formats data in this order:
        ['scalex', val, 'scaley', val, 'scalez', val, 'collider', val, 'isActive', val, 'isInvis', val].
        Data should be an array with the above syntax, all of those 6 values in any order, but following a ['var', val] structure.
        Also filters out any incorrect values.
        Might break if one of the 6 is missing.
        :return: Returns the formatted list
        """
        nextc = 0
        data = []
        for i in self.data:
            if nextc > 0:
                data.insert(nextc - 1, i)
                nextc = 0

            if i == "scalex":
                nextc = 1
            elif i == "scaley":
                nextc = 2
            elif i == "scalez":
                nextc = 3
            elif i == "collider":
                nextc = 4
            elif i == "isActive":
                nextc = 5
            elif i == "isInvis":
                nextc = 6
        return data

    def getScale(self):
        """
        Gets the scale of the current object, x, y, and z, in that order
        :return: The x, y, and z scale, in an array
        """
        data = self.formatData()
        return data[0:3]

    def getCollider(self):
        """
        Gets whether the current object is a collider.
        :return: Returns if it is a collider
        """
        data = self.formatData()
        return data[3]

    def getActive(self):
        """
            Gets whether the current object is active.
            :return: Returns if it is active
        """
        data = self.formatData()
        return data[4]

    def getInvis(self):
        """
            Gets whether the current object is invisible.
            :return: Returns if it is invisible
        """
        data = self.formatData()
        return data[5]


# External functions that relate to GameObjects
def readFormattedData(data: list, valueID):
    """
    Gets formatted data and reads a value
    Useless lmao
    :param data: The formatted data
    :param valueID: The ID of the value
    :return: The proper value
    """
    return data[valueID - 1]


# Still working this one out
# TODO: FIX THIS(0.2.0/0.3.0)
'''def orderByZIndex():
    objs = getObjectByClass(GameObject)
    return objs.sort(objs, gid)'''


# Player class
class Player:
    def __init__(self, x, y, z, facing, fov):
        """
        The player to act certain functions on
        :param x: The x position of the player
        :param y: The x position of the player
        :param z: The x position of the player
        :param facing: The direction the player is facing
        :param fov: The feild of veiw of the player
        """
        self.x = x
        self.y = y
        self.z = z
        self.facing = facing
        self.fov = fov

    def isColliding(self, obj: GameObject):
        """
        Tests if the player is colliding with an object
        :param obj: The object to test
        :return: Returns true if collision is true
        """
        objData = obj.formatData()
        objScale = obj.getScale()
        isColliding: bool = False
        if obj.getCollider() and obj.getActive():
            for i in range(3):
                objScale[i] = objScale[i] / 2
            if obj.x - objScale[0] <= self.x <= obj.x + objScale[0]:
                if obj.y - objScale[1] <= self.y <= obj.y + objScale[1]:
                    if obj.z - objScale[2] <= self.z <= obj.z + objScale[2]:
                        isColliding = True
        return isColliding

    def canSee(self, obj: GameObject):
        """
        Tests if the player can see an object. It also checks this using math.atan2(y, x), the most underrated and also best function in python.
        :param obj: The object to test
        :return: Returns true if player can see the object
        """
        if not obj.getInvis() and obj.getActive():
            if self.isColliding(obj):
                return True  # If they're in the block, they can probably see it

            x = obj.x - self.x
            y = obj.x - self.x

            t = math.atan2(y, x)  # BEST FUNCTION IN PYTHON

            t = t * (180 / math.pi)
            if t < 0:
                t = 360 + t

            halfFOV = self.fov / 2

            if self.facing - halfFOV <= t <= self.facing + halfFOV and self.z - halfFOV <= obj.z <= self.z + halfFOV:
                return True
            return False

    def move(self, d: float):
        """
        Moves d units in the players direction, uses cool trig ;)
        :param d: The distance to move
        """
        o = self.facing * (math.pi / 180)
        x = d * math.cos(o)
        y = d * math.sin(o)
        self.x = self.x + round(x, 2)
        self.y = self.y + round(y, 2)

    def turn(self, deg: float):
        """
        Changes the direction of the player in degrees(even though radians are superior)
        :param deg: The degrees to turn
        """
        if deg > 360:
            raise ValueError("Turning degrees cannot be over 360!")
        f = self.facing + deg
        if f > 360:
            f = f - 360
        if f < 0:
            f = f + 360
        self.facing = f


class Game:
    def __init__(self, height: int = 1, width: int = 0, engine=pygame):  # supports only PyGame for now
        """
        Defines the game
        :param height: Optional, the height of the game window, starts at 1 to stop (0, 0) with width, but also allowing you to run the game
        :param width: Optional, the width of the game window, starts at 0
        :param engine: Optional, the game engine, only change if you want custom settings really, set to a module. If there is another game module for python, I will consider adding it, but for now it's just custom properties
        """
        self.width = width
        self.height = height
        self.engine = engine

        if self.engine == pygame:
            self.c = self.engine.time.Clock()
            self.d = self.engine.display
            self.s = self.d.set_mode((self.width, self.height))
        self.init = False

    def initEngine(self):
        """
        Initialises the current engine
        """
        if self.engine == pygame:
            self.engine.init()
            self.init = True

    def keyPressed(self, key: str):
        """
        Tests if a key is pressed
        :param key: The name of the key
        :return: If it is pressed
        """
        if self.engine == pygame and self.init:
            k = self.engine.key.get_pressed()
            k = k[self.engine.key.key_code(key)]
            return k

    def runAtFPS(self, fps: int):
        """
        Ticks the game at a certain rate of frames per second
        :param fps: The frames per second to refresh on
        """
        if self.engine == pygame and self.init:
            self.s.fill("black")
            self.d.flip()
            self.c.tick(fps)

    def getEvents(self):
        """
        Get the events of the game
        :return: The events since last tick
        """
        if self.engine == pygame and self.init:
            e = []
            for event in pygame.event.get():
                e.append(event)
            return e

    def run(self, gameFunction, fps: int):
        """
        Runs the game with specified code. Once called, loops until quit.
        :param gameFunction: The function to be run once per tick, renders/updates the game
        :param fps: The frames per second max to run the game at
        """
        if self.engine == pygame and self.init:
            running = True
            while running:
                e = self.getEvents()
                if not e is None:
                    if self.engine.QUIT in e:
                        running = False

                gameFunction()

                self.runAtFPS(fps)


# THIS ENDS GAME CLASSES AND STARTS PHYSICS CLASSES

class Physics:
    def __init__(self, x: float, y: float, z: float, g: float, b: float, bl: int, s: float, st: float, gr: float, m: float):
        """
        Defines a physics object that will move and change based on physics updates
        :param x: The starting x of the object
        :param y: The starting y of the object
        :param z: The starting z of the object
        :param g: The gravity of the object
        :param b: The bounciness of the object
        :param bl: The loss of bounciness per bounce, random from `bl to 3bl
        :param s: The chance of the object breaking on impact
        :param st: The z value required to shatter, will not shatter if the distance from the original z to the ground
        :param gr: The z level of the ground
        :param m: The mass of the object
        """
        self.x = x
        self.y = y
        self.z = z
        self.g = g * 9.87  # count of earths gravity, g is a constant of earths gravity
        self.b = b * 9.87  # proportionalise b to match g
        self.bl = bl * 9.87  # same with bl
        self.s = s
        self.st = st
        self.gr = gr
        self.m = m
        self.a = 0

def updatePhysics():
    global pLastFrame
    pLastFrame = []
    physics = getObjectByClass(Physics)
    delp = True

    for p in physics:
        sz = p.z
        if p.gr != p.z:
            p.a = p.a + p.g * abs(((p.m * p.g) / (p.z - p.gr) ** 2))
            p.z = p.z - p.g - p.a
            if p.z < p.gr:
                p.z = p.gr
            p.g = round(p.g, 3)
            p.b = round(p.b, 3)
            p.z = round(p.z, 3)
        else:
            p.a = 0
            shatter = round(random.random(), 2)
            if shatter < p.s / 100 and sz - p.gr >= p.st:
                delp = False
                print(f"[GOOFPY PHYSICS]: Object shattered - {p}")

            if p.b > p.g and delp:
                p.z += p.b - p.g
                p.g = round(p.g, 3)
                p.b = round(p.b, 3)
                p.z = round(p.z, 3)
                l = int(p.bl)
                try:
                    p.b -= round(random.randrange(l, l * 3), 3)
                except ValueError:
                    raise TypeError("Bounce loss must be an integer")
                if p.b < 0:
                    p.b = 0
            else:
                p.b = 0
        p.g = round(p.g, 3)
        p.b = round(p.b, 3)
        p.z = round(p.z, 3) # Prevents precision loss
        pLastFrame = [p.b, p.g, p.z]
        if not delp:
            del p
def savePhysicsToJson(data: list):
    jsond = "[{"
    for i in range(len(data)):
        jsond = jsond + data[i]
        if i != len(data) - 1:
            jsond = jsond + "},{"
    jsond = jsond + "}]"
    f = open("physicsJSON.json", "w")
    jsond.replace('\\\"', '"')
    f.write(jsond)
    f.close()
