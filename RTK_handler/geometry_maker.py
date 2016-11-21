import SimpleRTK
import sys
import os
import glob
from .projection import Projection
from .csv_handler import CsvHandler


class GeometryMaker(object):

    '''
    This class provides a set of instruments to write a .xml geometry for the
    RTK (Reconstruction ToolKit) library starting from a .csv

    This class requires exactly the following folders and file structure:
    .
    ├── csv
    │   └── your_csv_file.csv
    └── geometry

    The RTK geometry.xml file will be saved into the 'geometry' folder.
    '''

    def __init__(self):
        # Detector variables
        self._pixel_size_direction_u = 0
        self._pixel_size_direction_v = 0
        self._source_to_isocenter_distance = 0
        self._source_to_detector_distance = 0

        self._geometry_name = 'geometry.xml'
        self._projectionObjectList = []
        self._rtk_geometry = False
        self._csvh = False

    ' Adds detector informations reading from keyboard '

    def add_detector_info(self):
        try:
            self._pixel_size_direction_u = float(
                input("Insert du: single pixel detector size on u direction (in mm)\n"))

            self._pixel_size_direction_v = float(
                input("Insert dv: single pixel detector size on v direction (in mm)\n"))

            self._source_to_isocenter_distance = float(
                input("Insert sid: source to isocenter distance (in mm)\n"))

            self._source_to_detector_distance = float(
                input("Insert sdd: source to detector distance (in mm)\n"))

        except ValueError:
            print("Error on input format")
            sys.exit()

    ' Get projection object list from csv file '

    def get_projection_object_list(self):
        csvPath = os.path.join('csv')
        self._csvh = CsvHandler()
        self._projectionObjectList = self._csvh.get_projection_object_list_from_csv(
            csvPath)


    ' Uses the SimpleRTK library in order to setting up the geometry '

    def fill_rtk_geometry(self):
        try:
            self._rtk_geometry = SimpleRTK.ThreeDCircularProjectionGeometry()

            for projection in self._projectionObjectList:
                proj_offset_x = - projection.iso_u * self._pixel_size_direction_u
                proj_offset_y = - projection.iso_v * self._pixel_size_direction_v
                # proj_offset_x = 0
                # proj_offset_y = 0

                self._rtk_geometry.AddProjection(
                    self._source_to_isocenter_distance,
                    self._source_to_detector_distance,
                    projection.angle,
                    proj_offset_x,
                    proj_offset_y)
        except:
            print("Error using SimpleRTK.ThreeDCircularProjectionGeometry().")
            sys.exit(1)

    ' Write the geometry object created with SimpleRTK to file '

    def write_geometry_to_file(self):
        if not self._rtk_geometry:
            print("Error, must create a geometry with SimpleRTK first")
            sys.exit(1)

        if not os.path.isdir('geometry'):
            print('Error, \'geometry\' folder does not exist.')
            sys.exit(1)

        try:
            output_path = os.path.join('geometry', self._geometry_name)

            print("Writing geometry to .xml file...")

            geometrywriter = SimpleRTK.ThreeDCircularProjectionGeometryXMLFileWriter()
            geometrywriter.SetFileName(output_path)
            geometrywriter.Execute(self._rtk_geometry)

            print(output_path + " Successfully Writed.\n")
        except:
            print('Error inside write_to_file')
            sys.exit(1)


def create_geometry():
    # Create a GeometryMaker object
    gm = GeometryMaker()

    # Perform creation
    gm.add_detector_info()
    gm.get_projection_object_list()
    gm.fill_rtk_geometry()
    gm.write_geometry_to_file()
