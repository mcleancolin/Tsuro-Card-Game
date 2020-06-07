#!/usr/bin/env python3
import unittest, sys
import importlib

sys.path.append('../runtime-terror/Tsuro/Common')

from tiles import BoardTile, HandTile, Tile 

class TestClient(unittest.TestCase):

    # Tile Tests
    def test_end_of_path(self):
        paths = [('s1', 'e2'), ('s2', 'w1'), ('e1', 'n2'), ('n1', 'w2')]
        tile = Tile(paths)

        self.assertAlmostEqual(tile.end_of_path('s1'), 'e2')
        self.assertAlmostEqual(tile.end_of_path('e2'), 's1')

        hand_tile = HandTile(paths)
        self.assertAlmostEqual(hand_tile.end_of_path('e1'), 'n2')
        self.assertAlmostEqual(hand_tile.end_of_path('n2'), 'e1')

    #HandTile Tests
    def test__rotate(self):
        paths = [('s1', 'e2'), ('s2', 'w1'), ('e1', 'n2'), ('n1', 'w2')]
        hand_tile = HandTile(paths)
        hand_tile_rotated_clockwise = HandTile([('w1', 's1'), ('w2', 'n2'), ('s2', 'e2'), ('e1', 'n1')])
        hand_tile_rotated_counter = HandTile([('e2', 'n2'), ('e1', 's1'), ('n1', 'w1'), ('w2', 's2')])
        hand_tile_rotated_180 = HandTile([('n2', 'w1'), ('n1', 'e2'), ('w2', 's1'), ('s2', 'e1')])

        self.assertAlmostEqual(hand_tile.paths, paths)

        hand_tile.rotate(1)

        self.assertAlmostEqual(hand_tile.paths, hand_tile_rotated_counter.paths)

        hand_tile.rotate(1)

        self.assertAlmostEqual(hand_tile.paths, hand_tile_rotated_180.paths)

        hand_tile.rotate(1)

        self.assertAlmostEqual(hand_tile.paths, hand_tile_rotated_clockwise.paths)

        hand_tile.rotate(1)

        self.assertAlmostEqual(hand_tile.paths, paths)

if __name__ == '__main__':
    unittest.main()