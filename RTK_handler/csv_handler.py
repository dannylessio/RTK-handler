import os
import sys
import glob
import pyexcel
from .projection import Projection


class CsvHandler(object):
    '''
    This class reads a .csv file that contains informations about the acquisition
    of the projections.

    The csv file must be set as follows:
    +-----------+-------+--------+--------+----+
    | proj_name | angle | Niso_u | Niso_v | Io |
    +-----------+-------+--------+--------+----+

    Than it returns a list of Projection objects.
    '''

    def __init__(self):
        self._pyexcel_sheet = False
        self._csv_path = False

    ' Search if a folder contains an unique .csv file, if true returns his path'

    def find_csv_filename(self, folder):
        csvPath = ''
        path = os.path.join(folder, '*.csv')
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

    def get_projection_object_list_from_csv(self, csvFolder):
        self._csv_path = self.find_csv_filename(csvFolder)
        projectionObjectsList = []
        try:
            self._pyexcel_sheet = pyexcel.get_sheet(file_name=self._csv_path)
        except:
            print("Read failed on csv file.")
            sys.exit(1)

        # Create a list of Projection objects
        for row in self._pyexcel_sheet:
            projectionObjectsList.append(
                Projection(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]))

        # Pint how many projections are successfully readed
        print("\nNumber of projections successfully readed: " +
              str(len(projectionObjectsList)) + "\n")

        return projectionObjectsList
