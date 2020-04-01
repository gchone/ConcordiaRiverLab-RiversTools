# coding: latin-1

#####################################################
# Gu�nol� Chon�
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Cr�ation
# v1.1 - Juillet 2018 - S�paration de l'interface et du m�tier
# v1.2 - D�cembre 2018 - Ajout du workspace

import arcpy
from GaussianSmooth import *


class pointflowpath:
   pass

class GaussianSmooth(object):
    def __init__(self):

        self.label = "Interpolation par moyenne mobile (gaussienne)"
        self.description = "Interpolation des hauteurs plein-bord suivant l'�coulement"
        self.canRunInBackground = False

    def getParameterInfo(self):


        param_flowdir = arcpy.Parameter(
            displayName="Flow direction",
            name="flowdir",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_frompoint = arcpy.Parameter(
            displayName="Points de d�part",
            name="frompoint",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_bkfatcs = arcpy.Parameter(
            displayName="Valeurs � interpoler",
            name="values",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")

        param_sigma = arcpy.Parameter(
            displayName="�cart-type de la courbe gaussienne",
            name="sigma",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param_nbpts = arcpy.Parameter(
            displayName="Taille de fen�tre",
            name="nbpts",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")

        param_interpolatedbkf = arcpy.Parameter(
            displayName="Valeurs interpol�es",
            name="interpolated_values",
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

        param_frompoint.filter.list = ["Point"]
        param_sigma.value = 500
        param_nbpts.value = 10000


        params = [param_flowdir, param_frompoint, param_bkfatcs, param_sigma, param_nbpts, param_interpolatedbkf, param0]


        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):


        # R�cup�ration des param�tres
        str_flowdir = parameters[0].valueAsText
        str_frompoint = parameters[1].valueAsText
        str_bkfatcs = parameters[2].valueAsText
        gaussiansigma =int(parameters[3].valueAsText)
        nbpts = float(parameters[4].valueAsText)
        SaveResult = parameters[5].valueAsText
        arcpy.env.scratchWorkspace = parameters[6].valueAsText
        execute_GaussianSmooth(arcpy.Raster(str_flowdir), str_frompoint, arcpy.Raster(str_bkfatcs), gaussiansigma, nbpts, SaveResult, messages)

        return