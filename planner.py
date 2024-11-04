#!/usr/bin/env python3

# Compute 2d array operations
import numpy as np

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
        if value is None:
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
            if fillingOrPath is True:
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