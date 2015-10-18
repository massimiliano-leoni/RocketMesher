import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class FinSection(object):
    """Represents a fin section.
        A fin section is identified by its profile.
        Assuming the section is a plane polygon, it suffices to know the
        coordinates of the vertices of the polygon to define a fin section.
        Accordingly, the fin section stores only its name and a list of points.

        This class is not meant to be used directly; instead, it should be
        subclassed and the derived class should build the points list, typically
        in its constructor, so as to give the shape of the specific subclass."""
    def __init__(self, name):
        self.name = name
        self.points = []

    def getProfile(self):
        """Gets the fin profile."""
        return self.profile
    
    def setProfile(self, profile):
        """Sets the fin profile."""
        self.profile = profile
    
    def buildProfile(self):
        """Build fin profile."""
        edges = [geompy.MakeEdge(geompy.MakeVertex(self.points[i-1][0],
                                                   self.points[i-1][1],0.),
                                 geompy.MakeVertex(self.points[i][0],
                                                   self.points[i][1],0.))
                        for i in range(len(self.points))]

        self.profile = geompy.MakeWire(edges)

        self.centerProfile()

    def getHeight(self):
        """Calculates the height of the fin."""
        bb = geompy.BoundingBox(self.profile,True)

        return bb[3]-bb[2]
        
    def getLength(self):
        """Calculates the height of the fin."""
        bb = geompy.BoundingBox(self.profile,True)

        return bb[1]-bb[0]
        
    def centerProfile(self):
        """Centers the profile with respect to the rocket axis."""
        self.setProfile(geompy.MakeTranslation(self.getProfile(),
                                                     0.,
                                                     -self.getHeight()/2,
                                                     0.)) 


class RectangularFinSection(FinSection):
    """Represents a fin with rectangular section.
        Such a fin is created by specifying its name, length and height."""
    def __init__(self, name, length, height):
        """Define the vertices of the rectangular profile."""
        FinSection.__init__(self, name)
        
        self.points.append((0, 0))
        self.points.append((length, 0))
        self.points.append((length, height))
        self.points.append((0, height))

class RhomboidalFinSection(FinSection):
    """Represents a fin with rhomboidal section.
        The constructor takes the fin section name, length and height
        (lengths of the horizontal and vertical diagonals, respectively)."""
    def __init__(self, name, length, height):
        """Define the vertices of the rhomboidal profile."""
        FinSection.__init__(self, name)
        
        self.points.append((length/2, 0))
        self.points.append((length, height/2))
        self.points.append((length/2, height))
        self.points.append((0, height/2))

class HexaFinSection(FinSection):
    """Represents a fin with hexagonal section.
        The defining dimensions are the length in the rocket direction (length),
        the length in the perpendicular direction (height) and the length of the
        edges parallel to the rocket direction (inner)."""
    def __init__(self, name, length, height, inner):
        """Define the vertices of the hexagonal profile."""
        FinSection.__init__(self, name)
        
        self.points.append(((length-inner)/2, 0))
        self.points.append(((length-inner)/2+inner, 0))
        self.points.append((length, height/2))
        self.points.append(((length-inner)/2+inner, height))
        self.points.append(((length-inner)/2, height))
        self.points.append((0, height/2))
