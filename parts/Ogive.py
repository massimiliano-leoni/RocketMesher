import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math

class Ogive(object):
    ##  Represents a rocket ogive.
    #   The ogive can be represented by an arbitrary real function of real
    #   variable.
    #   For example, one could choose a Von Karman profile creating an ogive
    #   with expression parameter set to
    #   \f[
    #       \frac{4.5}{\sqrt{\pi}} \sqrt{\arccos \left(\frac{2t}{35}-1\right)
    #       - \frac{1}{2} \sin \left(2\arccos\left({\frac{2t}{35}-1}\right)\right)}
    #   \f]
    def __init__(self, name, length, expression):
        self.name = name
        self.length = length
        self.radius = 0
        self.expression = expression
        self.profile = geompy.MakeCurveParametric("t", self.expression, "0", 0, length, 100, GEOM.Interpolation, True)
