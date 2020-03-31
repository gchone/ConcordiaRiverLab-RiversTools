# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Création
# v1.1 - Juin 2018 - Séparation de l'interface et du métier, ajout du traitement étendu après les confluences
# v1.2 - Décembre 2018 - Ajout du workspace
# v1.3 - Décembre 2018 - English version

import arcpy
from FloodAndChannel import *


class BinaryRivers(object):
    def __init__(self):

        self.label = "Chanel detection"
        self.description = "Chanel detection"
        self.canRunInBackground = False

    def getParameterInfo(self):

        param_dem = arcpy.Parameter(
            displayName="DEM",
            name="dem",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_slope = arcpy.Parameter(
            displayName="Slope",
            name="slope",
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
        param_threshold = arcpy.Parameter(
            displayName="Difference of elevation threshold (m)",
            name="thresholdDeltaz",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param_threshold2 = arcpy.Parameter(
            displayName="Slope threshold (degrees)",
            name="thresholdSlope",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param_threshold3 = arcpy.Parameter(
            displayName="Modification threshold (%)",
            name="thresholdGrowth",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")
        param_maxiter = arcpy.Parameter(
            displayName="Maximum number of iterations",
            name="maxiter",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        param_rivers = arcpy.Parameter(
            displayName="Result - Chanel",
            name="rivers",
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

        param_threshold.value = 0.5
        param_threshold2.value = 12
        param_threshold3.value = 5


        params = [param_dem, param_slope, param_flowdir, param_frompoints, param_threshold, param_threshold2, param_threshold3, param_maxiter, param_rivers, param0]

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):

        # Récupération des paramètres
        str_dem = parameters[0].valueAsText
        str_slope = parameters[1].valueAsText
        str_flowdir = parameters[2].valueAsText
        str_frompoints = parameters[3].valueAsText
        threshold_deltaz = float(parameters[4].valueAsText)
        threshold_slope = float(parameters[5].valueAsText)
        threshold_growth = float(parameters[6].valueAsText) / 100
        maxiter_param = parameters[7].valueAsText
        str_output = parameters[8].valueAsText
        arcpy.env.scratchWorkspace = parameters[9].valueAsText
        if maxiter_param is None:
            # Si pas de nombre maximum d'itérations imposé par l'utilisateur, une valeur volontairement excessive est mise
            maxiter = 999999
        else:
            maxiter = int(maxiter_param)

        testedz = arcpy.sa.Plus(str_dem, threshold_deltaz)

        execute_FloodAndChannel(arcpy.Raster(str_dem), testedz, arcpy.Raster(str_flowdir), arcpy.Raster(str_slope),
                                str_frompoints, threshold_slope, threshold_growth, maxiter, str_output, messages, "EN")

        return