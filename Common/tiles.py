#!/usr/bin/env python3
from game_constants import NORTH, SOUTH, EAST, WEST

class Tile:
    #TODO : write equivalence function so we can tell if tiles are the same
    # Constructor
    def __init__(self, paths):
        """A tile has four sides: north, south, east, west and eight ports: n1, n2, s1, s2, e1, e2, w1, w2 A tile
        also has four paths, which are tuples of all of the ports (ex. [n1, e2]) they must be pairwise distinct, and
        all ports must be represented in the paths."""
        self.paths = paths #stored as list of tuples [('n1', 'e2'), ('n2', 'w1')]

    def end_of_path(self, starting_port):
        for path in self.paths:
            if starting_port in path:
                path_as_set = set(path)
                path_as_set.remove(starting_port)
                end_port = path_as_set.pop()
                return end_port


class HandTile(Tile):
    conversion_dict_to_num = {
        "s1": 0, "s2": 1, "e2": 2, "e1": 3, "n2": 4, "n1": 5, "w1": 6, "w2": 7
    }
    conversion_dict_to_str = [
        "s1", "s2", "e2", "e1", "n2", "n1", "w1", "w2"
    ]

    # Constructor
    def __init__(self, paths):
        Tile.__init__(self, paths)

    def __rotate_anticlockwise(self):
        num_coords = self.convert_coordinates_to_num()
        rotated_coords = []

        for edge in num_coords:
            rotated_coords.append(self.modulo_rotate(edge))

        str_coords = self.convert_coordinates_to_string(rotated_coords)
        self.paths = str_coords

    def modulo_rotate(self, current_tuple):
        init_increment = 2
        start_node = current_tuple[0] + init_increment
        end_node = current_tuple[1] + init_increment
        return tuple([start_node % 8, end_node % 8])

    def convert_coordinates(self, path_list, conversion_dict):
        new_coords = []

        for edge in path_list:
            node_start = conversion_dict[edge[0]]
            node_end = conversion_dict[edge[1]]
            new_coords.append((node_start, node_end))

        return new_coords

    def convert_coordinates_to_num(self):
        new_coordinates = self.convert_coordinates(self.paths, self.conversion_dict_to_num)
        return new_coordinates

    def convert_coordinates_to_string(self, num_coords):
        str_coords = self.convert_coordinates(num_coords, self.conversion_dict_to_str)
        return str_coords

    def rotate(self, num_of_rotations):
        for num in range(num_of_rotations):
            self.__rotate_anticlockwise()
        return self


class BoardTile(Tile):

    # Neighbor dictionary
    neighbors = {NORTH: None, EAST: None, SOUTH: None, WEST: None}
    # a neighbor can be either another BoardTile, None or EDGE representing the end of the board

    # Constructor
    def __init__(self, paths, neighbors):
        Tile.__init__(self, paths)
        self.neighbors = neighbors

    def set_neighbor(self, side, new_neighbor):
        self.neighbors[side] = new_neighbor

    def __eq__(self, other):
        if not isinstance(other, BoardTile):
            return NotImplemented

        return self.neighbors == other.neighbors and self.paths == other.paths
