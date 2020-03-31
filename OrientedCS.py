# coding: latin-1

#####################################################
# Gu�nol� Chon�
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Mars 2017 - Cr�ation
# v1.1 - Juillet 2018 - S�paration de l'interface et du m�tier, s�paration de la cr�ation des points et de l'orientation
#  des sections transversales, correction d'un bug lorsque la variance est nulle
# v1.2 - Aout 2018 - Bog apr�s les confluences corrig�

import arcpy
import numpy
from RasterIO import *


class pointflowpath:
   pass


def execute_orientedCS(r_flowdir, str_frompoints, str_ptscs, smoothingdistance, str_cs, messages, language = "FR"):

    # Chargement des fichiers
    flowdir = RasterIO(r_flowdir)

    arcpy.env.extent = r_flowdir
    arcpy.env.snapRaster = r_flowdir
    randomname = binascii.hexlify(os.urandom(6))
    temp_cs2 = arcpy.env.scratchWorkspace + "\\" + randomname
    arcpy.PointToRaster_conversion(str_ptscs, arcpy.Describe(str_ptscs).OIDFieldName, temp_cs2, cellsize=r_flowdir)
    temprastercs = RasterIO(arcpy.Raster(temp_cs2))
    Result = RasterIO(r_flowdir, str_cs, float, -255)

    # D�compte du nombre de points de d�part pour configurer de la barre de progression
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, "OID@")
    count = 0
    for frompoint in frompointcursor:
        count += 1
    progtext = "Calcul de l'orientation des sections transversales"
    if language == "EN":
        progtext = "Processing"
    arcpy.SetProgressor("step", progtext, 0, count, 1)
    progres = 0

    # Traitement effectu� pour chaque point de d�part
    frompointcursor = arcpy.da.SearchCursor(str_frompoints, "SHAPE@")
    for frompoint in frompointcursor:
        # Mise � jour de la barre de progression
        arcpy.SetProgressorPosition(progres)
        progres += 1

        # On prend l'objet g�om�trique (le point) associ� � la ligne dans la table
        frompointshape = frompoint[0].firstPoint

        # Conversion des coordonn�es
        currentcol = flowdir.XtoCol(frompointshape.X)
        currentrow = flowdir.YtoRow(frompointshape.Y)

        # Tests de s�curit� pour s'assurer que le point de d�part est � l'int�rieurs des rasters
        intheraster = True
        if currentcol<0 or currentcol>=flowdir.raster.width or currentrow<0 or currentrow>= flowdir.raster.height:
            intheraster = False
        elif (flowdir.getValue(currentrow, currentcol) <> 1 and flowdir.getValue(currentrow, currentcol) <> 2 and
                      flowdir.getValue(currentrow, currentcol) <> 4 and flowdir.getValue(currentrow, currentcol) <> 8 and
                      flowdir.getValue(currentrow, currentcol) <> 16 and flowdir.getValue(currentrow, currentcol) <> 32 and
                      flowdir.getValue(currentrow, currentcol) <> 64 and flowdir.getValue(currentrow, currentcol) <> 128):
            intheraster = False


        totaldistance = 0
        currentdistance = 0
        confluencedist = 0
        listpointsflowpath = []
        afterconfluence = False
        # Traitement effectu� sur chaque cellule le long de l'�coulement
        while (intheraster):

            # On stock diff�rentes informations sur le point dans listpointsflowpath
            currentpoint = pointflowpath()
            currentpoint.row = currentrow
            currentpoint.col = currentcol
            currentpoint.X = flowdir.ColtoX(currentcol)
            currentpoint.Y = flowdir.RowtoY(currentrow)
            currentpoint.addeddistance = currentdistance
            totaldistance = totaldistance + currentdistance
            currentpoint.distance = totaldistance
            listpointsflowpath.append(currentpoint)


            # Les points trait� sont mis � -999 (cela permet la d�tection des confluences)
            if not afterconfluence:
                Result.setValue(currentrow, currentcol, -999)


            # On cherche le prochain point � partir du flow direction
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

            # Tests de s�curit� pour s'assurer que l'on ne sorte pas des rasters
            if currentcol < 0 or currentcol >= flowdir.raster.width or currentrow < 0 or currentrow >= flowdir.raster.height:
                intheraster = False
            elif (flowdir.getValue(currentrow, currentcol) <> 1 and flowdir.getValue(currentrow, currentcol) <> 2 and
                          flowdir.getValue(currentrow, currentcol) <> 4 and flowdir.getValue(currentrow, currentcol) <> 8 and
                          flowdir.getValue(currentrow, currentcol) <> 16 and flowdir.getValue(currentrow, currentcol) <> 32 and
                          flowdir.getValue(currentrow, currentcol) <> 64 and flowdir.getValue(currentrow, currentcol) <> 128):
                intheraster = False

            if intheraster:
                if (Result.getValue(currentrow, currentcol) <> Result.nodata):
                    # Atteinte d'un point d�j� trait�
                    if confluencedist == 0:
                        confluencedist = totaldistance + currentdistance
                        afterconfluence = True

                    # On continue encore sur la moiti� de la distance de calcul de la pente apr�s le confluent
                    if (totaldistance + currentdistance - confluencedist) > smoothingdistance/2:
                        intheraster = False



        currentpointnumber = 0


        # Traitement effectu� sur la liste des points le long de l'�coulement
        while (currentpointnumber < len(listpointsflowpath)):

            currentpoint = listpointsflowpath[currentpointnumber]

            if temprastercs.getValue(currentpoint.row, currentpoint.col) <> temprastercs.nodata:
                # Point pour lequel on doit calculer l'orientation de la section transversale


                listXforregression = []
                listYforregression = []
                listXforregression.append(currentpoint.X)
                listYforregression.append(currentpoint.Y)
                distancefromcurrentpoint = 0
                nbcellsfromcurrentpoint = 0
                try:
                    # on ajoute dans listpointforregression les points situ�s avant le point courant, jusqu'� la distance souhait�e
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
                    # on ajoute �galement les points situ� apr�s le point courant, jusqu'� la distance souhait�e
                    while (distancefromcurrentpoint < smoothingdistance / 2):
                        nbcellsfromcurrentpoint = nbcellsfromcurrentpoint + 1
                        distancefromcurrentpoint = distancefromcurrentpoint + listpointsflowpath[
                            currentpointnumber + nbcellsfromcurrentpoint].addeddistance
                        listXforregression.append(listpointsflowpath[currentpointnumber + nbcellsfromcurrentpoint].X)
                        listYforregression.append(
                            listpointsflowpath[currentpointnumber + nbcellsfromcurrentpoint].Y)

                    # Variance et covariance prises avec 0 degr�s de libert�
                    varx = numpy.var(listXforregression)
                    vary = numpy.var(listYforregression)
                    covarxy = numpy.cov(listXforregression, listYforregression, bias=True)[0][1]

                    slope = 0

                    if (covarxy <> 0 and varx > 0 and vary > 0):
                        # Formule pour la r�gression par axe majeur : Legendre et Legendre, 1998, Numerical Ecology, 2�me �dition (p.507)
                        slope = (vary-varx+math.sqrt((vary-varx)**2+4*covarxy**2))/(2*covarxy)
                        angle = math.atan2(slope, 1)
                        # angle perpendiculaire � l'�coulement:
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
                            # on compare l'�volution en x et en y entre le premier et le dernier point
                            if (listXforregression[0]-listXforregression[-1])>(listYforregression[0]-listYforregression[-1]):
                                angle = math.pi/2
                            else:
                                angle = 0

                    Result.setValue(currentpoint.row, currentpoint.col, angle)


                except IndexError:
                    pass



            currentpointnumber = currentpointnumber + 1


    Result.save()
    # On supprime les -999 du r�sultat final
    raster_res = arcpy.sa.SetNull(str_cs, str_cs, "VALUE = -999")
    raster_res.save(str_cs)

    # On supprime le fichier temporaire
    arcpy.Delete_management(temp_cs2)

    return