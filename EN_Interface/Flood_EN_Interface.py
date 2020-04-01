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


class Flood(object):
    def __init__(self):

        self.label = "Flood"
        self.description = "Flood a DEM with a given elevation"
        self.canRunInBackground = False


    def getParameterInfo(self):

        param_dem = arcpy.Parameter(
            displayName="DEM",
            name="dem",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_elevation = arcpy.Parameter(
            displayName="Elevation",
            name="elevation",
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
            displayName="Modification threshold (%)",
            name="threshold",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param_maxiter = arcpy.Parameter(
            displayName="Maximum number of iterations",
            name="maxiter",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        param_flood = arcpy.Parameter(
            displayName="Result - Flooded area with elevation",
            name="flood",
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

        param_threshold.value = 5


        params = [param_dem, param_elevation, param_flowdir, param_frompoints, param_threshold, param_maxiter, param_flood, param0]

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
        str_elevation = parameters[1].valueAsText
        str_flowdir = parameters[2].valueAsText
        str_frompoints = parameters[3].valueAsText
        threshold = float(parameters[4].valueAsText) / 100
        maxiter_param = parameters[5].valueAsText
        str_flood = parameters[6].valueAsText
        arcpy.env.scratchWorkspace = parameters[7].valueAsText
        if maxiter_param is None:
            # Si pas de nombre maximum d'itérations imposé par l'utilisateur, une valeur volontairement excessive est mise
            maxiter = 999999
        else:
            maxiter = int(maxiter_param)

        execute_FloodAndChannel(arcpy.Raster(str_dem), arcpy.Raster(str_elevation), arcpy.Raster(str_flowdir), None, str_frompoints,None,threshold, maxiter, str_flood,messages,"EN")

        return