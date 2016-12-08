import SimpleITK as sitk
import sys
import os
import glob
from .csv_handler import CsvHandler


class ProjectionsHandler(object):

    def normalize_mha(self):
        inputPath = os.path.join('projections', 'non_normalized')
        output_path = os.path.join(
            'projections',
            'normalized',
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

        # Read the non-normalized Stack
        stack = sitk.ReadImage(mhaPath)

        # Readinfo
        width = stack.GetWidth()
        height = stack.GetHeight()
        depth = stack.GetDepth()

        # list of normalized projections
        norm_proj_list = []

        # assert dimension csv and depth
        if len(listOfProjectionObjects) != depth:
            print("Error csv dim and proj dime aren't the same.")
            sys.exit()

        # Normalize
        for zslice in range(0, depth):

            print("Normalize projection n " + str(zslice + 1))

            extractor = sitk.ExtractImageFilter()
            extractor.SetSize([width, height, 0])
            extractor.SetIndex([0, 0, zslice])

            # Extract a single projection
            proj = extractor.Execute(stack)

            # Normalize it
            proj = proj * float(1 / listOfProjectionObjects[zslice].io)
            proj = sitk.Log(proj)
            proj = proj * float(-1)

            # append it to the list of normalized projections
            norm_proj_list.append(proj)

        # Join normalized projections into a single 3D MHA image
        norm_stack = sitk.JoinSeries(norm_proj_list)

        # Copy the meta-information from original Stack
        norm_stack.CopyInformation(stack)

        # Force Origin to (0,0,0)
        norm_stack.SetOrigin([0, 0, 0])

        # Write it to file
        sitk.WriteImage(norm_stack, output_path)
        print(output_path + " successfully writed")


def normalize_projections():
    # Create ProjectionsHandler object
    ph = ProjectionsHandler()

    # Perform normalization
    ph.normalize_mha()
