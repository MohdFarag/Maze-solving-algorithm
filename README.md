# Maze Solving Algorithm

## Overview

Project that aim to find the optimal trajectory towards the goal in a finite 2D environment that is closed by obstacles, that's done by wavefront algorithm.

## Dependencies

``` txt
scipy
numpy
matplotlib
```

## Wavefront Algorithm

Given the start point and the goal point, the algorithm is implemented as follows:

1. The goal point is initialized with 2
2. The neighboring cells to the goal that are not obstacles are assigned the value of the goal point + 1
3. Update the goal value, that is, goal = goal + 1 then repeat steps 1 & 2 until all the spaces are filled.
4. The trajectory (shortest distance to the goal) is easily found by taking differences with all neighboring cells, that is, the minimum of the neighboring cells.

## Preview

![alt text](http://url/to/img.png)
