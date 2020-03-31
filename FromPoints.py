# coding: latin-1

#####################################################
# Gu�nol� Chon�
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Cr�ation
# v1.1 - Juin 2018 - S�paration de l'interface et du m�tier

import arcpy


def execute_FromPoints(flowacc, area_threshold, str_frompoints, messages, language = "FR"):



    # Calcul du seuil pour les points de d�part sur le raster "flow accumulation"
    flowacc_threshold = area_threshold * 1000 * 1000 / (flowacc.meanCellWidth * flowacc.meanCellHeight)
    # Cr�ation du raster des cours d'eau
    binrivers = arcpy.sa.SetNull(flowacc, 1, "VALUE < " + str(flowacc_threshold))

    # Calcul du nombre de pixels voisines �tant des cours d'eau
    nbvoisins = arcpy.sa.FocalStatistics(binrivers, arcpy.sa.NbrRectangle(3,3,"CELL"), "SUM", "")

    # On ne garde que les extr�mit�s (1 voisin, donc nbvoisin = 2)
    extremities = arcpy.sa.SetNull(nbvoisins, binrivers, "VALUE <> 2")

    # On supprime les points situ�s sur le bord (exutoires de la zone mod�lis�e)
    noborders = arcpy.sa.FocalStatistics(flowacc, arcpy.sa.NbrRectangle(3, 3, "CELL"), "SUM", "NODATA")
    borders = arcpy.sa.IsNull(noborders)
    frompoints = arcpy.sa.SetNull(borders, extremities, "VALUE = 1")

    # On convertit le raster en shapefile
    arcpy.RasterToPoint_conversion(frompoints, str_frompoints)



    return
