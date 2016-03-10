import sys
from .tools import insert_RTK_path, assert_RTK_path
from .tools import make_structure, assert_structure
from .tools import print_help
from .geometry_maker import create_geometry
from .projections_handler import normalize_projections

# Try to get the first parameter, if it does not exist print_help
try:
    option = sys.argv[1]
except:
    option = sys.argv[0]


def main():
    if option   == "help":
        print_help()
        sys.exit(0)

    elif option == "make-struct":
        make_structure()
        sys.exit(0)

    elif option == "create-geom":
        assert_structure()
        create_geometry()
        sys.exit(0)

    elif option == "norm-proj":
        assert_structure()
        normalize_projections()
        sys.exit(0)

    elif option == "insert-RTK-path":
        insert_RTK_path()
        sys.exit(0)

    else:
        print_help()
        sys.exit(1)
