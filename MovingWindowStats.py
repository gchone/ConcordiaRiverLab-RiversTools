# coding: latin-1

#####################################################
# Gu�nol� Chon�
# Concordia University
# Geography, Planning and Environment Department
# guenole.chone@concordia.ca
#####################################################

# Versions
# v1.0 - Novembre 2018 - Cr�ation



import arcpy
from RasterIO import *



class pointflowpath:
   pass



def execute_MovingWindowStats(r_flowdir, str_frompoint, r_values, distance, function, SaveResult, messages):


    # Chargement des fichiers
    flowdir = RasterIO(r_flowdir)
    valuesraster = RasterIO(r_values)
    try:
        flowdir.checkMatch(valuesraster)
    except Exception as e:
        messages.addErrorMessage(e.message)

    Result = RasterIO(r_flowdir, SaveResult, float,-255)


    # D�compte du nombre de points de d�part pour configurer de la barre de progression
    count = 0
    frompointcursor = arcpy.da.SearchCursor(str_frompoint, "OID@")
    for frompoint in frompointcursor:
        count += 1
    arcpy.SetProgressor("step", "Lissage par moyenne mobile", 0, count, 1)
    progres = 0

    # Traitement effectu� pour chaque point de d�part
    frompointcursor = arcpy.da.SearchCursor(str_frompoint, ["OID@", "SHAPE@"])
    for frompoint in frompointcursor:
        # Mise � jour de la barre de progression
        arcpy.SetProgressorPosition(progres)
        progres += 1

        # On prend l'objet g�om�trique (le point) associ� � la ligne dans la table
        frompointshape = frompoint[1].firstPoint

        # Conversion des coordonn�es
        currentcol = flowdir.XtoCol(frompointshape.X)
        currentrow = flowdir.YtoRow(frompointshape.Y)

        intheraster = True
        # Tests de s�curit� pour s'assurer que le point de d�part est � l'int�rieurs des rasters
        if currentcol<0 or currentcol>=flowdir.raster.width or currentrow<0 or currentrow>= flowdir.raster.height:
            intheraster = False
        elif (flowdir.getValue(currentrow, currentcol) <> 1 and flowdir.getValue(currentrow, currentcol) <> 2 and
                            flowdir.getValue(currentrow, currentcol) <> 4 and flowdir.getValue(currentrow, currentcol) <> 8 and
                            flowdir.getValue(currentrow, currentcol) <> 16 and flowdir.getValue(currentrow, currentcol) <> 32 and flowdir.getValue(currentrow, currentcol) <> 64 and flowdir.getValue(currentrow, currentcol) <> 128):
            intheraster = False

        listflowpath = []
        listpointsflowpath = []
        listdistance = []
        listelevation = []
        totaldistance = 0
        currentdistance = 0


        # Traitement effectu� sur chaque cellule le long de l'�coulement
        while (intheraster):

            currentpoint = pointflowpath()
            currentpoint.row = currentrow
            currentpoint.col = currentcol
            listpointsflowpath.append(currentpoint)
            totaldistance = totaldistance + currentdistance

            listflowpath.append(totaldistance)

            # On cr�e une liste des points d'�l�vation connue le long de l'�coulement, ainsi qu'une liste associ�e avec leur distance depuis le point de distance
            if valuesraster.getValue(currentrow, currentcol) <> valuesraster.nodata:
                listdistance.append(totaldistance)
                listelevation.append(valuesraster.getValue(currentrow, currentcol))


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
                            flowdir.getValue(currentrow, currentcol) <> 16 and flowdir.getValue(currentrow, currentcol) <> 32 and flowdir.getValue(currentrow, currentcol) <> 64 and flowdir.getValue(currentrow, currentcol) <> 128):
                intheraster = False

            if intheraster:
                if (Result.getValue(currentrow, currentcol) <> -255):
                    intheraster = False

        if len(listdistance) <= 1:
            # Avertissement si il n'y a qu'un seul (ou aucun) point de donn�es
            messages.addWarningMessage("Point source {0}: pas assez de sections transversales".format(frompoint[0]))

        else:

            currentpointnumber = 0
            # Traitement pour chaque point le long de l'�coulement
            while (currentpointnumber < len(listflowpath)):

                currentpoint = listpointsflowpath[currentpointnumber]
                weights = []
                values = []
                sumwgt = 0
                # On parcourt tous les points d'�l�vation connue
                for i in range(len(listdistance)):
                    distlocale = abs(listdistance[i]-listflowpath[currentpointnumber])
                    # ... pour trouver ceux situ�s � l'int�rieur de la fen�tre
                    if distlocale <= distance / 2:
                        values.append(listelevation[i])


                # On calcul la valeur finale � partir des valeurs et des poids associ�s
                finalvalue = function(values)

                Result.setValue(currentpoint.row, currentpoint.col, finalvalue)

                currentpointnumber = currentpointnumber + 1


    Result.save()

    return

class message:
    def addErrorMessage(self, txtmessage):
        print txtmessage
    def addWarningMessage(self, txtmessage):
        print txtmessage

if __name__ == "__main__":
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.overwriteOutput = True
    arcpy.env.scratchWorkspace = r"F:\MSP2\tmp"

    str_frompoint = r"F:\MSP2\Yamaska\demnov18\pointspourmesuresws\frompoint50km.shp"
    r_flowdir =  arcpy.Raster(r"F:\MSP2\Yamaska\demnov18\flowdir")
    r_values = arcpy.Raster(r"F:\MSP2\Yamaska\demnov18\pointspourmesuresws\slope100")
    distance = 500
    SaveResult = r"F:\MSP2\Yamaska\demnov18\pointspourmesuresws\varslope2"


    def stdev(list):
        try:
            mean = 0
            for value in list:
                mean += value
            mean = mean / len(list)
            var = 0
            for value in list:
                var += (value - mean)*(value - mean)
            var = var / len(list)

            return math.sqrt(var)
        except Exception:
            return None

    mymessage = message()
    execute_MovingWindowStats(r_flowdir, str_frompoint, r_values, distance, stdev, SaveResult, mymessage)