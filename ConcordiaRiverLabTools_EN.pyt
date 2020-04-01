# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Juin 2018 - Création

# Compilation des outils développés pour la gestion des rivières

# ENGLISH INTERFACE version

from EN_Interface.FlowLength_EN_Interface import *
from EN_Interface.Breach_EN_Interface import *
from EN_Interface.Slope_EN_Interface import *
from EN_Interface.FromPoints_EN_Interface import *
from EN_Interface.CS_EN_Interface import *
from EN_Interface.OrientedCS_EN_Interface import *
from EN_Interface.ChannelDetector_EN_Interface import *
from EN_Interface.Flood_EN_Interface import *
from EN_Interface.BankfullAtCS_EN_Interface import *
from EN_Interface.FloatEuclideanAllocation_EN_Interface import *
from EN_Interface.GaussianSmooth_EN_Interface import *
from EN_Interface.LinearInterpolation_EN_Interface import *
from EN_Interface.RiverWidth_EN_Interface import *
from EN_Interface.WidthWatershed_EN_Interface import *
from EN_Interface.ResampleFlood_EN_Interface import *
from EN_Interface.BridgeCorrection_EN_Interface import *



class Toolbox(object):
    def __init__(self):

        self.label = "Extract rivers characteristics"
        self.alias = ""



        self.tools = [FlowLength, Breach, Slope, FromPoints, CS, OrientedCS, Flood, BinaryRivers, FastBankfullAtCS, FloatEuclidean, GaussianSmooth, LinearInterpolation, RiverWidth, WidthWatershed, ResampleFlood, BridgeCorrection]



