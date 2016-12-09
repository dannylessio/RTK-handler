import sys
import argparse
from .tools import insert_RTK_path, assert_RTK_path
from .tools import make_structure, assert_structure, clean_structure
from .tools import rtkfdk_reconstruction
from .geometry_maker import create_geometry
from .projections_handler import normalize_projections


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', action='store_true', default=False,
                        dest='make_structure',
                        help='create the folder structure')

    parser.add_argument('-g', action='store_true', default=False,
                        dest='create_geometry',
                        help='create the XML geometry')

    parser.add_argument(
        '-n',
        action='store_true',
        default=False,
        dest='normalize_projections',
        help='normalize MHA stack')

    parser.add_argument('-r', action='store_true', default=False,
                        dest='rtkfdk_reconstruction',
                        help='reconstruct with rtkfdk')

    parser.add_argument(
        '-c',
        action='store_true',
        default=False,
        dest='clean_structure',
        help='delete the folder structure')

    parser.add_argument('-p', action='store_true', default=False,
                        dest='insert_rtk_path',
                        help='insert RTK-bin folder path')

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 0.2')

    # Print the help if no options are given
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    # If there are some options, parse them
    options = parser.parse_args()

    # Chech if the parsed options are True
    if options.make_structure:
        make_structure()
        sys.exit(0)

    if options.create_geometry:
        assert_structure()
        # assert_csv()
        create_geometry()
        sys.exit(0)

    if options.normalize_projections:
        assert_structure()
        # assert_csv()
        normalize_projections()
        sys.exit(0)

    if options.insert_rtk_path:
        insert_RTK_path()
        sys.exit(0)

    if options.clean_structure:
        assert_structure()
        clean_structure()
        sys.exit(0)

    if options.rtkfdk_reconstruction:
        assert_structure()
        assert_RTK_path()
        # assert_normalized_proj()
        rtkfdk_reconstruction()
        sys.exit(0)

if __name__ == "__main__":
    main()
