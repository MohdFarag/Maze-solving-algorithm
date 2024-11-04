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
# Calculate algorithm run time
import time
# Planner Functions
from planner import planner
# Read Inputs
from input_reader import read_inputs_from_user
# Print Outputs
from output_printer import print_information, draw_map


def main():
    maze, start_index = read_inputs_from_user()

    start_time = time.time()
    value_map, trajectory = planner(maze, start_index[0], start_index[1])
    stop_time = time.time()

    print_information(value_map, trajectory, stop_time - start_time)

    draw_map(maze, trajectory, start_index)


if __name__ == "__main__":
    main()
