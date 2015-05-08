import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class Fins(object):
    """represents a group of fins"""
    def __init__(self, name, height, finSection, tube, finNumber=4,
                 verticalOffset=0, angularOffset=0, scaleFactor=1, theta=0):
        self.name = name
        self.height = float(height)
        self.finNumber = finNumber
        self.angularOffset = angularOffset
        self.verticalOffset = verticalOffset
        self.finSection = finSection
        self.section = finSection.getProfile()
        self.position = tube.position
        self.radius = tube.radius
        self.scaleFactor = scaleFactor
        self.theta = theta
        tube.addFins(self)

    def getHeight(self):
        """gets height"""
        return self.height

    def setHeight(self, h):
        """sets height"""
        self.height = float(h)

    def getFinNumber(self):
        """gets the number of fins"""
        return self.finNumber

    def setFinNumber(self, n):
        """sets the number of fins in the set"""
        self.finNumber = n

    def getVerticalOffset(self):
        """gets the vertical offset"""
        return self.verticalOffset

    def setVerticalOffset(self, l):
        """sets vertical offset"""
        self.verticalOffset = l

    def getAngularOffset(self):
        """gets angular offset"""
        return self.angularOffset

    def setAngularOffset(self, theta):
        """sets angular offset"""
        self.angularOffset = theta

    def buildFins(self):
        """builds the group of fins"""
        width = self.finSection.getHeight()
        radialAdjustment = self.radius - math.sqrt(self.radius**2 -
                                                   (width/2)**2) + 0.001
        self.section = \
            geompy.MakeTranslation(self.section,
                                   self.position + self.getVerticalOffset(),
                                   0,
                                   self.radius - radialAdjustment)

        face = geompy.MakeFaceWires([self.section], True)

        OZ = geompy.MakeVectorDXDYDZ(math.cos(self.theta + math.pi/2),
                                     0,
                                     math.sin(self.theta + math.pi/2))
        fin = geompy.MakePrismVecH(face, OZ, self.height, self.scaleFactor)
        
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
        fins = []

        for i in range(self.finNumber):
            fins.append(geompy.MakeRotation(fin, OX,
                                            i*2*math.pi/self.getFinNumber()
                                           + self.getAngularOffset()))


        self.fins = geompy.MakeFuseList(fins, True)
        
