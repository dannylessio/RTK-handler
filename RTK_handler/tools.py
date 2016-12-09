from os.path import expanduser
import os
import sys
import pickle
import subprocess
import shutil

home = expanduser("~")
__pkl_file_path = os.path.join(home, '.RTK_handler.pkl')

'''
    __path_of contains this folder structure:

    .
    ├── csv
    ├── geometry
    ├── projections
    │   ├── non_normalized
    │   └── normalized
    └── reconstructions
        └── rtkfdk
'''

__path_of = {
    'csv': os.path.join('csv'),
    'geometry': os.path.join('geometry'),
    'projections': os.path.join('projections'),
    'projections_non_normalized': os.path.join(
        'projections',
        'non_normalized'),
    'projections_normalized': os.path.join(
        'projections',
        'normalized'),
    'reconstructions': os.path.join('reconstructions'),
    'reconstructions_rtkfdk': os.path.join(
        'reconstructions',
        'rtkfdk'),
}


''' Reads from keyboard the RTK-bin absolute path and stores it inside conf.py '''


def insert_RTK_path():
    # Read abs path from stdin
    abs_path = input(
        "Enter the full RTK-bin path\n")

    try:
        print("Testing if the path is correct...")
        path = os.path.join(abs_path, 'bin', 'HelloWorld')
        popen = subprocess.Popen(path, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()

        stored = {'rtk_path': abs_path}

        # Write this path on file in binary mode, Overwrites the file if it
        # exists.
        f = open(__pkl_file_path, "wb")
        pickle.dump(stored, f)
        f.close()

        print("Configuration success!")

    except:
        print("Error on RTK-bin path, cannot execute the HelloWorld binary.")
        sys.exit(1)


def assert_RTK_path():
    try:
        f = open(__pkl_file_path, "rb")
        f.close()
    except:
        print("Please run the setup option first.\n")
        sys.exit(1)


'''
    Creates the folder structure:
'''


def make_structure():
    try:
        for directory in sorted(__path_of):
            os.mkdir(__path_of[directory])

        print("Structure created successfully.")

    except:
        print("Error on creating structure.")
        sys.exit(0)


'''
    Check if the folder structure exist
'''


def assert_structure():
    try:
        for directory in sorted(__path_of):
            if not os.path.exists(__path_of[directory]):
                raise ValueError("Directory does not exist")

    except ValueError as e:
        print(e)
        sys.exit(1)


'''
    Cleans the folder structure
'''


def clean_structure():

    # copy relevant files inside os.getcwd() folder
    dest = os.getcwd()

    srcList = [
        __path_of['csv'],
        __path_of['geometry'],
        __path_of['projections_non_normalized'],
        __path_of['reconstructions_rtkfdk'],
    ]

    for src in srcList:
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.move(full_file_name, dest)

    # delete folders
    shutil.rmtree(__path_of['csv'])
    shutil.rmtree(__path_of['geometry'])
    shutil.rmtree(__path_of['projections'])
    shutil.rmtree(__path_of['reconstructions'])
    print("Structure successfully cleaned.")


def add_RTK_path_to(command):
    # pick up the RTK-bin path from pickle
    f = open(__pkl_file_path, "rb")
    readed = pickle.load(f)
    f.close()

    # enter to the bin folder
    rtk_path = readed['rtk_path']
    rtk_bin_path = os.path.join(rtk_path, 'bin')

    # assembly the command
    command_name = command[0]
    full_command = os.path.join(rtk_bin_path, command_name)
    command[0] = full_command

    return command


def execute(command):
    # execute, wait and print to console
    popen = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        universal_newlines=True)
    
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line

    popen.stdout.close()
    return_code = popen.wait()

    if return_code:
        raise subprocess.CalledProcessError(return_code, command)


def rtkfdk_reconstruction():

    rootFolder = os.getcwd()

    projections_folder = os.path.join(
        rootFolder, __path_of['projections_normalized'])
    projections_name = str(os.listdir(projections_folder)[0])

    output_path = os.path.join(
        rootFolder,
        __path_of['reconstructions_rtkfdk'],
        'rtkfdk_recon.mha')

    geometry_path = os.path.join(
        rootFolder, __path_of['geometry'], 'geometry.xml')

    spacing_x = str(input("Insert spacing on x direction\n"))
    spacing_y = str(input("Insert spacing on y direction\n"))
    spacing_z = str(input("Insert spacing on z direction\n"))

    dimension_x = str(input("insert x dimension\n"))
    dimension_y = str(input("insert y dimension\n"))
    dimension_z = str(input("insert z dimension\n"))

    command = [
        'rtkfdk',
        '-p',
        str(projections_folder),
        '-r',
        str(projections_name),
        '-g',
        str(geometry_path),
        '-o',
        str(output_path),
        '--dimension',
        str(dimension_x),
        str(dimension_y),
        str(dimension_z),
        '--spacing',
        str(spacing_x),
        str(spacing_y),
        str(spacing_z),
        '-v'
    ]

    # assembly
    command = add_RTK_path_to(command)

    # execute
    for line in execute(command):
        print(line, end="")
