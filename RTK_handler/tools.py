import os
from os.path import expanduser
import sys
import pickle
import subprocess
import shutil

home = expanduser("~")
__pkl_file_path = os.path.join( home, '.RTK_handler.pkl' )

'''
    __path_of contains this folder structure:

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

__path_of = {
    'csv' : os.path.join('csv') ,
    'geometry' : os.path.join('geometry') ,
    'projections' : os.path.join('projections') ,
    'projections_non_normalized' : os.path.join('projections', 'non_normalized') ,
    'projections_non_normalized_mha' : os.path.join('projections', 'non_normalized','mha') ,
    'projections_non_normalized_set_of_tiff' : os.path.join('projections', 'non_normalized','set_of_tiff') ,
    'projections_normalized' : os.path.join('projections', 'normalized') ,
    'projections_normalized_mha' : os.path.join('projections', 'normalized','mha') ,
    'projections_normalized_set_of_tiff' : os.path.join('projections', 'normalized','set_of_tiff') ,
    'reconstructions' : os.path.join('reconstructions') ,
    'reconstructions_from' : os.path.join('reconstructions','from') ,
    'reconstructions_from_mha_normalized_proj' : os.path.join('reconstructions','from','mha_normalized_proj') ,
    'reconstructions_from_tiff_without_norm_proj' : os.path.join('reconstructions','from','tiff_without_norm_proj')
    }

def execute_bin_inside_RTK_bin( command ):
    # pick up the RTK-bin path from pickle
    f = open(__pkl_file_path, "rb")
    readed = pickle.load( f )
    f.close()

    # enter to the bin folder
    rtk_path = readed['rtk_path']
    rtk_bin_path = os.path.join(rtk_path, 'bin')

    # assembly the command
    command_name = command[0]
    full_command = os.path.join(rtk_bin_path, command_name)
    command[0] = full_command

    # execute, wait and print to console
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print( str(output) )


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
        f = open(__pkl_file_path, "wb")
        pickle.dump(stored, f)
        f.close()

        print("Cofiguration success!")

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
        for directory in sorted( __path_of ):
            os.mkdir( __path_of[ directory ] )

        print("Structure created successfully.")

    except:
        print("Error on creating structure.")
        sys.exit(0)

'''
    Check if the folder structure exist
'''
def assert_structure():
    try:
        for directory in sorted( __path_of ):
            if not os.path.exists( __path_of[ directory ] ) :
                raise ValueError( "Directory does not exist" )

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
        __path_of['csv'] ,
        __path_of['geometry'],
        __path_of[ 'projections_non_normalized_mha' ],
        __path_of[ 'reconstructions_from_mha_normalized_proj'] ,
        __path_of['reconstructions_from_tiff_without_norm_proj']
        ]

    for src in srcList:
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.move(full_file_name, dest)

    # delete folders

    shutil.rmtree( __path_of[ 'csv' ] )
    shutil.rmtree( __path_of[ 'geometry' ] )
    shutil.rmtree( __path_of[ 'projections'] )
    shutil.rmtree( __path_of['reconstructions'] )
    print("Structure successfully cleaned.")


def ask_for_projection_source():
    inputString = "Reconstruct from:\n0 : normalized mha\n1 : non-normalized tiff set\n"

    # Get the option
    try:
        source = input(inputString)

        # remember
        if int(source) not in range(0,2):
            raise ValueError

        return source

    except:
        print("Error on input.")

#def assert_projection_source( source ):


def fdk_default_reconstruction( source ):

    # from normalized mha
    if int(source) == 0:
        rootFolder = os.getcwd()

        projections_folder = os.path.join(rootFolder, __path_of['projections_normalized_mha'] )
        projections_name = str( os.listdir( projections_folder )[0] )

        output_path = os.path.join( rootFolder, __path_of['reconstructions_from_mha_normalized_proj'], 'normalized_recon.mha' )

        geometry_path = os.path.join( rootFolder, __path_of['geometry'], 'geometry.xml' )

        spacing_x = str( input( "Insert spacing on x direction\n" ) )
        spacing_y = str( input( "Insert spacing on y direction\n" ) )
        spacing_z = str( input( "Insert spacing on z direction\n" ) )

        dimension_x = str( input( "insert x dimension\n" ) )
        dimension_y = str( input( "insert y dimension\n" ) )
        dimension_z = str( input( "insert z dimension\n" ) )


        #command = 'rtkfdk -p ' + projections_folder + ' -r ' + projections_name + ' -o ' + output_path + ' -g ' + geometry_path + ' --spacing ' + spacing_x + ' ' + spacing_y + ' ' + spacing_z + ' --dimension ' + dimension_x + ' ' + dimension_y + ' ' + dimension_z + ' -v'
        command = [
            'rtkfdk',
            '-p',
            str(projections_folder),
            '-r',
            str(projections_name),
            '-o',
            str(output_path),
            '-g',
            str(geometry_path),
            '--spacing',
            str(spacing_x),
            str(spacing_y),
            str(spacing_z),
            '--dimension',
            str(dimension_x),
            str(dimension_y),
            str(dimension_z),
            '-v'
        ]

        print("Reconstructing and writing...")
        execute_bin_inside_RTK_bin( command )

    # from non-normalized tiff set
    else:
        rootFolder = os.getcwd()

        projections_folder = os.path.join(rootFolder, __path_of['projections_normalized_set_of_tiff'] )

        output_path = os.path.join( rootFolder, __path_of['reconstructions_from_tiff_without_norm_proj'], 'non_norm_tiff_recon.mha' )

        geometry_path = os.path.join( rootFolder, __path_of['geometry'], 'geometry.xml' )

        spacing_x = str( input( "Insert spacing on x direction\n" ) )
        spacing_y = str( input( "Insert spacing on y direction\n" ) )
        spacing_z = str( input( "Insert spacing on z direction\n" ) )

        dimension_x = str( input( "insert x dimension\n" ) )
        dimension_y = str( input( "insert y dimension\n" ) )
        dimension_z = str( input( "insert z dimension\n" ) )


        #command = 'rtkfdk -p ' + projections_folder + ' -r ' + projections_name + ' -o ' + output_path + ' -g ' + geometry_path + ' --spacing ' + spacing_x + ' ' + spacing_y + ' ' + spacing_z + ' --dimension ' + dimension_x + ' ' + dimension_y + ' ' + dimension_z + ' -v'
        command = [
            'rtkfdk',
            '-p',
            str(projections_folder),
            '-r',
            '.*.tiff',
            '-o',
            str(output_path),
            '-g',
            str(geometry_path),
            '--spacing',
            str(spacing_x),
            str(spacing_y),
            str(spacing_z),
            '--dimension',
            str(dimension_x),
            str(dimension_y),
            str(dimension_z),
            '-v'
        ]

        print("Reconstructing and writing...")
        execute_bin_inside_RTK_bin( command )
