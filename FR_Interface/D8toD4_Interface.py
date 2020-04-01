# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Création
# v1.1 - Avril 2020 - Séparation de l'interface et du métier


from D8toD4 import *

class D8toD4(object):
    def __init__(self):

        self.label = "D4 flow direction"
        self.description = "Transforme un flow direction D8 et D4 le long des écoulements"
        self.canRunInBackground = False


    def getParameterInfo(self):

        param_flowdir = arcpy.Parameter(
            displayName="Flow direction",
            name="flowdir",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_dem = arcpy.Parameter(
            displayName="MNE",
            name="dem",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_frompoint = arcpy.Parameter(
            displayName="Points de départ",
            name="frompoint",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_d4fd = arcpy.Parameter(
            displayName="Flow direction corrigé",
            name="d4fd",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Output")





        params = [param_flowdir, param_dem, param_frompoint, param_d4fd]

        return params

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):

        # Récupération des paramètres
        str_flowdir = parameters[0].valueAsText
        str_dem = parameters[1].valueAsText
        str_frompoint = parameters[2].valueAsText
        SaveResult = parameters[3].valueAsText

        execute_D8toD4(arcpy.Raster(str_flowdir), arcpy.Raster(str_dem), str_frompoint, SaveResult, messages)

        return