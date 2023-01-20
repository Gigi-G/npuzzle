# description: This file contains the distance metrics used in the A* algorithm
# author: Seminara Luigi
# date: 2023-01-18
# tags: python, distance, manhattan, euclidean, linear_conflict, misplaced_tiles, linear_manhattan_conflict

import math


def manhattan_distance(point1_x, point1_y, point2_x, point2_y):
    """ 
        It is the sum of absolute values of differences in the point 1's x and y coordinates and the point 2's x and y coordinates respectively 
            @param point1_x: x coordinate of point 1
            @param point1_y: y coordinate of point 1
            @param point2_x: x coordinate of point 2    
    """    
    return abs(point1_x - point2_x) + abs(point1_y-point2_y)



def eculidean_distance(point1_x, point1_y, point2_x, point2_y):
    """ 
        It is the square root of the sum of the squares of the differences in the point 1's x and y 
            @param point1_x: x coordinate of point 1
            @param point1_y: y coordinate of point 1
            @param point2_x: x coordinate of point 2
            @param point2_y: y coordinate of point 2
    """
    return math.sqrt(math.pow(point1_x - point2_x,2) + math.pow(point1_y - point2_y,2))



def linear_conflict_single(state):
    """ 
        It is the sum of the linear conflicts in each row and column 
            @param state: the state of the puzzle
    """
    n = state.n
    config = state.config
    goal = state.goal
    linear_conflicts = 0
    # Linear Conflict in rows
    for i in range(n):
        row = config[i*n:(i+1)*n]
        goal_row = goal[i*n:(i+1)*n]
        for j in range(n):
            if row[j] in goal_row[j+1:]:
                linear_conflicts += 2
    # Linear Conflict in columns
    for i in range(n):
        col = config[i::n]
        goal_col = goal[i::n]
        for j in range(n):
            if col[j] in goal_col[j+1:]:
                linear_conflicts += 2
    return linear_conflicts



def misplaced_tiles(state):
    """ 
        It is the number of tiles that are not in their goal positions
            @param state: the state of the puzzle    
    """
    n = state.n
    config = state.config
    goal = state.goal
    misplaced_tiles = 0
    for i in range(n*n):
        if config[i] != goal[i]:
            misplaced_tiles += 1
    return misplaced_tiles



def manhattan_distance_state(state):
    """ 
        It is the sum of the manhattan distances of each tile from its goal position
            @param state: the state of the puzzle
    """
    distances = 0
    for i, item in enumerate(state.config):
        current_row = i // state.n
        current_col = i % state.n
        goal_idx = state.goal.index(item)
        goal_row = goal_idx // state.n
        goal_col = goal_idx % state.n
        distances += manhattan_distance(current_row, current_col, goal_row, goal_col)
    return distances
    


def linear_manhattan_conflict(state):
    """ 
        It is the sum of the linear conflicts and the manhattan distances of each tile from its goal position
            @param state: the state of the puzzle
    """
    return linear_conflict_single(state) + manhattan_distance_state(state)