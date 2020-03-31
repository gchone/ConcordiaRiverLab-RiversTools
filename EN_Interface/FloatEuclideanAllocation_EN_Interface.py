# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Juillet 2018 - Création
# v1.1 - Décembre 2018 - English version

import arcpy

class FloatEuclidean(object):
    def __init__(self):

        self.label = "Euclidean Allocation for Float rasters"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):

        param_raster = arcpy.Parameter(
            displayName="Raster",
            name="raster",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")
        param_distance = arcpy.Parameter(
            displayName="Distance",
            name="distance",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")
        param_res = arcpy.Parameter(
            displayName="Result",
            name="result",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output")


        params = [param_raster, param_distance, param_res]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Récupération des paramètres
        str_raster = parameters[0].valueAsText
        distance = parameters[1].valueAsText
        if distance is not None:
            distance = float(distance)
        SaveResult = parameters[2].valueAsText

        # Traitement très court, conservé ici
        result = arcpy.sa.Float(arcpy.sa.EucAllocation(arcpy.sa.Int(arcpy.Raster(str_raster)*1000000),distance))/1000000
        result.save(SaveResult)


        return