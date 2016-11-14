import SimpleITK
import sys
import os
import glob
import pyexcel
from .projection import Projection
from .csv_handler import CsvHandler

class ProjectionsHandler(object):
    def normalize_mha(self):
        inputPath = os.path.join('projections', 'non_normalized', 'mha')
        output_path = os.path.join(
                'projections',
                'normalized',
                'mha',
                'normalized.mha')

        # Getting MHA name
        path = os.path.join(inputPath, '*.mha')
        listOfMHANames = glob.glob(path)

        # Find it
        if len(listOfMHANames) > 1:
            print("Error, more than one .mha file is present")
            sys.exit()
        else:
            mhaPath = listOfMHANames[0]
            print("\nFound .mha image inside: " + mhaPath)

        # Getting a list of projection objects from csv file
        csvFolder = os.path.join('csv')
        csvHandler = CsvHandler()
        listOfProjectionObjects = csvHandler.get_projection_object_list_from_csv(
            csvFolder)

        # Read
        non_normalized_mha = SimpleITK.ReadImage(mhaPath)

        # Create a copy
        normalized_mha = SimpleITK.ReadImage(mhaPath)
        
        # Normalize
        size = list(non_normalized_mha.GetSize())
        zdim = size[2]
        size[2] = 0

        # assert dimension csv and zdim
        if len(listOfProjectionObjects) != zdim:
            print("Error csv dim and proj dime aren't the same.")
            sys.exit()

        for zslice in range(0, zdim):

            print("Normalize projection n " + str(zslice+1))
            index = [0, 0, zslice]

            Extractor = SimpleITK.ExtractImageFilter()
            Extractor.SetSize(size)
            Extractor.SetIndex(index)

            # Extract projection from non_normalized_mha
            image = Extractor.Execute(non_normalized_mha)
                
            # normalize it
            image = image * float(1 / listOfProjectionObjects[zslice].io)
            image = SimpleITK.Log(image)
            image = image * float(-1)

            # convert the 2d slice into a 3d volume slice
            slice_vol = SimpleITK.JoinSeries(image)

            # paste the 3d white slice into the black volume
            normalized_mha = SimpleITK.Paste(normalized_mha, slice_vol, slice_vol.GetSize(), destinationIndex=[0,0,zslice])
        
        SimpleITK.WriteImage(normalized_mha, output_path)
        print(output_path + " successfully writed")
           

def normalize_projections():
    # Create ProjectionsHandler object
    ph = ProjectionsHandler()

    # Perform normalization
    ph.normalize_mha()
