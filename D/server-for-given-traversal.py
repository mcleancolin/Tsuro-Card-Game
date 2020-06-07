class Graph:
    """Represents a graph of nodes connected by edges"""
    nodes = set()
    edges = []
    graph = {}

    def __init__(self, nodes):
        self.nodes = nodes
        for node in nodes:
            self.graph[node] = set()

    def can_reach(self, color, node):
        """Determines if node of given color can reach target node"""
        colored_node = self.__find_color(color)
        if not colored_node:
            return False
        visited = set()
        to_check = set([colored_node])
        while len(to_check) > 0:
            curr_node = to_check.pop()
            if curr_node not in visited:
                visited.add(curr_node)
                neighbors = self.graph[curr_node]
                for n in neighbors:
                    if n == node: return True
                    to_check.add(n)
        return False

    def add_edge(self, node1, node2):
        """Adds an edges to the graph between the given nodes"""
        self.graph[node1].add(node2)
        self.graph[node2].add(node1)

    def get_node(self, name):
        """Gets the node from the graph named name"""
        for node in self.graph.keys():
            if node.name == name:
                return node
        return False

    def __find_color(self, color):
        """Finds the node of given color, if it exists in the graph"""
        for node in self.graph.keys():
            if node.color == color:
                return node
        return False

class Node:
    """Represents a colored and named Node"""
    color = ""
    name = ""

    def __init__(self, name):
        self.name = name

    def set_color(self, color):
        """Sets the color of this Node to given color"""
        self.color = color

def add_token(node, color):
    """Adds color to given node"""
    node.set_color(color)
    return node

def new_labrinyth(names):
    "Created a new Graph with nodes of given names"
    nodes = set()
    for name in names:
        nodes.add(Node(name))
    return Graph(nodes)

