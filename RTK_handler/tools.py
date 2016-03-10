import os
import sys
import pickle
import subprocess

def print_help():
    print('\nUsage: RTK-handler opt\n\nopt-0 : help\nopt-1 : setup\nopt-2 : make-struct\nopt-3 : create-geom\nopt-4 : norm-proj\nopt-5 : FDK-recon\n')


''' Reads from keyboard the RTK-bin absolute path and stores it inside conf.py '''
def setup():
    # Read abs path from stdin
    abs_path = input("Enter your absolute RTK-bin folder path like this: /home/dlessio/RTK-bin\n")

    try:
        print("Testing if path is correct...")
        path = os.path.join(abs_path, 'bin', 'HelloWorld')
        popen = subprocess.Popen(path, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()

        stored = { 'rtk_path' : abs_path }

        # Write this path on file in binary mode, Overwrites the file if it exists.
        f = open("store.pkl", "wb")
        pickle.dump(stored, f)
        f.close()

        print("Cofiguration success!")

    except:
        print("Error on RTK-bin path, cannot execute the HelloWorld binary.")
        sys.exit(1)


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
