import sys
import pickle

def print_help():
    print('RTK-handler opt\nopt-1 : setup\nopt-2 : make-struct\nopt-3 : create-geom\nopt-4 : norm-proj\nopt-5 : FDK-recon\n')


''' Reads from keyboard the RTK-bin absolute path and stores it inside conf.py '''
def setup():
    # Read abs path from stdin
    abs_path = input("Enter your absolute RTK-bin folder path like this: /home/dlessio/RTK-bin\n")
    stored = { 'rtk_path' : abs_path }

    # Write this path on file in binary mode, Overwrites the file if it exists.
    f = open("store.pkl", "wb")
    pickle.dump(stored, f)
    f.close()

def assert_setup():
    try:
        f = open("store.pkl", "rb")
        f.close()
    except:
        print("Please run the setup option first.\n")
        sys.exit(1)

def make_structure():
    print("making structure")

def assert_structure():
    print("asserting structure")
