# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Avril 2017 - Création
# v1.1 - Juillet 2018 - Séparation de l'interface et du métier, ajout du calcul en étoile (sections non-orientées),
#  découplage de la résolution des rasters.

import arcpy
from RasterIO import *


def execute_RiverWith(r_binary, r_flowdir, str_frompoints, r_cs, oriented, str_width, messages, language = "FR"):




    # Chargement des fichiers
    binary = RasterIO(r_binary)
    flowdir = RasterIO(r_flowdir)
    cs = RasterIO(r_cs)
    try:
        flowdir.checkMatch(cs)
    except Exception as e:
        messages.addErrorMessage(e.message)

    Result = RasterIO(r_flowdir, str_width, float,-255)

    # Décompte du nombre de points de départ pour configurer de la barre de progression
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, "OID@")
    count = 0
    for frompoint in frompointcursor:
        count += 1

    progtext = "Calcul de la largeur aux sections transversales"
    if language == "EN":
        progtext = "Processing"
    arcpy.SetProgressor("step", progtext, 0, count, 1)
    progres = 0

    # Traitement effectué pour chaque point de départ
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, "SHAPE@")
    for frompoint in frompointcursor:
        # Mise à jour de la barre de progression
        arcpy.SetProgressorPosition(progres)
        progres += 1

        # On prend l'objet géométrique (le point) associé à la ligne dans la table
        frompointshape = frompoint[0].firstPoint

        # Conversion des coordonnées
        currentcol = flowdir.XtoCol(frompointshape.X)
        currentrow = flowdir.YtoRow(frompointshape.Y)

        intheraster = True
        # Tests de sécurité pour s'assurer que le point de départ est à l'intérieurs des rasters
        if currentcol<0 or currentcol>=flowdir.raster.width or currentrow<0 or currentrow>= flowdir.raster.height:
            intheraster = False
        elif (flowdir.getValue(currentrow, currentcol) != 1 and flowdir.getValue(currentrow, currentcol) != 2 and
                      flowdir.getValue(currentrow, currentcol) != 4 and flowdir.getValue(currentrow, currentcol) != 8 and
                      flowdir.getValue(currentrow, currentcol) != 16 and flowdir.getValue(currentrow, currentcol) != 32 and
                      flowdir.getValue(currentrow, currentcol) != 64 and flowdir.getValue(currentrow, currentcol) != 128):
            intheraster = False

        # Traitement effectué sur chaque cellule le long de l'écoulement
        while (intheraster):

            # On se reprojète dans le système de coordonnées du raster binary
            colbinary = binary.XtoCol(flowdir.ColtoX(currentcol))
            rowbinary = binary.YtoRow(flowdir.RowtoY(currentrow))

            angle = cs.getValue(currentrow,currentcol)
            if angle != cs.nodata:

                if oriented:
                    # calcul de la ligne et de la colonne du prochain point dans l'axe de la section transversale
                    if (angle > math.pi / 4 and angle < 3 * math.pi / 4):
                        rowinc = -1
                        colinc = math.cos(angle)
                    else:
                        colinc = 1
                        rowinc = -math.sin(angle)
                    if angle > 3 * math.pi / 4:
                        rowinc = -rowinc

                    step = 0

                    while binary.getValue(rowbinary + int(rowinc*step),colbinary + int(colinc*step)) != binary.nodata:
                        step += 1

                    # on répète les opérations précédentes en progressant dans l'autre sens le long de la section transversale
                    step2 = 0


                    while binary.getValue(rowbinary - int(rowinc*step2), colbinary - int(colinc*step2)) != binary.nodata:
                        step2 += 1

                    # if the process was not interrupted because an edge was reached
                    if (rowbinary + int(rowinc * step)) >= 0 and (colbinary + int(colinc * step)) >= 0 and (
                                rowbinary - int(rowinc * step2)) >= 0 and (colbinary - int(colinc * step2)) and (
                                rowbinary + int(rowinc * step)) < binary.raster.height and (colbinary + int(colinc * step)) < binary.raster.width and (
                                rowbinary - int(rowinc * step2)) < binary.raster.height and (colbinary - int(colinc * step2)) < binary.raster.width:

                        basedist = math.sqrt((rowinc*binary.raster.meanCellHeight)**2 + (colinc*binary.raster.meanCellWidth)**2)

                        width = basedist*(step + step2)
                        Result.setValue(currentrow,currentcol,width)

                else:
                    # on teste la largeur sur une étoile à 16 branches et on prend le minimum
                    minwidth = None
                    for star_i in range(1,9):
                        step = 0
                        step2 = 0
                        if star_i == 1:
                            rowinc = 0
                            colinc = 1
                        if star_i == 2:
                            rowinc = step%2
                            colinc = 1
                        if star_i == 3:
                            rowinc = 1
                            colinc = 1
                        if star_i == 4:
                            rowinc = 1
                            colinc = step%2
                        if star_i == 5:
                            rowinc = 1
                            colinc = 0
                        if star_i == 6:
                            rowinc = 1
                            colinc = -step%2
                        if star_i == 7:
                            rowinc = 1
                            colinc = -1
                        if star_i == 8:
                            rowinc = step%2
                            colinc = -1

                        while binary.getValue(rowbinary + int(rowinc * step),
                                              colbinary + int(colinc * step)) != binary.nodata:
                            step += 1

                        while binary.getValue(rowbinary - int(rowinc * step2),
                                              colbinary - int(colinc * step2)) != binary.nodata:
                            step2 += 1

                        width = None
                        # if the process was not interrupted because an edge was reached
                        if (rowbinary + int(rowinc * step)) >= 0 and (colbinary + int(colinc * step)) >= 0 and (
                                    rowbinary - int(rowinc * step2)) >= 0 and (colbinary - int(colinc * step2)) and (
                                    rowbinary + int(rowinc * step)) < binary.raster.height and (
                                    colbinary + int(colinc * step)) < binary.raster.width and (
                                    rowbinary - int(rowinc * step2)) < binary.raster.height and (
                                    colbinary - int(colinc * step2)) < binary.raster.width:
                            basedist = math.sqrt((rowinc * binary.raster.meanCellHeight) ** 2 + (
                            colinc * binary.raster.meanCellWidth) ** 2)

                            width = basedist * (step + step2)

                        if minwidth is not None:
                            if width is not None:
                                minwidth = min(minwidth, width)
                        else:
                            minwidth = width

                    if minwidth is not None:
                        Result.setValue(currentrow, currentcol, minwidth)

            # On cherche le prochain point à partir du flow direction
            direction = flowdir.getValue(currentrow, currentcol)
            if (direction == 1):
                currentcol = currentcol + 1

            if (direction == 2):
                currentcol = currentcol + 1
                currentrow = currentrow + 1

            if (direction == 4):
                currentrow = currentrow + 1

            if (direction == 8):
                currentcol = currentcol - 1
                currentrow = currentrow + 1

            if (direction == 16):
                currentcol = currentcol - 1

            if (direction == 32):
                currentcol = currentcol - 1
                currentrow = currentrow - 1

            if (direction == 64):
                currentrow = currentrow - 1

            if (direction == 128):
                currentcol = currentcol + 1
                currentrow = currentrow - 1

            # Tests de sécurité pour s'assurer que l'on ne sorte pas des rasters
            if currentcol < 0 or currentcol >= flowdir.raster.width or currentrow < 0 or currentrow >= flowdir.raster.height:
                intheraster = False
            elif (flowdir.getValue(currentrow, currentcol) != 1 and flowdir.getValue(currentrow, currentcol) != 2 and
                          flowdir.getValue(currentrow, currentcol) != 4 and flowdir.getValue(currentrow, currentcol) != 8 and
                          flowdir.getValue(currentrow, currentcol) != 16 and flowdir.getValue(currentrow, currentcol) != 32 and
                          flowdir.getValue(currentrow, currentcol) != 64 and flowdir.getValue(currentrow, currentcol) != 128):
                intheraster = False

            if intheraster:
                if (Result.getValue(currentrow, currentcol) != -255):
                    # Atteinte d'un confluent
                    intheraster = False



    Result.save()


    return