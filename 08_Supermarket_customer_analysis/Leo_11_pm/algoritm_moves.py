import operator
import numpy as np

def heuristic(current,target):
    """calculating the estimated distance between the current node and the targeted node
       -> Manhattan Distance"""
    result = (abs(target[0]-current[0]) + abs(target[1]-current[1]))
    return result


def walkable(grid_array):
    """checks if node is on the grid and not an obstacle"""
    
    walkable = []
    for i in range(len(grid_array)):
        for j in range(len(grid_array[0])):
            if grid_array[i, j] == 0:
                walkable.append((i,j))
    return walkable

def get_path_from_finish(current):
    """Traces back the path thourgh parent-nodes"""

    backwards = []
    while current:
        backwards.append(current.location)
        current = current.parent
    backwards.reverse()
    return backwards

def create_neighbours(poss_moves, current_node, finish_node, grid_array, frontier):
    """Creates neighbour-nodes for current node and adds them to the frontier-list"""

    for move in poss_moves:
        node_position = (current_node.location[0] + move[0],
                            current_node.location[1] + move[1])
        if node_position in walkable(grid_array):
            neighbour = Node(parent=current_node,
                            location=node_position,
                            cost=current_node.cost + 1,
                            heur=heuristic(node_position, finish_node.location))
            frontier.append(neighbour)
    return frontier


def find_path(grid_array, start, finish, p_moves):
    """ A*-Algorithm that finds the shortest path between
        given nodes and returns it as list of tuples"""

    start_node = Node(None, start)
    finish_node = Node(None, finish)
    frontier = [start_node]

    while frontier:
        frontier.sort(key=operator.attrgetter('f_value'))
        current_node = frontier[0]
        frontier.pop(0)

        if current_node.location != finish_node.location:
            frontier = create_neighbours(p_moves, current_node, finish_node, grid_array, frontier)
        else:
            shortest_path = get_path_from_finish(current_node)
            return shortest_path

class Node():
    """Class for the nodes of a pathfinding grid"""

    def __init__(self, parent, location, cost=0, heur=0):
        self.parent = parent
        self.location = location
        self.cost = cost  # distance from start-node (cost)
        self.heur = heur  # approx. distance to goal-node
        self.f_value = self.cost + self.heur  # sum of cost and heuristic value

#if __name__ == '__main__':
grid = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1]
    ])

    # y,x positions
start_given = (2,2)
finish_given = (10,10)
possible_moves = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
path = find_path(grid, start_given, finish_given, possible_moves)
print(path)

##########################################################################################################


fuits = [(2,14),(2,15),(3,14),(3,15),(4,14),(4,15),(5,14),(5,15),(6,14),(6,15)]
spices =[(2,10),(2,11),(3,10),(3,11),(4,10),(4,11),(5,10),(5,11),(6,10),(6,11)]
drinks =[(2,6),(2,7),(3,6),(3,7),(4,6),(4,7),(5,6),(5,7),(6,6),(6,7)]
dairy =[(2,2),(2,3),(3,2),(3,3),(4,2),(4,3),(5,2),(5,3),(6,2),(6,3)]
checkout =[(8,2),(8,3),(9,2),(9,3),(8,6),(8,7),(9,6),(9,7),(8,10),(8,11),(9,10),(9,11)]
entrance = [(7,14),(7,15),(8,14),(8,15),(9,14),(9,15),(10,14),(10,15)]
