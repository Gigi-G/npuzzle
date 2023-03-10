# description: BA* search algorithm
# author: Seminara Luigi
# date: 2023-01-24
# tags: python, BA*, search, algorithm

import logging
from tqdm import tqdm
from utils.priority_queue import PriorityQueue

def BA_STAR(initial_state, goal_state, heuristic):
    """Bidirectional A* algorithm"""
    # Create the start and goal state priority queues
    start_frontier = PriorityQueue('min',heuristic)
    goal_frontier = PriorityQueue('min',heuristic)
    start_frontier.append(initial_state)
    goal_frontier.append(goal_state)
    start_frontier_config = {}
    goal_frontier_config = {}
    start_frontier_config[tuple(initial_state.config)] = True
    goal_frontier_config[tuple(goal_state.config)] = True
    explored = set()
    nodes_expanded_from_start = 0
    nodes_expanded_from_goal = 0
    max_search_depth_from_start = 0
    max_search_depth_from_goal = 0
    log = ""
    
    def generator():
        while start_frontier and goal_frontier:
            yield

    for _ in tqdm(generator()):
        start_state = start_frontier.pop()
        goal_state = goal_frontier.pop()
        log += "****** Start State ******\n"
        log = start_state.display(log)
        log += "****** Goal State ******\n"
        log = goal_state.display(log)
        explored.add(start_state)
        explored.add(goal_state)
        if start_state.is_goal():
            logging.info(log)
            return (start_state, nodes_expanded_from_start, max_search_depth_from_start)
        if goal_state.is_goal():
            logging.info(log)
            return (goal_state, nodes_expanded_from_goal, max_search_depth_from_goal)
        
        result = start_frontier_direction(start_state, heuristic, start_frontier, goal_frontier, start_frontier_config, goal_frontier_config, explored, nodes_expanded_from_start + 1, max_search_depth_from_goal)
        
        if result[0]:
            max_search_depth = max_search_depth_from_start if max_search_depth_from_start > max_search_depth_from_goal else max_search_depth_from_goal
            logging.info(log)
            return (result[1], result[2], max_search_depth)
        
        nodes_expanded_from_start, max_search_depth_from_start = result[1], result[2]
        
        result = goal_frontier_direction(goal_state, heuristic, start_frontier, goal_frontier, start_frontier_config, goal_frontier_config, explored, nodes_expanded_from_start + 1, max_search_depth_from_goal)
        
        if result[0]:
            max_search_depth = max_search_depth_from_start if max_search_depth_from_start > max_search_depth_from_goal else max_search_depth_from_goal
            logging.info(log)
            return (result[1], result[2], max_search_depth)
        
        nodes_expanded_from_goal, max_search_depth_from_goal = result[1], result[2]
        
    logging.info(log)
    return None



def start_frontier_direction(start_state, heuristic, start_frontier, goal_frontier, start_frontier_config, goal_frontier_config, explored, nodes_expanded, max_search_depth):
    for neighbor in start_state.expand(RLDU= False):
        if neighbor not in explored and tuple(neighbor.config) not in start_frontier_config:
            start_frontier.append(neighbor)
            start_frontier_config[tuple(neighbor.config)] = True
            if neighbor.cost > max_search_depth:
                max_search_depth = neighbor.cost
        elif neighbor in start_frontier:
            if heuristic(neighbor) < start_frontier[neighbor]:
                start_frontier.__delitem__(neighbor)
                start_frontier.append(neighbor)
        elif tuple(neighbor.config) in goal_frontier_config:
            return find_intersection_from_start(neighbor, goal_frontier, explored, nodes_expanded, max_search_depth)
    return (False, nodes_expanded, max_search_depth)



def goal_frontier_direction(goal_state, heuristic, start_frontier, goal_frontier, start_frontier_config, goal_frontier_config, explored, nodes_expanded, max_search_depth):
    for neighbor in goal_state.expand(RLDU= False):
        if neighbor not in explored and tuple(neighbor.config) not in goal_frontier_config:
            goal_frontier.append(neighbor)
            goal_frontier_config[tuple(neighbor.config)] = True
            if neighbor.cost > max_search_depth:
                max_search_depth = neighbor.cost
        elif neighbor in goal_frontier:
            if heuristic(neighbor) < goal_frontier[neighbor]:
                goal_frontier.__delitem__(neighbor)
                goal_frontier.append(neighbor)
        elif tuple(neighbor.config) in start_frontier_config:
            return find_intersection_from_goal(neighbor, start_frontier, explored, nodes_expanded, max_search_depth)
    return (False, nodes_expanded, max_search_depth)



def find_intersection_from_start(neighbor, goal_frontier, explored, nodes_expanded, max_search_depth):
    if neighbor in explored:
        for node in explored:
            if tuple(node.config) == tuple(neighbor.config):
                r = []
                parent = node.parent
                while parent:
                    r.append(parent)
                    parent = parent.parent
                while r[0].parent.config == neighbor.config:
                    neighbor = neighbor.parent
                r[0].parent = neighbor
                for n in r[1:]:
                    n.parent = r[r.index(n)-1]
                for n in r:
                    n.cost = n.parent.cost + 1
                return (True, r[-1], nodes_expanded, max_search_depth)
    
    while goal_frontier:
        node = goal_frontier.pop()
        if tuple(node.config) == tuple(neighbor.config):
            r = []
            parent = node.parent
            while parent:
                r.append(parent)
                parent = parent.parent
            while r[0].parent.config == neighbor.config:
                neighbor = neighbor.parent
            r[0].parent = neighbor
            for n in r[1:]:
                n.parent = r[r.index(n)-1]
            for n in r:
                n.cost = n.parent.cost + 1
            return (True, r[-1], nodes_expanded, max_search_depth)
        return (False, nodes_expanded, max_search_depth)
        
        
        
def find_intersection_from_goal(neighbor, start_frontier, explored, nodes_expanded, max_search_depth):
    if neighbor in explored:
        for node in explored:
            if tuple(node.config) == tuple(neighbor.config):
                r = []
                parent = neighbor.parent
                while parent:
                    r.append(parent)
                    parent = parent.parent
                while r[0].parent.config == neighbor.config:
                    neighbor = neighbor.parent
                r[0].parent = node
                for n in r[1:]:
                    n.parent = r[r.index(n)-1]
                for n in r:
                    n.cost = n.parent.cost + 1
                return (True, r[-1], nodes_expanded, max_search_depth)
         
    while start_frontier:
        node = start_frontier.pop()
        if tuple(node.config) == tuple(neighbor.config):
            r = []
            parent = neighbor.parent
            while parent:
                r.append(parent)
                parent = parent.parent
            while r[0].parent.config == neighbor.config:
                neighbor = neighbor.parent
            r[0].parent = node
            for n in r[1:]:
                n.parent = r[r.index(n)-1]
            for n in r:
                n.cost = n.parent.cost + 1
            return (True, r[-1], nodes_expanded, max_search_depth)
    return (False, nodes_expanded, max_search_depth)