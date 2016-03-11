import os
import sys
import pickle
import subprocess
import shutil

def print_help():
    print('\nUsage: RTK-handler opt\n\nopt-0 : help\nopt-1 : make-struct\nopt-2 : create-geom\nopt-3 : norm-proj\nopt-4 : insert-RTK-path\nopt-5 : clean-structure\n')


''' Reads from keyboard the RTK-bin absolute path and stores it inside conf.py '''
def insert_RTK_path():
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
        f = open(".store.pkl", "wb")
        pickle.dump(stored, f)
        f.close()

        print("Cofiguration success!")

    except:
        print("Error on RTK-bin path, cannot execute the HelloWorld binary.")
        sys.exit(1)


def assert_RTK_path():
    try:
        f = open(".store.pkl", "rb")
        f.close()
    except:
        print("Please run the setup option first.\n")
        sys.exit(1)


'''
It creates the following structure:
.
├── csv
├── geometry
├── projections
│   ├── non_normalized
│   │   ├── mha
│   │   └── set_of_tiff
│   └── normalized
│       ├── mha
│       └── set_of_tiff
└── reconstructions
    └── from
        ├── mha_normalized_proj
        └── tif_without_norm_proj
'''
def make_structure():
    try:
        os.mkdir(os.path.join('csv'))
        os.mkdir(os.path.join('geometry'))
        os.mkdir(os.path.join('projections'))
        os.mkdir(os.path.join('projections', 'non_normalized'))
        os.mkdir(os.path.join('projections', 'non_normalized','mha'))
        os.mkdir(os.path.join('projections', 'non_normalized','set_of_tiff'))
        os.mkdir(os.path.join('projections', 'normalized'))
        os.mkdir(os.path.join('projections', 'normalized','mha'))
        os.mkdir(os.path.join('projections', 'normalized','set_of_tiff'))
        os.mkdir(os.path.join('reconstructions'))
        os.mkdir(os.path.join('reconstructions','from'))
        os.mkdir(os.path.join('reconstructions','from','mha_normalized_proj'))
        os.mkdir(os.path.join('reconstructions','from','tiff_without_norm_proj'))
        print("Structure created successfully.")

    except:
        print("Error on creating structure.")
        sys.exit(0)


def assert_structure():
    try:
        if not os.path.exists(os.path.join('csv')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('geometry')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('projections')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('projections', 'non_normalized')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('projections', 'non_normalized','mha')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('projections', 'non_normalized','set_of_tiff')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('projections', 'normalized')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('projections', 'normalized','mha')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('projections', 'normalized','set_of_tiff')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('reconstructions')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('reconstructions','from')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('reconstructions','from','mha_normalized_proj')) :
            raise ValueError("Directory does not exist")
        if not os.path.exists(os.path.join('reconstructions','from','tiff_without_norm_proj')) :
            raise ValueError("Directory does not exist")

    except ValueError as e:
        print(e)
        sys.exit(1)

'''
    Clean the previous generated structure
'''
def clean_structure():

    # copy relevant files inside folders
    dest = os.getcwd()

    srcList = [os.path.join('csv'), os.path.join('geometry'), os.path.join('projections','non_normalized','mha')]

    for src in srcList:
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.move(full_file_name, dest)

    # delete folders
    shutil.rmtree(os.path.join('csv'))
    shutil.rmtree(os.path.join('geometry'))
    shutil.rmtree(os.path.join('projections'))
    shutil.rmtree(os.path.join('reconstructions'))
    print("Structure successfully cleaned.")
