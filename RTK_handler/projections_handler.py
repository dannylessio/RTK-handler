import SimpleITK
import sys
import os
import glob
import pyexcel
from .projection import Projection
from .special_counter import SpecialCounter
from .csv_handler import CsvHandler

class ProjectionsHandler( object ):
    '''
    This class can operate inside a single .mha image type,
    It can extract all the slices inside a set of .tiff images
    It can normalize all the extracted images with basic image operations
    It can reassemble the set of .tiff into a single .mha image

    This class requires exactly the following folders and file structure:
    .
    └── projections
        ├── non_normalized
        │   ├── mha
        │   │   └── your_mha_file.mha
        │   └── set_of_tiff
        └── normalized
            ├── mha
            └── set_of_tiff
    '''


    'Given an .mha image it extracts a set of tiff projections'
    def extract_tiff_set_from_non_normalized_mha( self ):
        inputPath = os.path.join('projections','non_normalized','mha')
        outputPath = os.path.join('projections','non_normalized','set_of_tiff','')

        # Getting MHA name
        path = os.path.join(inputPath, '*.mha')
        listOfMHANames = glob.glob(path)

        if len(listOfMHANames) > 1:
            print("Error, more than one .mha file is present")
            sys.exit()
        else:
            mhaPath = listOfMHANames[0]
            print("\nFound .mha image inside: " + mhaPath)

        inputImage = SimpleITK.ReadImage(mhaPath)
        size = list(inputImage.GetSize())
        zdim = size[2]
        size[2] = 0

        counter = SpecialCounter(5)

        for zslice in range(0, zdim):

            index = [0, 0, zslice]

            Extractor = SimpleITK.ExtractImageFilter()
            Extractor.SetSize(size)
            Extractor.SetIndex(index)

            outputImage = outputPath + counter.getValue() + ".tiff"
            SimpleITK.WriteImage(Extractor.Execute(inputImage), outputImage)
            print(outputImage + " successfully writed")
            counter.increment()


    'Given a set of tiff projections, it normalize from a .csv attenuation file'
    def normalize_extracted_tiff_projections( self ):
        inputPath = os.path.join('projections','non_normalized','set_of_tiff','')
        outputPath = os.path.join('projections','normalized','set_of_tiff','')

        # Getting a list of projection objects from csv file
        csvFolder = os.path.join('csv')
        csvHandler = CsvHandler()
        listOfProjectionObjects = csvHandler.get_projection_object_list_from_csv( csvFolder )

        # Normalize images
        for projection in listOfProjectionObjects:
            reader = SimpleITK.ImageFileReader()
            reader.SetFileName(inputPath + projection.name)
            image = reader.Execute()

            # normalize
            image = image * float( 1 / projection.io )
            image = SimpleITK.Log(image)
            image = image * float(-1)

            writer = SimpleITK.ImageFileWriter()
            writer.SetFileName(outputPath + projection.name)
            writer.Execute(image)
            print("normalized " + projection.name + " successfully!")


    'Given a set of tiffs projections, it creates a new .mha image'
    def generate_mha_from_normalized_tiff( self ):
        input_path = os.path.join('projections','normalized','set_of_tiff','')
        output_path = os.path.join('projections','normalized','mha','normalized.mha')

        path = os.path.join(input_path, '*.tiff')

        # create an empty list of names
        listOfImageNames = []
        for filenames in glob.glob(path):
            listOfImageNames.append(filenames)

        # sort it!
        listOfImageNames.sort()

        print("Reading from tif directory:")
        reader = SimpleITK.ImageSeriesReader()

        # set image names into reader object
        reader.SetFileNames(listOfImageNames)

        image = reader.Execute()

        print("Image readed successfully.")

        size = image.GetSize()
        print("Image size:", size[0], size[1], size[2])

        print("Writing image to output path: " + output_path)

        SimpleITK.WriteImage(image, output_path)

        return


def normalize_projections():
    # Create ProjectionsHandler object
    ph = ProjectionsHandler()

    # Perform normalization
    ph.extract_tiff_set_from_non_normalized_mha()
    ph.normalize_extracted_tiff_projections()
    ph.generate_mha_from_normalized_tiff()
