#!/usr/bin/env python3
import unittest, sys
import importlib

sys.path.append('../runtime-terror/Tsuro/Common')

from board import Board
from tiles import HandTile 
from avatar import Avatar
from game_constants import EDGE

class TestClient(unittest.TestCase):

    def test_is_coordinate_occupied(self):
        board = Board()
        hand_tile = HandTile([('s1', 's2'), ('e2', 'e1'), ('n2', 'n1'), ('w1', 'w2')])

        self.assertAlmostEqual(board.is_coordinate_occupied("f4"), False)

        board.place_tile(hand_tile, "f4")

        self.assertAlmostEqual(board.is_coordinate_occupied("f4"), True)

    def test_get_board_coordinate_neighbors(self):
        empty_board = Board()

        a1_neighbors = empty_board.get_board_coordinate_neighbors("a1")
        c4_neighbors = empty_board.get_board_coordinate_neighbors("c4")
        j10_neighbors = empty_board.get_board_coordinate_neighbors("j10")

        self.assertAlmostEqual(a1_neighbors["north"], EDGE)
        self.assertAlmostEqual(a1_neighbors["east"], None)
        self.assertAlmostEqual(a1_neighbors["south"], None)
        self.assertAlmostEqual(a1_neighbors["west"], EDGE)

        self.assertAlmostEqual(c4_neighbors["north"], None)
        self.assertAlmostEqual(c4_neighbors["east"], None)
        self.assertAlmostEqual(c4_neighbors["south"], None)
        self.assertAlmostEqual(c4_neighbors["west"], None)

        self.assertAlmostEqual(j10_neighbors["north"], None)
        self.assertAlmostEqual(j10_neighbors["east"], EDGE)
        self.assertAlmostEqual(j10_neighbors["south"], EDGE)
        self.assertAlmostEqual(j10_neighbors["west"], None)


    def test_convert_to_board_tile(self):
        empty_board = Board()
        hand_tile = HandTile([('s1', 's2'), ('e2', 'e1'), ('n2', 'n1'), ('w1', 'w2')])
        board_tile = empty_board.convert_to_board_tile(hand_tile, "a1")

        self.assertAlmostEqual(board_tile.neighbors["north"], EDGE)
        self.assertAlmostEqual(board_tile.neighbors["east"], None)
        self.assertAlmostEqual(board_tile.neighbors["south"], None)
        self.assertAlmostEqual(board_tile.neighbors["west"], EDGE)

    def test_place_tile(self):
        empty_board = Board()
        hand_tile = HandTile([('s1', 's2'), ('e2', 'e1'), ('n2', 'n1'), ('w1', 'w2')])
        hand_tile_2 = HandTile([('s1', 'e1'), ('s2', 'n2'), ('e2', 'w2'), ('n1', 'w1')])

        self.assertAlmostEqual(len(empty_board.tiles), 0)

        board_tile = empty_board.place_tile(hand_tile, "a1")
        
        self.assertAlmostEqual(len(empty_board.tiles), 1)
        self.assertAlmostEqual(empty_board.tiles["a1"], board_tile)
        self.assertAlmostEqual(board_tile.neighbors["north"], EDGE)
        self.assertAlmostEqual(board_tile.neighbors["east"], None)
        self.assertAlmostEqual(board_tile.neighbors["south"], None)
        self.assertAlmostEqual(board_tile.neighbors["west"], EDGE)

        new_board_tile = empty_board.place_tile(hand_tile_2, "a2")

        self.assertAlmostEqual(len(empty_board.tiles), 2)
        self.assertAlmostEqual(empty_board.tiles["a2"], new_board_tile)
        self.assertAlmostEqual(new_board_tile.neighbors["north"], board_tile)
        self.assertAlmostEqual(new_board_tile.neighbors["east"], None)
        self.assertAlmostEqual(new_board_tile.neighbors["south"], None)
        self.assertAlmostEqual(new_board_tile.neighbors["west"], EDGE)

        self.assertAlmostEqual(board_tile.neighbors["north"], EDGE)
        self.assertAlmostEqual(board_tile.neighbors["east"], None)
        self.assertAlmostEqual(board_tile.neighbors["south"], new_board_tile)
        self.assertAlmostEqual(board_tile.neighbors["west"], EDGE)

    def test_end_of_path(self):
        board = Board()
        hand_tile = HandTile([('s1', 'e2'), ('s2', 'w1'), ('e1', 'n2'), ('n1', 'w2')])
        hand_tile_2 = HandTile([('n1', 'n2'), ('e1', 'w1'), ('e2', 'w2'), ('s2', 's1')])
        
        board.place_tile(hand_tile, "a1")

        self.assertAlmostEqual(board.end_of_path("a1", "n2")["tile"], "a1")
        self.assertAlmostEqual(board.end_of_path("a1", "n2")["port"], "e1")

        board.place_tile(hand_tile_2, "b1")
        
        self.assertAlmostEqual(board.end_of_path("a1", "n2")["tile"], "b1")
        self.assertAlmostEqual(board.end_of_path("a1", "n2")["port"], "e1")
        
        board.place_tile(hand_tile_2, "c1")

        self.assertAlmostEqual(board.end_of_path("a1", "n2")["tile"], "c1")
        self.assertAlmostEqual(board.end_of_path("a1", "n2")["port"], "e1")

        self.assertAlmostEqual(board.end_of_path("a1", "s1")["tile"], "c1")
        self.assertAlmostEqual(board.end_of_path("a1", "s1")["port"], "e2")

        board.place_tile(hand_tile, "d1")

        self.assertAlmostEqual(board.end_of_path("a1", "n2")["tile"], "d1")
        self.assertAlmostEqual(board.end_of_path("a1", "n2")["port"], "s2")

        self.assertAlmostEqual(board.end_of_path("a1", "s1")["tile"], EDGE)
        self.assertAlmostEqual(board.end_of_path("a1", "s1")["port"], EDGE)

    def test_move_player(self):
        board = Board()

    def test_first_turn(self):
        empty_board = Board()
        player = Avatar("white")
        hand_tile = HandTile([('s1', 'e2'), ('s2', 'w1'), ('e1', 'n2'), ('n1', 'w2')])

        self.assertAlmostEqual(player.current_tile, None)
        self.assertAlmostEqual(player.current_port, None)
        self.assertAlmostEqual(len(empty_board.tiles), 0)

        try:
            empty_board.first_turn(player, hand_tile, "a1", "n1")
        except:
            print("Tile choice is suicide")

        empty_board.first_turn(player, hand_tile, "a1", "n2")

        self.assertAlmostEqual(player.current_tile, "a1")
        self.assertAlmostEqual(player.current_port, "e1")
        self.assertAlmostEqual(len(empty_board.tiles), 1)
        self.assertAlmostEqual("a1" in empty_board.tiles, True)
        self.assertAlmostEqual(empty_board.tiles["a1"].paths, hand_tile.paths)

    def test_take_turn(self):
        empty_board = Board()
        player = Avatar("white")
        hand_tile = HandTile([('s1', 'e2'), ('s2', 'w1'), ('e1', 'n2'), ('n1', 'w2')])
        hand_tile_2 = HandTile([('n1', 'n2'), ('e1', 'w1'), ('e2', 'w2'), ('s2', 's1')])

        self.assertAlmostEqual(player.current_tile, None)
        self.assertAlmostEqual(player.current_port, None)
        self.assertAlmostEqual(len(empty_board.tiles), 0)

        empty_board.first_turn(player, hand_tile, "a1", "n2")

        self.assertAlmostEqual(player.current_tile, "a1")
        self.assertAlmostEqual(player.current_port, "e1")
        self.assertAlmostEqual(len(empty_board.tiles), 1)

        try:
            empty_board.take_turn(hand_tile, "a2", player)
        except:
            print("Player has broken the rules")

        empty_board.take_turn(hand_tile_2, "b1", player)

        self.assertAlmostEqual(player.current_tile, "b1")
        self.assertAlmostEqual(player.current_port, "e1")
        self.assertAlmostEqual(len(empty_board.tiles), 2)
        
if __name__ == '__main__':
    unittest.main()