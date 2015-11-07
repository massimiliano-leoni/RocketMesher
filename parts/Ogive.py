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
    def __init__(self, name, length, expression, quality=100):
        self.name = name
        self.length = length
        self.radius = 0
        self.expression = expression
        self.profile = geompy.MakeCurveParametric("t", self.expression, "0", 0,
                                                  length, quality, GEOM.Interpolation, True)

class HaackOgive(Ogive):
    """docstring for HaackOgive"""
    def __init__(self, name, length, radius, C):
        theta = "acos(2*t/{0}-1)".format(length)
        expression = \
        "{0}/sqrt(pi)*sqrt({1} - 0.5*sin(2*{1}) + {2}*sin({1})*sin({1})*sin({1}))".format(radius,theta,C)
        super(HaackOgive, self).__init__(name,length,expression)
        self.radius = radius

class VonKarman(HaackOgive):
    """docstring for VonKarman"""
    def __init__(self, name, length, radius):
        super(VonKarman, self).__init__(name, length, radius, 0.0)
                
