#!/usr/bin/env python3
import unittest, sys
import importlib
from datetime import datetime
sys.path.append('../runtime-terror/Tsuro/Common')
from referee import Referee

class TestClient(unittest.TestCase):

    def test_referee_creation(self):
        referee = Referee()
        self.assertAlmostEqual(len(referee.player_connections), 0)
        self.assertAlmostEqual(len(referee.winners), 0)
        self.assertAlmostEqual(len(referee.loosers), 0)
        self.assertAlmostEqual(referee.game_over, False)


if __name__ == '__main__':
    unittest.main()
