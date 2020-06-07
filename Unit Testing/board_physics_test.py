#!/usr/bin/env python3
import unittest, sys
import importlib

sys.path.append('../runtime-terror/Tsuro/Common')

import board_physics
from game_constants import EDGE

class TestClient(unittest.TestCase):

    def test_valid_port(self):
        port_invalid_side = 'x2'
        port_invalid_space = 'n5'
        valid_ports = ['n1', 'n2', 's1', 's2', 'e1', 'e2', 'w1', 'w2']

        for port in valid_ports:
            self.assertAlmostEqual(board_physics.valid_port(port), True)

        self.assertAlmostEqual(board_physics.valid_port(port_invalid_side), False)
        self.assertAlmostEqual(board_physics.valid_port(port_invalid_space), False)

    def test_valid_coordinate(self):
        good_coordinate1 = "a1"
        good_coordinate2 = "b2"
        good_coordinate3 = "h10"
        bad_coordinate_column = "m3"
        bad_coordinate_row = "c11"

        self.assertAlmostEqual(board_physics.valid_coordinate(good_coordinate1), True)
        self.assertAlmostEqual(board_physics.valid_coordinate(good_coordinate2), True)
        self.assertAlmostEqual(board_physics.valid_coordinate(good_coordinate3), True)
        self.assertAlmostEqual(board_physics.valid_coordinate(bad_coordinate_column), False)
        self.assertAlmostEqual(board_physics.valid_coordinate(bad_coordinate_row), False)

    def test_get_opposite_side(self):
        self.assertAlmostEqual(board_physics.get_opposite_side("south"), "north")
        self.assertAlmostEqual(board_physics.get_opposite_side("north"), "south")
        self.assertAlmostEqual(board_physics.get_opposite_side("east"), "west")
        self.assertAlmostEqual(board_physics.get_opposite_side("west"), "east")

    def test_port_to_side(self):
        port1 = 'n1'
        port2 = 's2'
        port3 = 'e1'
        port4 = 'w1'

        self.assertAlmostEqual(board_physics.port_to_side(port1), "north")
        self.assertAlmostEqual(board_physics.port_to_side(port2), "south")
        self.assertAlmostEqual(board_physics.port_to_side(port3), "east")
        self.assertAlmostEqual(board_physics.port_to_side(port4), "west")

    def test_get_connecting_port(self):
        self.assertAlmostEqual(board_physics.get_connecting_port("n1"), "s1")
        self.assertAlmostEqual(board_physics.get_connecting_port("n2"), "s2")
        self.assertAlmostEqual(board_physics.get_connecting_port("s1"), "n1")
        self.assertAlmostEqual(board_physics.get_connecting_port("s2"), "n2")
        self.assertAlmostEqual(board_physics.get_connecting_port("e1"), "w1")
        self.assertAlmostEqual(board_physics.get_connecting_port("e2"), "w2")
        self.assertAlmostEqual(board_physics.get_connecting_port("w1"), "e1")
        self.assertAlmostEqual(board_physics.get_connecting_port("w2"), "e2")
        

    def test_is_edge(self):
        self.assertAlmostEqual(board_physics.is_edge("a1"), True)
        self.assertAlmostEqual(board_physics.is_edge("c1"), True)
        self.assertAlmostEqual(board_physics.is_edge("c4"), False)

    def test_get_coordinate_neighbor(self):
        a1_north = board_physics.get_coordinate_neighbor("a1", "north")
        a1_south = board_physics.get_coordinate_neighbor("a1", "south")
        a1_east = board_physics.get_coordinate_neighbor("a1", "east")
        a1_west = board_physics.get_coordinate_neighbor("a1", "west")
        self.assertAlmostEqual(a1_north, EDGE)
        self.assertAlmostEqual(a1_south, "a2")
        self.assertAlmostEqual(a1_east, "b1")
        self.assertAlmostEqual(a1_west, EDGE)

        f7_north = board_physics.get_coordinate_neighbor("f7", "north")
        f7_south = board_physics.get_coordinate_neighbor("f7", "south")
        f7_east = board_physics.get_coordinate_neighbor("f7", "east")
        f7_west = board_physics.get_coordinate_neighbor("f7", "west")

        self.assertAlmostEqual(f7_north, "f6")
        self.assertAlmostEqual(f7_south, "f8")
        self.assertAlmostEqual(f7_east, "g7")
        self.assertAlmostEqual(f7_west, "e7")


        j10_north = board_physics.get_coordinate_neighbor("j10", "north")
        j10_south = board_physics.get_coordinate_neighbor("j10", "south")
        j10_east = board_physics.get_coordinate_neighbor("j10", "east")
        j10_west = board_physics.get_coordinate_neighbor("j10", "west")

        self.assertAlmostEqual(j10_north, "j9")
        self.assertAlmostEqual(j10_south, EDGE)
        self.assertAlmostEqual(j10_east, EDGE)
        self.assertAlmostEqual(j10_west, "i10")
        
    def test_connecting_coordinate(self):
        self.assertAlmostEqual(board_physics.get_connecting_coordinate("a1", "n2"), EDGE)
        self.assertAlmostEqual(board_physics.get_connecting_coordinate("a1", "s2"), "a2")
        self.assertAlmostEqual(board_physics.get_connecting_coordinate("a1", "e2"), "b1")
        self.assertAlmostEqual(board_physics.get_connecting_coordinate("a1", "w2"), EDGE)

    def test_get_all_edge_coordinates(self):
        north_edge_coordinates = set(["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1", "j1"])
        south_edge_coordinates = set(["a10", "b10", "c10", "d10", "e10", "f10", "g10", "h10", "i10", "j10"])
        west_edge_coordinates = set(["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"])
        east_edge_coordinates = set(["j1", "j2", "j3", "j4", "j5", "j6", "j7", "j8", "j9", "j10"])
        all_edge_coordinates = board_physics.get_all_edge_coordinates()
        
        self.assertAlmostEqual(len(all_edge_coordinates), len(set(all_edge_coordinates)))
        self.assertAlmostEqual(north_edge_coordinates.issubset(set(all_edge_coordinates)), True)
        self.assertAlmostEqual(south_edge_coordinates.issubset(set(all_edge_coordinates)), True)
        self.assertAlmostEqual(west_edge_coordinates.issubset(set(all_edge_coordinates)), True)
        self.assertAlmostEqual(east_edge_coordinates.issubset(set(all_edge_coordinates)), True)

    def test_board_coordinate_to_cardinal(self):
        zero_zero = board_physics.board_coordinate_to_cardinal("a1")
        nine_nine = board_physics.board_coordinate_to_cardinal("j10")
        four_seven = board_physics.board_coordinate_to_cardinal("e8")

        self.assertAlmostEqual(zero_zero, (0, 0))
        self.assertAlmostEqual(nine_nine, (9, 9))
        self.assertAlmostEqual(four_seven, (4, 7))

    def test_cardinal_coordinate_to_board(self):
        a_one = board_physics.cardinal_coordinate_to_board(0, 0)
        j_ten = board_physics.cardinal_coordinate_to_board(9, 9)
        e_eight = board_physics.cardinal_coordinate_to_board(4, 7)

        self.assertAlmostEqual(a_one, "a1")
        self.assertAlmostEqual(j_ten, "j10")
        self.assertAlmostEqual(e_eight, "e8")

    def test_convert_port_string(self):
        convert_port_string = {
            "n1": "A", 
            "n2": "B", 
            "e1": "C", 
            "e2": "D", 
            "s2": "E", 
            "s1": "F", 
            "w2": "G", 
            "w1": "H"
        }

        self.assertAlmostEqual(board_physics.convert_port_string("I"), "invalid port string")
        self.assertAlmostEqual(board_physics.convert_port_string("a"), "invalid port string")
        
        for our_port, alpha_port in convert_port_string.items():
            self.assertAlmostEqual(board_physics.convert_port_string(our_port), alpha_port)
            self.assertAlmostEqual(board_physics.convert_port_string(alpha_port), our_port)

if __name__ == '__main__':
    unittest.main()