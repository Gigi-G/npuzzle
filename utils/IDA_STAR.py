# description: IDA* search algorithm
# author: Seminara Luigi
# date: 2023-01-18
# tags: python, IDA*, search, algorithm

import logging
from tqdm import tqdm

explored = set()
log = ""

def IDA_STAR(initial_state,heuristic):
    """IDA* search"""
    
    global log
    global explored
    
    threshold = heuristic(initial_state)
    
    def generator():
        while True:
            yield
    
    for _ in tqdm(generator()):
        explored.clear()
        result = search(initial_state, heuristic, initial_state.cost, threshold)
        if result[0] == "cutoff":
            threshold = result[1]
        elif result == "failure":
            logging.info(log)
            return None
        else:
            logging.info(log)
            return (result[1], result[2], result[3])
    

def search(state, heuristic, g, threshold, nodes_expanded = 0, max_search_depth = 0):
    global log
    global explored
    
    log += f"****** State with threshold = {threshold}******\n"
    log = state.display(log)
    
    if state.is_goal():
        logging.info(log)
        return ("found", state, nodes_expanded, max_search_depth)
        
    estimated_cost = g + heuristic(state)
    
    if estimated_cost > threshold:
        log += f"Estimated cost = {estimated_cost} > threshold = {threshold}\n"
        log += ("/"*50) + "\n"
        return ("cutoff", estimated_cost)
    
    min = float("inf")
    for neigbhor in state.expand(RLDU = False):
        if neigbhor not in explored:
            explored.add(neigbhor)
            if neigbhor.cost > max_search_depth:
                max_search_depth = neigbhor.cost
            result = search(neigbhor, heuristic, neigbhor.cost, threshold, nodes_expanded+1, max_search_depth)
            if result[0] == "found":
                return result
            elif result[0] == "cutoff":
                if result[1] < min:
                    min = result[1]
        
    if min == float("inf"):
        return "failure"
    return ("cutoff", min)