#!/usr/bin/env python3
import unittest, sys
import importlib

sys.path.append('../runtime-terror/Tsuro/Common')

from board import Board
from tiles import BoardTile, HandTile, Tile
from avatar import Avatar
from rulechecker import RuleChecker

class TestClient(unittest.TestCase):

    def test_check_player_color(self):
        rule_checker = RuleChecker()
        valid_colors = ['white', 'black', 'red', 'green', 'blue']

        for color in valid_colors:
             self.assertAlmostEqual(rule_checker.check_player_color(color), True)

        self.assertAlmostEqual(rule_checker.check_player_color("orange"), False)

    def test_valid_starting_port(self):
        rc = RuleChecker()

        coordinate = "a1"
        port_valid_north = 'n1'
        port_valid_west = 'w1'
        port_invalid = 's2'
        port_invalid_side = 'x2'
        port_invalid_space = 'n5'

        self.assertAlmostEqual(rc.valid_starting_port(coordinate, port_valid_north), True)
        self.assertAlmostEqual(rc.valid_starting_port(coordinate, port_valid_west), True)
        self.assertAlmostEqual(rc.valid_starting_port(coordinate, port_invalid), False)
        self.assertAlmostEqual(rc.valid_starting_port(coordinate, port_invalid_side), False)
        self.assertAlmostEqual(rc.valid_starting_port(coordinate, port_invalid_space), False)

    def test_check_player_dead(self):
        rule_checker = RuleChecker()
        board = Board()
        player = Avatar('green')
        tile_1 = HandTile([('n1', 's2'), ('n2', 'e2'), ('e1', 'w2'), ('s1', 'w1')])
        tile_2 = HandTile([('n1', 'e2'), ('n2', 'w2'), ('e1', 's1'), ('s2', 'w1')])
        
        board.first_turn(player, tile_1, 'a1', 'n1')
        self.assertAlmostEqual(player.current_port, 's2')
        self.assertAlmostEqual(player.current_tile, 'a1')

        self.assertAlmostEqual(rule_checker.check_player_dead(board, tile_2, "a2", player), True)
        self.assertAlmostEqual(rule_checker.check_player_dead(board, tile_1, "a2", player), False)

    def test_check_first_turn(self):
        rc = RuleChecker()
        empty_board = Board()
        player = Avatar("white")
        suicide_tile = HandTile([('s1', 's2'), ('e2', 'e1'), ('n2', 'n1'), ('w1', 'w2')])
        tile = HandTile([('n1', 's2'), ('n2', 'e2'), ('e1', 'w2'), ('s1', 'w1')])

        # Not on edge
        not_the_edge = rc.check_first_turn(empty_board, suicide_tile, "c7", "w2")
        self.assertAlmostEqual(not_the_edge["legal"], False)
        self.assertAlmostEqual(not_the_edge["rules broken"], ["tile placement is not on the board's edge", "starting port is invalid"])

        # No suicides
        suicide_move = rc.check_first_turn(empty_board, suicide_tile, "a1", "n1")
        self.assertAlmostEqual(suicide_move["legal"], False)
        self.assertAlmostEqual(suicide_move["rules broken"], ["tile placement is avoidable suicide"])
        self.assertAlmostEqual(rc.check_first_turn(empty_board, suicide_tile, "a1", "n2")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, suicide_tile, "a1", "w1")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, suicide_tile, "a1", "w2")["legal"], False)

        # No iterior ports allowed
        interior_port_move = rc.check_first_turn(empty_board, suicide_tile, "a1", "e2")
        self.assertAlmostEqual(interior_port_move["legal"], False)
        self.assertAlmostEqual(interior_port_move["rules broken"], ["starting port is invalid"])
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "a1", "n2")["legal"], True)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "a1", "s2")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "a1", "w2")["legal"], True)

        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "a2", "e1")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "a2", "n1")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "a2", "s1")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "a2", "w1")["legal"], True)

        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "b1", "e2")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "b1", "n2")["legal"], True)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "b1", "s2")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "b1", "w2")["legal"], False)


        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "j10", "e2")["legal"], True)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "j10", "n2")["legal"], False)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "j10", "s2")["legal"], True)
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "j10", "w2")["legal"], False)


        empty_board.first_turn(player, tile, "a1", "n1")

        # No neighbors
        placed_on_occupied_spot = rc.check_first_turn(empty_board, tile, "a1", "s2")
        self.assertAlmostEqual(placed_on_occupied_spot["legal"], False)
        self.assertAlmostEqual(placed_on_occupied_spot["rules broken"], ['coordinate is already occupied', 'starting port is invalid', 'tile placement is avoidable suicide'])
        
        placed_tile_with_neighbors = rc.check_first_turn(empty_board, tile, "a1", "s1")
        self.assertAlmostEqual(placed_tile_with_neighbors["legal"], False)
        self.assertAlmostEqual(placed_tile_with_neighbors["rules broken"], ['coordinate is already occupied', 'starting port is invalid', 'tile placement is avoidable suicide'])
        
        self.assertAlmostEqual(rc.check_first_turn(empty_board, tile, "b1", "e2")["legal"], False)

    def test_check_turn(self):
        rc = RuleChecker()
        empty_board = Board()
        player = Avatar("white")
        tile = HandTile([('s1', 'e2'), ('s2', 'w1'), ('e1', 'n2'), ('n1', 'w2')])
        tile_2 = HandTile([('n1', 's2'), ('n2', 'e2'), ('e1', 'w2'), ('s1', 'w1')])
        suicide_tile = HandTile([('n1', 'w1'), ('n2', 'e1'), ('s2', 'e2'), ('s1', 'w2')])

        empty_board.first_turn(player, tile, "a1", "n2")
        self.assertAlmostEqual(player.current_port, "e1")
        self.assertAlmostEqual(player.current_tile, "a1")

        player.tiles = [tile_2, suicide_tile]

        # Tile has to be at the correct coordinate
        self.assertAlmostEqual(rc.check_turn(empty_board, tile_2, "a1", player)["legal"], False)
        self.assertAlmostEqual(rc.check_turn(empty_board, tile_2, "a2", player)["legal"], False)
        self.assertAlmostEqual(rc.check_turn(empty_board, tile_2, "b1", player)["legal"], True)

        # Tile cannot cause a suicide if there are other options
        self.assertAlmostEqual(rc.check_turn(empty_board, suicide_tile, "b1", player)["legal"], False)

        player.tiles = [suicide_tile]

        self.assertAlmostEqual(rc.check_turn(empty_board, suicide_tile, "b1", player)["legal"], True)



if __name__ == '__main__':
    unittest.main()
        
