# description: A* search algorithm
# author: Seminara Luigi
# date: 2023-01-18
# tags: python, A*, search, algorithm

import logging
from tqdm import tqdm
from utils.priority_queue import PriorityQueue

def A_STAR(initial_state,heuristic):
    """A * search"""
    frontier = PriorityQueue('min',heuristic)
    frontier.append(initial_state)
    frontier_config = {}
    frontier_config[tuple(initial_state.config)] = True
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0
    log = ""

    def generator():
        while frontier:
            yield

    for _ in tqdm(generator()):
        state = frontier.pop()
        log += "****** State ******\n"
        log = state.display(log)
        explored.add(state)
        if state.is_goal():
            logging.info(log)
            return (state, nodes_expanded, max_search_depth)

        nodes_expanded += 1
        for neigbhor in state.expand(RLDU= False):
            if neigbhor not in explored and tuple(neigbhor.config) not in frontier_config:
                frontier.append(neigbhor)
                frontier_config[tuple(neigbhor.config)] = True
                if neigbhor.cost > max_search_depth:
                    max_search_depth = neigbhor.cost
            elif neigbhor in frontier:
                if heuristic(neigbhor) < frontier[neigbhor]:
                    frontier.__delitem__(neigbhor)
                    frontier.append(neigbhor)
    
    logging.info(log)
    return None