# coding: latin-1

#####################################################
# Guénolé Choné
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Création
# v1.1 - Juillet 2018 - Séparation de l'interface et du métier, séparation de la création des points et de l'orientation
#  des sections transversales, correction d'un bug lorsque la variance est nulle
# v1.2 - Aout 2018 - Bog après les confluences corrigé
# v1.3 - Mai 2020 - Coordinate system = dem

import arcpy
import numpy
from RasterIO import *


class pointflowpath:
   pass


def execute_orientedCS(r_flowdir, str_frompoints, str_ptscs, smoothingdistance, str_cs, messages, language = "FR"):

    arcpy.env.outputCoordinateSystem = r_flowdir.spatialReference

    # Chargement des fichiers
    flowdir = RasterIO(r_flowdir)

    arcpy.env.extent = r_flowdir
    arcpy.env.snapRaster = r_flowdir
    randomname = binascii.hexlify(os.urandom(6))
    temp_cs2 = arcpy.env.scratchWorkspace + "\\" + str(randomname)
    arcpy.PointToRaster_conversion(str_ptscs, arcpy.Describe(str_ptscs).OIDFieldName, temp_cs2, cellsize=r_flowdir)
    temprastercs = RasterIO(arcpy.Raster(temp_cs2))
    Result = RasterIO(r_flowdir, str_cs, float, -255)

    # Décompte du nombre de points de départ pour configurer de la barre de progression
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, "OID@")
    count = 0
    for frompoint in frompointcursor:
        count += 1
    progtext = "Calcul de l'orientation des sections transversales"
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

        # Tests de sécurité pour s'assurer que le point de départ est à l'intérieurs des rasters
        intheraster = True
        if currentcol<0 or currentcol>=flowdir.raster.width or currentrow<0 or currentrow>= flowdir.raster.height:
            intheraster = False
        elif (flowdir.getValue(currentrow, currentcol) != 1 and flowdir.getValue(currentrow, currentcol) != 2 and
                      flowdir.getValue(currentrow, currentcol) != 4 and flowdir.getValue(currentrow, currentcol) != 8 and
                      flowdir.getValue(currentrow, currentcol) != 16 and flowdir.getValue(currentrow, currentcol) != 32 and
                      flowdir.getValue(currentrow, currentcol) != 64 and flowdir.getValue(currentrow, currentcol) != 128):
            intheraster = False


        totaldistance = 0
        currentdistance = 0
        confluencedist = 0
        listpointsflowpath = []
        afterconfluence = False
        # Traitement effectué sur chaque cellule le long de l'écoulement
        while (intheraster):

            # On stock différentes informations sur le point dans listpointsflowpath
            currentpoint = pointflowpath()
            currentpoint.row = currentrow
            currentpoint.col = currentcol
            currentpoint.X = flowdir.ColtoX(currentcol)
            currentpoint.Y = flowdir.RowtoY(currentrow)
            currentpoint.addeddistance = currentdistance
            totaldistance = totaldistance + currentdistance
            currentpoint.distance = totaldistance
            listpointsflowpath.append(currentpoint)


            # Les points traité sont mis à -999 (cela permet la détection des confluences)
            if not afterconfluence:
                Result.setValue(currentrow, currentcol, -999)


            # On cherche le prochain point à partir du flow direction
            direction = flowdir.getValue(currentrow, currentcol)
            if (direction == 1):
                currentcol = currentcol + 1
                currentdistance = flowdir.raster.meanCellWidth
            if (direction == 2):
                currentcol = currentcol + 1
                currentrow = currentrow + 1
                currentdistance = math.sqrt(
                    flowdir.raster.meanCellWidth * flowdir.raster.meanCellWidth + flowdir.raster.meanCellHeight * flowdir.raster.meanCellHeight)
            if (direction == 4):
                currentrow = currentrow + 1
                currentdistance = flowdir.raster.meanCellHeight
            if (direction == 8):
                currentcol = currentcol - 1
                currentrow = currentrow + 1
                currentdistance = math.sqrt(
                    flowdir.raster.meanCellWidth * flowdir.raster.meanCellWidth + flowdir.raster.meanCellHeight * flowdir.raster.meanCellHeight)
            if (direction == 16):
                currentcol = currentcol - 1
                currentdistance = flowdir.raster.meanCellWidth
            if (direction == 32):
                currentcol = currentcol - 1
                currentrow = currentrow - 1
                currentdistance = math.sqrt(
                    flowdir.raster.meanCellWidth * flowdir.raster.meanCellWidth + flowdir.raster.meanCellHeight * flowdir.raster.meanCellHeight)
            if (direction == 64):
                currentrow = currentrow - 1
                currentdistance = flowdir.raster.meanCellHeight
            if (direction == 128):
                currentcol = currentcol + 1
                currentrow = currentrow - 1
                currentdistance = math.sqrt(
                    flowdir.raster.meanCellWidth * flowdir.raster.meanCellWidth + flowdir.raster.meanCellHeight * flowdir.raster.meanCellHeight)

            # Tests de sécurité pour s'assurer que l'on ne sorte pas des rasters
            if currentcol < 0 or currentcol >= flowdir.raster.width or currentrow < 0 or currentrow >= flowdir.raster.height:
                intheraster = False
            elif (flowdir.getValue(currentrow, currentcol) != 1 and flowdir.getValue(currentrow, currentcol) != 2 and
                          flowdir.getValue(currentrow, currentcol) != 4 and flowdir.getValue(currentrow, currentcol) != 8 and
                          flowdir.getValue(currentrow, currentcol) != 16 and flowdir.getValue(currentrow, currentcol) != 32 and
                          flowdir.getValue(currentrow, currentcol) != 64 and flowdir.getValue(currentrow, currentcol) != 128):
                intheraster = False

            if intheraster:
                if (Result.getValue(currentrow, currentcol) != Result.nodata):
                    # Atteinte d'un point déjà traité
                    if confluencedist == 0:
                        confluencedist = totaldistance + currentdistance
                        afterconfluence = True

                    # On continue encore sur la moitié de la distance de calcul de la pente après le confluent
                    if (totaldistance + currentdistance - confluencedist) > smoothingdistance/2:
                        intheraster = False



        currentpointnumber = 0


        # Traitement effectué sur la liste des points le long de l'écoulement
        while (currentpointnumber < len(listpointsflowpath)):

            currentpoint = listpointsflowpath[currentpointnumber]

            if temprastercs.getValue(currentpoint.row, currentpoint.col) != temprastercs.nodata:
                # Point pour lequel on doit calculer l'orientation de la section transversale


                listXforregression = []
                listYforregression = []
                listXforregression.append(currentpoint.X)
                listYforregression.append(currentpoint.Y)
                distancefromcurrentpoint = 0
                nbcellsfromcurrentpoint = 0
                try:
                    # on ajoute dans listpointforregression les points situés avant le point courant, jusqu'à la distance souhaitée
                    while (distancefromcurrentpoint <= smoothingdistance / 2):
                        nbcellsfromcurrentpoint = nbcellsfromcurrentpoint - 1
                        if (currentpointnumber + nbcellsfromcurrentpoint > 0):
                            distancefromcurrentpoint = distancefromcurrentpoint + listpointsflowpath[
                                currentpointnumber + nbcellsfromcurrentpoint].addeddistance
                            listXforregression.append(
                                listpointsflowpath[currentpointnumber + nbcellsfromcurrentpoint].X)
                            listYforregression.append(
                                listpointsflowpath[currentpointnumber + nbcellsfromcurrentpoint].Y)
                        else:
                            raise IndexError
                    distancefromcurrentpoint = 0
                    nbcellsfromcurrentpoint = 0
                    # on ajoute également les points situé après le point courant, jusqu'à la distance souhaitée
                    while (distancefromcurrentpoint < smoothingdistance / 2):
                        nbcellsfromcurrentpoint = nbcellsfromcurrentpoint + 1
                        distancefromcurrentpoint = distancefromcurrentpoint + listpointsflowpath[
                            currentpointnumber + nbcellsfromcurrentpoint].addeddistance
                        listXforregression.append(listpointsflowpath[currentpointnumber + nbcellsfromcurrentpoint].X)
                        listYforregression.append(
                            listpointsflowpath[currentpointnumber + nbcellsfromcurrentpoint].Y)

                    # Variance et covariance prises avec 0 degrés de liberté
                    varx = numpy.var(listXforregression)
                    vary = numpy.var(listYforregression)
                    covarxy = numpy.cov(listXforregression, listYforregression, bias=True)[0][1]

                    slope = 0

                    if (covarxy != 0 and varx > 0 and vary > 0):
                        # Formule pour la régression par axe majeur : Legendre et Legendre, 1998, Numerical Ecology, 2ème édition (p.507)
                        slope = (vary-varx+math.sqrt((vary-varx)**2+4*covarxy**2))/(2*covarxy)
                        angle = math.atan2(slope, 1)
                        # angle perpendiculaire à l'écoulement:
                        angle = angle + math.pi/2
                        if (angle > math.pi):
                            angle = angle - 2*math.pi
                    else:
                        if varx == 0:
                            angle = 0
                        elif vary == 0:
                            angle = math.pi/2
                        else:
                            # la covariance est nulle
                            # on compare l'évolution en x et en y entre le premier et le dernier point
                            if (listXforregression[0]-listXforregression[-1])>(listYforregression[0]-listYforregression[-1]):
                                angle = math.pi/2
                            else:
                                angle = 0

                    Result.setValue(currentpoint.row, currentpoint.col, angle)


                except IndexError:
                    pass



            currentpointnumber = currentpointnumber + 1


    Result.save()
    # On supprime les -999 du résultat final
    raster_res = arcpy.sa.SetNull(str_cs, str_cs, "VALUE = -999")
    raster_res.save(str_cs)

    # On supprime le fichier temporaire
    arcpy.Delete_management(temp_cs2)

    return