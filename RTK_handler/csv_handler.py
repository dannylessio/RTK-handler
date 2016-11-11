import os
import sys
import glob
import pyexcel
from .projection import Projection
from .special_counter import SpecialCounter


class CsvHandler( object ):
    '''
    This class reads a .csv file that contains informations about the acquisition
    of the projections.

    The csv file must be set as follows:
    +-----------+-------+-------+-------+----+
    | proj_name | angle | iso_u | iso_v | Io |
    +-----------+-------+-------+-------+----+

    For example, Row 0 must be like:
    +-----------+---------+---------+---------+----------+
    | 00000.tif | 0       | 479.440 | 290.950 | 1604.774 |
    +-----------+---------+---------+---------+----------+

    Row 1 like:
    +-----------+---------+---------+---------+----------+
    | 00001.tif | 1.800   | 479.440 | 290.950 | 1604.009 |
    +-----------+---------+---------+---------+----------+

    And so on..

    Than it returns a list of objects (from Projection class) having those attributes.
    '''

    def __init__( self ):
        self._pyexcel_sheet = False
        self._csv_path      = False

    ' Search if a folder contains an unique .csv file, if true returns his path'
    def find_csv_filename( self, folder):
        csvPath = ''
        path = os.path.join( folder, '*.csv' )
        listOfCsvNames = glob.glob(path)

        if not listOfCsvNames:
            print("No csv found")
            sys.exit()

        if len(listOfCsvNames) > 1:
            print("Error, more than one csv file is present")
            sys.exit()
        else:
            csvPath = listOfCsvNames[0]
            print("\nFound .csv file inside: " + csvPath)
            return csvPath


    ' Return a list of Projection objection objects readed from csv '
    def get_projection_object_list_from_csv( self, csvFolder):
        self._csv_path = self.find_csv_filename( csvFolder )
        projectionObjectsList = []
        try:
            self._pyexcel_sheet = pyexcel.get_sheet( file_name = self._csv_path )
        except:
            print("Read failed on csv file.")
            sys.exit(1)

        # Create a list of Projection objects
        for row in self._pyexcel_sheet:
            projectionObjectsList.append( Projection( row[0], row[1], row[2], row[3], row[4] ) )

        # Pint how many projections are successfully readed
        print("\nNumber of projections successfully readed: " + str( len( projectionObjectsList ) ) + "\n")

        return projectionObjectsList


    ' Updates the first column of the .csv file with an incremented value'
    def change_projection_names_on_csv( self ):
        if not self._pyexcel_sheet:
            print("Error, pyexcel_sheet is empty")
            sys.exit(1)

        num_rows = self._pyexcel_sheet.number_of_rows()
        counter = SpecialCounter(5)

        for i in range(0, num_rows):
            print("Updating row " + str(i + 1) + " with " + counter.getValue() + ".tiff")
            self._pyexcel_sheet[i, 0] = counter.getValue() + ".tiff"
            counter.increment()

            self._pyexcel_sheet.save_as(self._csv_path)

        print("Changes to " + self._csv_path + " updated successfully.")
        return
