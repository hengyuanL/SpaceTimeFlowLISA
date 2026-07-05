# encoding: latin2
"""Algorithm utilities used by SpaceTimeFlowLISA."""
__author__ = "Juan C. Duque"
__credits__ = "Copyright (c) 2009-11 Juan C. Duque"
__license__ = "New BSD License"
__version__ = "1.0.0"
__maintainer__ = "RiSE Group"
__email__ = "contacto@rise-group.org"

try:
    from areamanager import AreaManager
except ImportError:
    AreaManager = None

from helperfunctions import calculateGetisG
from helperfunctions import calculateMoranI
from helperfunctions import calculateGearyC
from helperfunctions import calculateMultiGearyC
from helperfunctions import calculateBivaraiteMoranI
from helperfunctions import quickSort2
from helperfunctions import neighborSort
from helperfunctions import randomOD

try:
    from memory import BasicMemory
    from memory import ExtendedMemory
    from regionmaker import RegionMaker
    from sommanager import geoSomManager
    from sommanager import somManager
except ImportError:
    BasicMemory = None
    ExtendedMemory = None
    RegionMaker = None
    geoSomManager = None
    somManager = None