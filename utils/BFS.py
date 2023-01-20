# description: Breadth First Search Algorith
# author: Seminara Luigi
# date: 2023-01-18
# tags: python, BFS, search, algorithm

import queue

def BFS(initial_state):
    frontier = queue.Queue() 
    frontier.put(initial_state)
    frontier_config = {}
    frontier_config[tuple(initial_state.config)] = True
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while not frontier.empty():
        state = frontier.get()
        print("****** State ******")
        state.display()
        explored.add(state.config)
        if state.is_goal():
            return (state,nodes_expanded,max_search_depth)
        
        nodes_expanded += 1
        for neighbor in state.expand(RLDU = False):
            if neighbor.config not in explored and tuple(neighbor.config) not in frontier_config:   
                frontier.put(neighbor)
                frontier_config[tuple(neighbor.config)] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
    return None