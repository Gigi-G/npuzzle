# description: this file contains the PuzzleSolver class which is responsible for solving the puzzle.
# author: Seminara Luigi
# date: 2023-01-18
# tags: python, puzzle, solver, BFS, DFS, A*

from utils.distance_metrics import manhattan_distance, eculidean_distance, linear_conflict_single, misplaced_tiles, linear_manhattan_conflict
from utils.BFS import BFS
from utils.DFS import DFS
from utils.A_STAR import A_STAR
from utils.IDA_STAR import IDA_STAR
from puzzle.puzzle_state import PuzzleState
import math
import time
import resource

class PuzzleSolver(object):

    def __init__(self, initial_state, goal, algorithm='BFS', heuristic= None):
        """ The constructor of the PuzzleSolver class.

            Args:
                initial_state: this is the initial state of the puzzle.
                goal: this is the goal state of the puzzle.
                algorithm: this is the search algorithm. Defaults to 'BFS'.
                heuristic: this is the heuristics. Defaults to None.

            Raises:
                NotImplementedError: if the algorithm or heuristic is not supported.
                AttributeError: if the heuristic is not provided in case of using A* Search.
        """
        # Assign the initial state of the puzzle.
        self.initial_state = initial_state

        # Assign the search algorithm that will be used in the solver.
        self.set_algorithm(algorithm)

        # Assign the heuristic algorithm that will be used in the solver.
        self.assign_heuristic(heuristic, algorithm)

        # Create a Puzzle State Object with the inputs for Solver.
        initial_state = tuple(map(int, initial_state))
        size = int(math.sqrt(len(initial_state)))
        self.puzzle_state = PuzzleState(initial_state, size, goal, self.calculate_total_cost)



    def set_algorithm(self, algorithm):
        """
            Set the search algorithm that will be used in the solver.

            Args:
                algorithm: this is the search algorithm.
        """
        if(algorithm == 'BFS'): 
            self.search_alg = BFS
        elif(algorithm == 'DFS'):
            self.search_alg = DFS
        elif(algorithm == 'A*'):
            self.search_alg = A_STAR
        elif(algorithm == 'IDA*'):
            self.search_alg = IDA_STAR
        else:
            raise NotImplementedError("No such algorithm is supported.")



    def assign_heuristic(self, heuristic, algorithm):
        """
            Assign the heuristic algorithm that will be used in the solver.
            
            Args:
                heuristic: this is the heuristic algorithm.
                algorithm: this is the search algorithm.
            
            Raises:
                NotImplementedError: if the heuristic is not supported.
                AttributeError: if the heuristic is not provided in case of using A* Search.
        """
        if(heuristic == None and (algorithm == 'A*' or algorithm == 'IDA*')):
            raise AttributeError("Required Attribute `heuristic` in case of useing A* Search.")
        
        elif(heuristic == 'manhattan_distance'):
            self.dist_metric = manhattan_distance
        
        elif(heuristic == 'euclidean_distance'):
            self.dist_metric = eculidean_distance
        
        elif(heuristic == 'linear_conflict'):
            self.dist_metric = linear_conflict_single
        
        elif(heuristic == 'misplaced_tiles'):
            self.dist_metric = misplaced_tiles
        
        elif(heuristic == 'linear_manhattan_conflict'):
            self.dist_metric = linear_manhattan_conflict
            
        elif(heuristic == None and algorithm != 'A*' and algorithm != 'IDA*'):
            pass
        
        else:
            raise NotImplementedError("No such Heuristic is supported.")
 
 
    
    def calculate_total_cost(self, state):
        """
            Calculate the total estimated cost of a state.
        
            Args:
                state: this is the state of the puzzle.
        """
        sum_heuristic = 0
        if self.dist_metric == manhattan_distance or self.dist_metric == eculidean_distance:
            for i, item in enumerate(state.config):
                current_row = i // state.n
                current_col = i % state.n
                goal_idx = state.goal.index(item)
                goal_row = goal_idx // state.n
                goal_col = goal_idx % state.n
                sum_heuristic += self.dist_metric(current_row,current_col,goal_row,goal_col)
            
        else:
            sum_heuristic = self.dist_metric(state)
        return sum_heuristic + state.cost



    def writeOutput(self, result, running_time, ram_usage):
        """
            Write the output of the solver to a file.

            Args:
                result: this is the result of the search algorithm.
                running_time: this is the running time of the search algorithm.
                ram_usage: this is the ram usage of the search algorithm.

            Returns:
                list: path to reach the goal state.
        """
        final_state, nodes_expanded, max_search_depth = result
        path_to_goal = [final_state.action]
        parent_to_goal = [final_state]
        cost_of_path = final_state.cost
        parent_state = final_state.parent

        # Get the path of the actions to reach the goal state.
        while parent_state:
            if parent_state.parent:
                parent_to_goal.append(parent_state)
                path_to_goal.append(parent_state.action)
            parent_state = parent_state.parent
        path_to_goal.reverse()
        parent_to_goal.reverse()
        search_depth = len(path_to_goal)

        # Write the path of the state puzzle.
        print("\n\n\n")
        print("-"*50)
        print("******* Results *******")
        
        path = []
        for state in parent_to_goal:
            print("Action: " + str(state.action))
            state.display()
            config = state.config
            matrix = []
            n = int(math.sqrt(len(config)))
            for i in range(n):
                line = []
                offset = i * n
                for j in range(n):
                    line.append(config[offset + j])
                matrix.append(line)
            path.append(matrix)
        print("-"*50)
            
        # Write all the results.
        print("path_to_goal: " + str(path_to_goal) + "\n")
        print("cost_of_path: " + str(cost_of_path) +  "\n")
        print("nodes_expanded: " + str(nodes_expanded) + "\n")
        print("search_depth: " + str(search_depth) + "\n")
        print("max_search_depth: " + str(max_search_depth) +  "\n")
        print("running_time: " + str(running_time) + "\n")
        print("max_ram_usage: " + str(ram_usage) + "\n")
        
        return path



    def solve(self):
        """
            It solves the puzzle using the search algorithm and the heuristic algorithm.
            
            Returns:
                list: path to reach the goal state.
        """
        # Start the timer.
        start_time = time.time()
        
        # Get the initial memory usage.
        mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        
        # Run the search algorithm.
        if(self.search_alg == A_STAR):
            results = A_STAR(self.puzzle_state, self.calculate_total_cost)
        elif(self.search_alg == IDA_STAR):
            results = IDA_STAR(self.puzzle_state, self.calculate_total_cost)
        else: 
            results = self.search_alg(self.puzzle_state)
        
        # Get the final time.
        running_time = time.time() - start_time
        
        # Get the final memory usage.
        mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        ram_usage = (mem_final - mem_init) / 1024
        
        # Return the path to reach the goal state.
        return self.writeOutput(results, running_time, ram_usage)
 