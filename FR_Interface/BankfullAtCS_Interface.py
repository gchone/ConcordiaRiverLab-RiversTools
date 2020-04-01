# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# v1.1 - 10 mai 2018 - Correction de la méthode de détection: interpolation linéaire faite entre les segments (
#   NB: erreur de compteur également présent dans la version 1.0)
# v1.2 - 14 mai 2018 - Départ de la détection plein-bord à 50 cm (5 fois l'incrément dans le code). Un départ à 10cm
#   créait un faux plein bord aux premiers 10 cm dans certains cas
# v1.3 - 25 mai 2018 - Optimisation du code
# v1.4 - 05 juillet 2018 - Séparation de l'interface et du code métier
# v1.5 - Décembre 2018 - Ajout du workspace


import arcpy
from BankfullAtCS import *


class FastBankfullAtCS(object):
    def __init__(self):

        self.label = "Élévations plein-bord aux sections transversales"
        self.description = "Détection des élévations plein-bord aux sections transversales"
        self.canRunInBackground = False

    def getParameterInfo(self):


        param_dem = arcpy.Parameter(
            displayName="MNE",
            name="dem",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_cs = arcpy.Parameter(
            displayName="Raster des sections transversales",
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
            displayName="Points de départ",
            name="frompoint",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_p_detect = arcpy.Parameter(
            displayName="p_détect",
            name="p_detect",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param_maxh = arcpy.Parameter(
            displayName="Hauteur plein-bord maximale",
            name="maxh",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param_bkf = arcpy.Parameter(
            displayName="Raster des élévations plein-bord",
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


        # Récupération des paramètres
        str_dem = parameters[0].valueAsText
        str_flowdir = parameters[1].valueAsText
        str_frompoints = parameters[2].valueAsText
        str_cs = parameters[3].valueAsText
        p_detect = float(parameters[4].valueAsText)
        thresholdz = float(parameters[5].valueAsText)
        str_bkf = parameters[6].valueAsText
        arcpy.env.scratchWorkspace = parameters[7].valueAsText
        # Détection par incrément de 10 cm
        increment = 0.1

        execute_BankfullAtCS(arcpy.Raster(str_dem), arcpy.Raster(str_flowdir), str_frompoints, arcpy.Raster(str_cs), p_detect, thresholdz, increment, str_bkf, messages)

        return