"""Maze solving Algorithm

This script aim to find the optimal trajectory towards the goal in 
a finite 2D environment that is closed by obstacles, that's done 
by wavefront algorithm.

This tool accepts (.mat) files

Dependencies: `scipy`, `numpy`, `matplotlib`, `time`

Contains the following primary functions:

    * planner - returns value map and trajectory from map
    * draw_map - draws map & trajectory
    * read_information - gets map & start index from args & terminal
    * print_information - prints value map and trajectory indices
    * main - the main function of the script
"""

#!/usr/bin/env python3

# Read arguments
import argparse
# Read .mat file
import scipy.io 
# Compute 2d array operations
import numpy as np 
# Draw map & trajectory
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
# Calculate algorithm run time
import time

###########################################

# Planner function -> return [value_map, trajectory]
def planner(map: np.ndarray, start_row: int, start_column: int) -> tuple[np.ndarray, list[tuple[int,int]]]:
    # Copy map to not affect the original
    value_map = np.copy(map)
    
    # Step 1: Search of 2 (goal) in map
    end_index = np.where(value_map==2)

    if len(end_index[0]) == 0:
        print("No goal found.")
        return [],[]

    end_row, end_col = end_index[0][0], end_index[1][0]
    end_index = (end_row, end_col)

    # Step 2: Filling matrix
    queue = [end_index]
    visited = [end_index]
    while len(queue) != 0:
        value = queue.pop(0)
        visited.append(value)
        neighbours = get_neighbours(value_map, value, visited, True)
        
        for neighbour in neighbours:
            value_map = filling_neighbours(value_map, value, neighbour[1])
            queue.append(neighbour[1])

    # Set start index (destination)
    start_index = (start_row, start_column)

    # Step 3: Getting trajectory
    queue = [start_index]
    trajectory = [start_index]
    visited = []
    
    value = None
    # Continue until reach to the goal
    while value != end_index:
        value = queue.pop(0)
        visited.append(value)

        # If value is none -> there is no valid trajectory
        if value == None:
            trajectory = []
            break
        
        neighbours = get_neighbours(value_map, value, visited, False) 
        minimum_neighbour = get_minimum_neighbour(neighbours)
        trajectory.append(minimum_neighbour)
        queue.append(minimum_neighbour)

    return value_map, trajectory[:-1]

# Get index of minimum neighbour value
def get_minimum_neighbour(neighbours: list) -> tuple[int,int]:
    """Get index of minimum neighbour value"""
    minimum_index, minimum_value = (0,0), None
    for neighbour in neighbours:
        # Get value & index of neighbour
        value, index = neighbour[0], neighbour[1]
       
        if minimum_value == None:
            minimum_value, minimum_index = value, index
        elif minimum_value > value:
            minimum_value, minimum_index = value, index

    return minimum_index

# Fill neighbour given value of its prev. neighbour        
def filling_neighbours(map: np.ndarray, index: tuple[int,int], neighbour: tuple[int,int]) -> np.ndarray:
    # Update the neighbour value, that is, neighbour = index + 1
    map[neighbour] = map[index] + 1
    return map

# Check if x and y in boundaries of map or not
def check_in_map_boundary(map: np.ndarray, index: tuple[int,int]) -> bool:
    rows, cols = map.shape[0], map.shape[1]

    x, y = index[0], index[1]
    if (x >= 0 and x < rows) and (y >= 0 and y < cols):
        return True
    else:
        return False

# Get Neighbours of specific index
def get_neighbours(map: np.ndarray, index: tuple[int,int], visited: list, fillingOrPath: bool) -> list:
    indices = list() 

    # Priorities : 
    # [upper, Right, Lower, Left, Upper right, lower right, Lower Left, Upper Left]
    indices.append((index[0]-1, index[1]))  # Up
    indices.append((index[0], index[1]+1))  # Right
    indices.append((index[0]+1, index[1]))  # Down
    indices.append((index[0], index[1]-1))  # Left

    indices.append((index[0]-1, index[1]+1))  # Up right
    indices.append((index[0]-1, index[1]-1))  # Up left
    indices.append((index[0]+1, index[1]+1))  # Down right
    indices.append((index[0]+1, index[1]-1))  # Down left

    final = list()
    # Pop the ones (obstacles) & Neighbours that are visited
    for i in indices:
        # Check if neighbour inside the map or not
        if check_in_map_boundary(map,i):
            # Check if we fill map or get trajectory
            if fillingOrPath == True:
                # If filling -> indices of zeros only
                if map[i[0]][i[1]] == 0:
                    if i not in visited:
                        value = map[i[0]][i[1]]
                        final.append((value,i))
            else:
                # If getting trajectory -> indices that hasn't ones (obstacles)
                if map[i[0]][i[1]] != 1:
                    if i not in visited:
                        value = map[i[0]][i[1]]
                        final.append((value,i))

    return final

# Draw map with trajectory from start to the goal
def draw_map(map: np.ndarray, trajectory: list, end_index: tuple[int,int]) -> None:
    # Set trajectory with number 3
    for index in trajectory[:-1]:
        map[index] = 3
    
    # Set trajectory with number 4
    map[end_index] = 4 

    # Define colormap fpr every number (label2rgb)
    label2rgb_cmap = ListedColormap(['#FFFFFF', '#000083', '#80FF80', '#830000', '#0080FF'], N=5)

    # Draw matrix
    fig, ax = plt.subplots()
    ax.imshow(map, cmap=label2rgb_cmap)

    if len(trajectory) == 0:
        ax.set_title("There's no path.")
    else:
        ax.set_title('Trajectory Map')
    
    # Save result image
    fig.savefig('maze.png')
    # Show plot 
    plt.show()

# Print information function
def print_information(value_map: np.ndarray, trajectory: list, taken_time: float):
    # Print map filled with values
    print("value_map = ")
    print(value_map)

    print("") # Space

    # Check if there's possible trajectory or not !
    if len(trajectory) == 0:
        print("There's No Path")
    else:
        # Print trajectory indices
        print("trajectory = ")
        for index in trajectory:
            print(index[0], index[1])

    print(f"Time taken: {taken_time:.5} secs")

# Get arguments from terminal
def get_args() -> tuple[str,str]:
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('maze', metavar='maze', help='Enter the path of the .mat file')
    parser.add_argument('variable', metavar='var', help='Enter the name of variable that contain the map')
    args = parser.parse_args()

    return args.maze, args.variable

# Get input from user
def read_information() -> tuple[np.ndarray, tuple[int,int]]:
    # Read .mat File
    file_path, variable = get_args()
    map_file = scipy.io.loadmat(file_path, mat_dtype=True)
    maze = map_file[variable]

    start_x = int(input("Please, Enter X coord. for start: "))
    start_y = int(input("Please, Enter Y coord. for start: "))

    # Start index of map
    start_index = start_x, start_y

    return maze, start_index

###########################################

def main():
    # Get information from args & terminal
    maze, start_index = read_information()
    
    start_time = time.time()

    # Get value map and trajectory from map
    value_map, trajectory = planner(maze, start_index[0], start_index[1])

    stop_time = time.time()
       
    # Print value map and trajectory indices
    print_information(value_map, trajectory, stop_time - start_time)

    # Draw map & trajectory
    draw_map(maze, trajectory, start_index)



if __name__ == "__main__":
    main()





