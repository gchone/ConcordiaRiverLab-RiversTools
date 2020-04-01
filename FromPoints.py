# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Création
# v1.1 - Juin 2018 - Séparation de l'interface et du métier

import arcpy


def execute_FromPoints(flowacc, area_threshold, str_frompoints, messages, language = "FR"):



    # Calcul du seuil pour les points de départ sur le raster "flow accumulation"
    flowacc_threshold = area_threshold * 1000 * 1000 / (flowacc.meanCellWidth * flowacc.meanCellHeight)
    # Création du raster des cours d'eau
    binrivers = arcpy.sa.SetNull(flowacc, 1, "VALUE < " + str(flowacc_threshold))

    # Calcul du nombre de pixels voisines étant des cours d'eau
    nbvoisins = arcpy.sa.FocalStatistics(binrivers, arcpy.sa.NbrRectangle(3,3,"CELL"), "SUM", "")

    # On ne garde que les extrémités (1 voisin, donc nbvoisin = 2)
    extremities = arcpy.sa.SetNull(nbvoisins, binrivers, "VALUE <> 2")

    # On supprime les points situés sur le bord (exutoires de la zone modélisée)
    noborders = arcpy.sa.FocalStatistics(flowacc, arcpy.sa.NbrRectangle(3, 3, "CELL"), "SUM", "NODATA")
    borders = arcpy.sa.IsNull(noborders)
    frompoints = arcpy.sa.SetNull(borders, extremities, "VALUE = 1")

    # On convertit le raster en shapefile
    arcpy.RasterToPoint_conversion(frompoints, str_frompoints)



    return
