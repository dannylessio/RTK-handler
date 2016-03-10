import sys
from .tools import setup, assert_setup
from .tools import make_structure, assert_structure
from .tools import print_help
from .geometry_maker import create_geometry
from .projections_handler import normalize_projections

option = sys.argv[1]

def main():
    if option   == "help":
        print_help()
        sys.exit(0)

    elif option == "setup":
        setup()
        sys.exit(0)

    elif option == "make-structure":
        assert_setup()
        make_structure()
        sys.exit(0)

    elif option == "create-geometry":
        assert_setup()
        assert_structure()
        create_geometry()
        sys.exit(0)

    elif option == "normalize-projections":
        assert_setup()
        assert_structure()
        normalize_projections()
        sys.exit(0)

    else:
        print_help()
        sys.exit(1)
