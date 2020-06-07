#!/usr/bin/env python3
import unittest, sys
import importlib
from datetime import datetime
sys.path.append('../runtime-terror/Tsuro/Player')
from strategy import strategy_factory
sys.path.append('../runtime-terror/Tsuro/Common')
from game_state import GameState
from board import Board

class TestClient(unittest.TestCase):

    def test_dumb_first_turn(self):
        game_state = GameState()
        strategy = strategy_factory("dumb")
        first_turn = [0, 1, 2]
        next_legal_turn = [3, 15, 11]
        illegal_turn = [2, 2, 34]

        turn_1 = strategy.first_turn(game_state, first_turn)

        game_state.player_first_turn("white", turn_1[0], turn_1[1], turn_1[2], turn_1[3])
        turn_2 = strategy.first_turn(game_state, next_legal_turn)
        turn_3 = strategy.first_turn(game_state, illegal_turn)

        self.assertAlmostEqual(turn_1, [2, 0, 'a1', 'n1'])
        self.assertAlmostEqual(turn_2, [11, 0, 'c1', 'n1'])
        self.assertAlmostEqual(turn_3, [34, 0, 'a1', 'n1'])

    def test_dumb_intermediate_turn(self):
        player_color = "white"
        game_state = GameState()
        strategy = strategy_factory("dumb")
        first_turn = [9, 15, 3]
        first_int_turn = [11, 10]
        second_int_turn = [12, 20]
        third_int_turn = [2, 21]

        turn_1 = strategy.first_turn(game_state, first_turn)
        game_state.player_first_turn(player_color, turn_1[0], turn_1[1], turn_1[2], turn_1[3])
        
        turn_2 = strategy.intermediate_turn(game_state, first_int_turn, player_color)
        self.assertAlmostEqual(turn_2, [11, 0, 'a2'])
        game_state.player_take_turn(player_color, turn_2[0], turn_2[1], turn_2[2], first_int_turn)
        
        turn_3 = strategy.intermediate_turn(game_state, second_int_turn, player_color)
        self.assertAlmostEqual(turn_3, [12, 0, 'b2'])
        game_state.player_take_turn(player_color, turn_3[0], turn_3[1], turn_3[2], second_int_turn)
        
        turn_4 = strategy.intermediate_turn(game_state, third_int_turn, player_color)
        self.assertAlmostEqual(turn_4, [2, 0, 'b1'])

    def test_dumb_second_turn(self):
        game_state = GameState()
        strategy = strategy_factory("second")
        first_turn = [0, 1, 2]
        next_legal_turn = [3, 15, 11]
        illegal_turn = [2, 2, 34]

        turn_1 = strategy.first_turn(game_state, first_turn)

        game_state.player_first_turn("white", turn_1[0], turn_1[1], turn_1[2], turn_1[3])
        turn_2 = strategy.first_turn(game_state, next_legal_turn)
        turn_3 = strategy.first_turn(game_state, illegal_turn)

        self.assertAlmostEqual(turn_1, [2, 0, 'a1', 'n1'])
        self.assertAlmostEqual(turn_2, [11, 0, 'a3', 'w1'])
        self.assertAlmostEqual(turn_3, [34, 0, 'a1', 'n1'])

    def test_second_intermediate_turn(self):
        player_color = "white"
        game_state = GameState()
        strategy = strategy_factory("second")
        first_turn = [9, 15, 3]
        first_int_turn = [11, 10]
        second_int_turn = [12, 20]
        third_int_turn = [2, 34]

        turn_1 = strategy.first_turn(game_state, first_turn)
        game_state.player_first_turn(player_color, turn_1[0], turn_1[1], turn_1[2], turn_1[3])
        

        turn_2 = strategy.intermediate_turn(game_state, first_int_turn, player_color)
        self.assertAlmostEqual(turn_2, [10, 0, 'a2'])
        game_state.player_take_turn(player_color, turn_2[0], turn_2[1], turn_2[2], first_int_turn)
        
        turn_3 = strategy.intermediate_turn(game_state, second_int_turn, player_color)
        self.assertAlmostEqual(turn_3, [20, 0, 'a3'])
        game_state.player_take_turn(player_color, turn_3[0], turn_3[1], turn_3[2], second_int_turn)
        
        turn_4 = strategy.intermediate_turn(game_state, third_int_turn, player_color)
        self.assertAlmostEqual(turn_4, [2, 0, 'b3'])


if __name__ == '__main__':
    unittest.main()
