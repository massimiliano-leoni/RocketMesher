import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class FinSection(object):
    """represents a fin section"""
    def __init__(self, name):
        self.name = name
        self.points = []

    def getProfile(self):
        """gets the fin profile"""
        return self.profile
    
    def setProfile(self, profile):
        """sets the fin profile"""
        self.profile = profile
    
    def buildProfile(self):
        """build fin profile"""
        edges = [geompy.MakeEdge(geompy.MakeVertex(self.points[i-1][0],
                                                   self.points[i-1][1],0.),
                                 geompy.MakeVertex(self.points[i][0],
                                                   self.points[i][1],0.))
                        for i in range(len(self.points))]

        self.profile = geompy.MakeWire(edges)

        self.centerProfile()

    def getHeight(self):
        """calculates height of generic fin"""
        minY = min([P[1] for P in self.points])
        maxY = max([P[1] for P in self.points])

        return maxY - minY
        

    def centerProfile(self):
        """center the profile wrt the rocket axis"""
        self.setProfile(geompy.MakeTranslation(self.getProfile(),
                                                     0.,
                                                     -self.getHeight()/2,
                                                     0.)) 


class RectangularFinSection(FinSection):
    """represents a fin with rectangular section"""
    def __init__(self, name, length, height):
        FinSection.__init__(self, name)
        
        self.points.append((0, 0))
        self.points.append((length, 0))
        self.points.append((length, height))
        self.points.append((0, height))

class RomboidalFinSection(FinSection):
    """represents a fin with romboidal  section"""
    def __init__(self, name, length, height):
        FinSection.__init__(self, name)
        
        self.points.append((length/2, 0))
        self.points.append((length, height/2))
        self.points.append((length/2, height))
        self.points.append((0, height/2))

class HexaFinSection(FinSection):
    """represents a fin with romboidal  section"""
    def __init__(self, name, length, height, inner):
        FinSection.__init__(self, name)
        
        self.points.append(((length-inner)/2, 0))
        self.points.append(((length-inner)/2+inner, 0))
        self.points.append((length, height/2))
        self.points.append(((length-inner)/2+inner, height))
        self.points.append(((length-inner)/2, height))
        self.points.append((0, height/2))
