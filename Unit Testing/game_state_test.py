#!/usr/bin/env python3
import unittest, sys
import importlib
sys.path.append('../runtime-terror/Tsuro/Common')
from game_state import GameState
from board import Board
from tiles import BoardTile, HandTile, Tile

class TestClient(unittest.TestCase):
    
    def test_player_first_turn(self):
        game_state = GameState()

        # should succeed
        success_result = game_state.player_first_turn("white", 1, 0, "a1", "n1")
        self.assertAlmostEqual(success_result["legal"], True)
        self.assertAlmostEqual(success_result["rules broken"], None)

        # should fail
        failure_result = game_state.player_first_turn("blue", 1, 90, "a2", "w2")
        self.assertAlmostEqual(failure_result["legal"], False)
        self.assertAlmostEqual(failure_result["rules broken"], ["tile placement has neighbors"])
        
    def test_player_take_turn(self):
        game_state = GameState()

        # should succeed
        game_state.player_first_turn("white", 1, 0, "a1", "n1")
        game_state.player_first_turn("blue", 1, 0, "g1", "n2")

        # should succeed
        success_result = game_state.player_take_turn("white", 1, 0, "a2", [1, 2])
        self.assertAlmostEqual(success_result["legal"], True)
        self.assertAlmostEqual(len(success_result["players killed"]), 0)        

        # should fail
        failure_result = game_state.player_take_turn("blue", 2, 0, "a2", [2, 3])
        self.assertAlmostEqual(failure_result["legal"], False)
        self.assertAlmostEqual(len(failure_result["rules broken"]), 2)
        self.assertAlmostEqual(failure_result["rules broken"], ['coordinate is already occupied', 'tile placement is not in front of given player'])  

        failure_result = game_state.player_take_turn("blue", 2, 0, "j4", [2, 4])
        self.assertAlmostEqual(failure_result["legal"], False)
        self.assertAlmostEqual(len(failure_result["rules broken"]), 1)
        self.assertAlmostEqual(failure_result["rules broken"], ['tile placement is not in front of given player'])  

if __name__ == '__main__':
    unittest.main()
