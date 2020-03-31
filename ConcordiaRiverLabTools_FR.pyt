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

from FR_Interface.FlowLength_Interface import *
from FR_Interface.Breach_Interface import *
from FR_Interface.Slope_Interface import *
from FR_Interface.FromPoints_Interface import *
from FR_Interface.CS_Interface import *
from FR_Interface.OrientedCS_Interface import *
from FR_Interface.ChannelDetector_Interface import *
from FR_Interface.Flood_Interface import *
from FR_Interface.BankfullAtCS_Interface import *
from FR_Interface.FloatEuclideanAllocation_Interface import *
from FR_Interface.GaussianSmooth_Interface import *
from FR_Interface.LinearInterpolation_Interface import *
from FR_Interface.RiverWidth_Interface import *
from FR_Interface.WidthWatershed_Interface import *
from FR_Interface.ResampleFlood_Interface import *
from FR_Interface.BridgeCorrection_Interface import *



class Toolbox(object):
    def __init__(self):

        self.label = "Outils de gestion des rivières"
        self.alias = ""



        self.tools = [FlowLength, Breach, Slope, FromPoints, CS, OrientedCS, Flood, BinaryRivers, FastBankfullAtCS, FloatEuclidean, GaussianSmooth, LinearInterpolation, RiverWidth, WidthWatershed, ResampleFlood, BridgeCorrection]



