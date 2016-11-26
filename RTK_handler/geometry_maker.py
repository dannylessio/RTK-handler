import SimpleRTK as srtk
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
        self._Nu
        self._Nv
        self._du
        self._dv

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
            self._du = float(
                input("insert du   - Single pixel length in mm, u dir\n"))

            self._dv = float(
                input("insert dv   - Single pixel length in mm, v dir\n"))

            self._source_to_isocenter_distance = float(
                input("insert SID  - Source to Isocenter Distance, in mm\n"))

            self._source_to_detector_distance = float(
                input("insert SDD  - Source to Detector Distance, in mm\n"))

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
            self._rtk_geometry = srtk.ThreeDCircularProjectionGeometry()

            for projection in self._projectionObjectList:
                # if N_off_u == 0 nothing happens
                proj_offset_x = projection.N_off_u * self._du
                proj_offset_y = projection.N_off_v * self._dv
                
                #proj_offset_x = - projection.iso_u * self._pixel_size_direction_u
                #proj_offset_y = - projection.iso_v * self._pixel_size_direction_v
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

            geometrywriter = srtk.ThreeDCircularProjectionGeometryXMLFileWriter()
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
