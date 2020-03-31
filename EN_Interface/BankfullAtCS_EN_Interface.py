# coding: latin-1

#####################################################
# Gu�nol� Chon�
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# v1.1 - 10 mai 2018 - Correction de la m�thode de d�tection: interpolation lin�aire faite entre les segments (
#   NB: erreur de compteur �galement pr�sent dans la version 1.0)
# v1.2 - 14 mai 2018 - D�part de la d�tection plein-bord � 50 cm (5 fois l'incr�ment dans le code). Un d�part � 10cm
#   cr�ait un faux plein bord aux premiers 10 cm dans certains cas
# v1.3 - 25 mai 2018 - Optimisation du code
# v1.4 - 05 juillet 2018 - S�paration de l'interface et du code m�tier
# v1.5 - D�cembre 2018 - Ajout du workspace
# v1.5 - D�cembre 2018 - Version englaise

import arcpy
from BankfullAtCS import *


class FastBankfullAtCS(object):
    def __init__(self):

        self.label = "Bankfull elevation at cross-sections"
        self.description = "Bankfull elevation at cross-sections"
        self.canRunInBackground = False

    def getParameterInfo(self):


        param_dem = arcpy.Parameter(
            displayName="DEM",
            name="dem",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_cs = arcpy.Parameter(
            displayName="Cross-sections (oriented raster)",
            name="cs",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_flowdir = arcpy.Parameter(
            displayName="Flow direction",
            name="flowdir",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_frompoints = arcpy.Parameter(
            displayName="From points",
            name="frompoint",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_p_detect = arcpy.Parameter(
            displayName="p_detect",
            name="p_detect",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param_maxh = arcpy.Parameter(
            displayName="Maximum bankfull depth",
            name="maxh",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param_bkf = arcpy.Parameter(
            displayName="Result - Bankfull elevation at XS",
            name="bkf",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output")
        param0 = arcpy.Parameter(
            displayName="Workspace",
            name="in_workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        param0.filter.list = ["File System"]
        param0.value = arcpy.env.scratchWorkspace

        param_frompoints.filter.list = ["Point"]
        param_p_detect.value = 0
        param_maxh.value = 6


        params = [param_dem, param_flowdir, param_frompoints, param_cs, param_p_detect, param_maxh ,param_bkf, param0]

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):


        # R�cup�ration des param�tres
        str_dem = parameters[0].valueAsText
        str_flowdir = parameters[1].valueAsText
        str_frompoints = parameters[2].valueAsText
        str_cs = parameters[3].valueAsText
        p_detect = float(parameters[4].valueAsText)
        thresholdz = float(parameters[5].valueAsText)
        str_bkf = parameters[6].valueAsText
        arcpy.env.scratchWorkspace = parameters[7].valueAsText
        # D�tection par incr�ment de 10 cm
        increment = 0.1

        execute_BankfullAtCS(arcpy.Raster(str_dem), arcpy.Raster(str_flowdir), str_frompoints, arcpy.Raster(str_cs), p_detect, thresholdz, increment, str_bkf, messages, "EN")

        return