#!/usr/bin/env python3

# To read .mat file
import scipy.io 
# To compute 2d array operations
import numpy as np 
# To Draw map & trajectory
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

###########################################

# Planner matrix -> return [value_map, trajectory]
def planner(map, start_row, start_column):

    map = np.copy(map)
    # Search of 2 (goal) in map
    end_index = np.where(map==2)
    end_row = end_index[0][0]
    end_col = end_index[1][0]
    endIndex = (end_row, end_col)

    # Filling matrix
    queue = [endIndex]
    visited = [endIndex]
    while len(queue) != 0:
        value = queue.pop(0)
        visited.append(value)
        Neighbours = getNeighbours(map, value, visited, True)

        # The Neighbouring cells to the goal that are not obstacles are assigned the value of the goal point + 1
        for Neighbour in Neighbours:
            map = fillingNeighbours(map, value, Neighbour[1])
            queue.append(Neighbour[1])

    # Set start index (destination)
    startIndex = (start_row, start_column)
    value = startIndex

    # Getting trajectory
    queue = [startIndex]
    visited = []
    trajectory = [startIndex]
    # Continue until reach to the goal
    while value != endIndex:
        value = queue.pop(0)
        visited.append(value)

        # If value is none -> there is no valid trajectory
        if value == None:
            trajectory = []
            break

        Neighbours = getNeighbours(map, value, visited, False) 
        minimumNeighbours = getMinimumNeighbours(Neighbours)
        trajectory.append(minimumNeighbours)
        queue.append(minimumNeighbours)

    return map, trajectory[:-1]

# Get index of minimum neighbour value
def getMinimumNeighbours(neighbours):
    minimumIndex = None
    minimumValue = None
    for neighbour in neighbours:
        value = neighbour[0]
        index = neighbour[1]
       
        if minimumValue == None:
            minimumValue = value
            minimumIndex = index
        elif minimumValue > value:
            minimumValue = value
            minimumIndex = index

    return minimumIndex

# Fill neighbour given value of its prev. neighbour        
def fillingNeighbours(map, index, neighbour):
    # Update the goal value, that is, goal = goal + 1
    map[neighbour] = map[index] + 1
    return map

def inMap(map,x,y):
    rows = map.shape[0]
    cols = map.shape[1]

    if (x >= 0 and x < rows) and (y >= 0 and y < cols):
        return True
    else:
        return False

# Get Neighbours of specific index
def getNeighbours(map, index, visited, fillingOrPath):
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
        if inMap(map,i[0],i[1]):
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
def drawMap(map, trajectory, endIndex):
    # Set trajectory with number 3
    for index in trajectory[:-1]:
        map[index] = 3
    
    # Set trajectory with number 4
    map[endIndex] = 4 

    # Define colormap fpr every number (label2rgb)
    label2RgbCmap = ListedColormap(['#FFFFFF', '#000083', '#80FF80', '#830000', '#0080FF'], N=5)

    # Plot matrix
    fig, ax = plt.subplots()
    ax.imshow(map, cmap=label2RgbCmap)
    if len(trajectory) == 0:
        ax.set_title("There's no path.")
    else:
        ax.set_title('Trajectory Map')
    
    # Save result image
    fig.savefig('maze.png')
    # Show plot 
    plt.show()

# Print information function
def printInformation(value_map, trajectory):
    # Print map filled with values
    print("value_map = ")
    print(value_map)

    # Check if there's possible trajectory or not !
    if len(trajectory) == 0:
        print("There's No Path")
    else:
        # Print trajectory indices
        print("trajectory = ")
        for index in trajectory:
            print(index[0], index[1])

###########################################

def main():
    # Read .mat File
    mapFile = scipy.io.loadmat('maze.mat', mat_dtype=True)
    maze = mapFile['map']

    # Start index of map
    startIndex = 45, 4

    # Get value map and trajectory from map
    value_map, trajectory = planner(maze, startIndex[0], startIndex[1])
    
    # Print information
    printInformation(value_map, trajectory)

    # Plot map
    drawMap(maze, trajectory, startIndex)

if __name__ == "__main__":
    main()





