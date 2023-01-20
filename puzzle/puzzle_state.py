# description: This file contains the PuzzleState class.
# author: Seminara Luigi
# date: 2023-01-18
# tags: python, puzzle, puzzle_state, puzzle_solver

import time
import resource
import sys
import math

class PuzzleState(object):

    def __init__(self, config, n, goal, cost_function, parent=None, action="Initial", cost=0):
        """ 
            The constructor of the PuzzleState class.

            Args:
                config: this is the configuration of the puzzle.
                n: this is the dimension of the puzzle.
                goal: this is the goal state of the puzzle.
                cost_function: this is the cost function.
                parent: this is the parent of the current state. Defaults to None.
                action: this is the action that led to the current state. Defaults to "Initial".
                cost: this is the cost of the current state. Defaults to 0.
                
            Raises:
                AttributeError: if the length of config is not correct or less than required.
        """
        if n*n != len(config) or n < 2:
            raise AttributeError("The length of config entered is not correct or less than required!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []
        self.goal = goal
        self.cost_function = cost_function

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break



    def get_blank_tile(self):
        """ It returns the position of the blank tile. """
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break
        return self.blank_row, self.blank_col, i



    def display(self):
        """ It displays the current state of the puzzle. """
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)



    def move_left(self):
        """ It moves the blank tile to the left. If it is not possible, it returns None."""
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function, parent=self, action="Left", cost=self.cost + 1)



    def move_right(self):
        """ It moves the blank tile to the right. If it is not possible, it returns None. """
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function, parent=self, action="Right", cost=self.cost + 1)



    def move_up(self):
        """ It moves the blank tile up. If it is not possible, it returns None. """
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function, parent=self, action="Up", cost=self.cost + 1)



    def move_down(self):
        """ It moves the blank tile down. If it is not possible, it returns None. """
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function, parent=self, action="Down", cost=self.cost + 1)



    def expand(self, RLDU=True):
        """
            It expands the node by adding all possible children to the list of children.
            
            Args:
                RLDU: this is the order of the children. Defaults to True.
        """
        if len(self.children) == 0:
            if RLDU:  #RLDU    
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
            else: #UDLR
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)        
        return self.children
                


    def is_goal(self):
        """ It checks if the current state is the goal state. """
        return list(self.config) == self.goal



    def __lt__(self, other):
        """ It compares the cost of two states. Ti is the overloaded less than operator. """
        return self.cost_function(self) < self.cost_function(other)



    def __le__(self, other):
        """ It compares the cost of two states. It is the overloaded less than or equal operator. """
        return self.cost_function(self) <= self.cost_function(other)