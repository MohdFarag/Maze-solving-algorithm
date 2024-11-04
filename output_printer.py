# Compute 2d array operations
import numpy as np

# Draw map & trajectory
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Define colormap fpr every number (label2rgb)
label2rgb_cmap = ListedColormap(['#FFFFFF', '#000083', '#80FF80', '#830000', '#0080FF'], N=5)
WHITE_COLOR = 0
DARK_BLUE_COLOR = 1
GREEN_COLOR = 2
RED_COLOR = 3
LIGHT_BLUE_COLOR = 4

# Draw map with trajectory from start to the goal
def draw_map(map: np.ndarray, trajectory: list, end_index: tuple[int,int]) -> None:
    for index in trajectory:
        map[index] = RED_COLOR

    map[end_index] = LIGHT_BLUE_COLOR

    # Draw matrix
    fig, ax = plt.subplots()
    ax.imshow(map, cmap=label2rgb_cmap)

    if isThereTrajectory(trajectory):
        ax.set_title('Trajectory Map')
    else:
        ax.set_title("There's no path.")

    # Save result image
    fig.savefig('maze.png')

    # Show plot
    plt.show()

def print_value_map(value_map):
    print("value_map = ")
    print(value_map)

def isThereTrajectory(trajectory: list):
    return len(trajectory) > 0

def print_trajectory(trajectory: list):
    if isThereTrajectory(trajectory):
        print("trajectory = ")

        for index in trajectory:
            print(index[0], index[1])
    else:
        print("There's No Path")



# Print information function
def print_information(value_map: np.ndarray, trajectory: list, taken_time: float):

    print_value_map(value_map)

    print("") # Space

    print_trajectory(trajectory)

    print("") # Space

    print(f"Time taken: {taken_time:.5} secs")
