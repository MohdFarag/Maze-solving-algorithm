

# Read arguments
import argparse
# Read .mat file
import scipy.io
# Compute 2d array operations
import numpy as np
from about import description

# Get arguments from terminal
def read_arguments() -> tuple[str,str]:
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('maze_path',
                        metavar='maze_path',
                        help='Enter the path of the (.mat) file')

    parser.add_argument('maze_variable',
                        metavar='var',
                        help='Enter the name of variable that contain the map')

    arguments = parser.parse_args()

    return arguments.maze_path, arguments.maze_variable

def read_mat_file(file_path, variable):
    map_file = scipy.io.loadmat(file_path, mat_dtype=True)
    maze = map_file[variable]

    return maze

# Get inputs from terminal
def read_inputs() -> tuple[str,str]:
    start_x = int(input("Please, Enter X coord. for start: "))
    start_y = int(input("Please, Enter Y coord. for start: "))

    return start_x, start_y

# Get input from user
def read_inputs_from_user() -> tuple[np.ndarray, tuple[int,int]]:
    file_path, variable = read_arguments()

    maze = read_mat_file(file_path, variable)

    start_index = read_inputs()

    return maze, start_index
