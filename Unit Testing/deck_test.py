#!/usr/bin/env python3
import unittest, sys
import importlib
sys.path.append('../runtime-terror/Tsuro/Common')
from deck import Deck

class TestClient(unittest.TestCase):

    def test_deal_random_tiles(self):
        deck = Deck()
        random_deal_3 = deck.deal_random_tiles(3)
        random_deal_2 = deck.deal_random_tiles(2)

        self.assertAlmostEqual(len(random_deal_3), 3)
        self.assertAlmostEqual(len(random_deal_2), 2)

        for tile_index in random_deal_2 + random_deal_3:
            self.assertTrue(tile_index < 35)
            self.assertTrue(tile_index > -1)

    def test_deal_tiles(self):
        deck = Deck()
        deal_3 = deck.deal_tiles(3)
        deal_2 = deck.deal_tiles(2)

        self.assertAlmostEqual(deal_3, [0, 1, 2])
        self.assertAlmostEqual(deal_2, [3, 4])

    def test_get_tile(self):
        deck = Deck()
        tile_15 = deck.get_tile(15)
        tile_34 = deck.get_tile(34)

        tile_15_paths = [('n1', 'e1'), ('n2', 'w2'), ('e2', 's2'), ('s1', 'w1')]
        tile_34_paths = [('n1', 'n2'), ('e1', 'e2'), ('s2', 's1'), ('w2', 'w1')]

        self.assertAlmostEqual(tile_15.paths, tile_15_paths)
        self.assertAlmostEqual(tile_34.paths, tile_34_paths)

        tile_15.rotate(1)

        tile_15 = deck.get_tile(15)
        self.assertAlmostEqual(tile_15.paths, tile_15_paths)

    def test_get_tiles(self):
        deck = Deck()
        tile_list = deck.get_tiles([15, 34])

        tile_15_paths = [('n1', 'e1'), ('n2', 'w2'), ('e2', 's2'), ('s1', 'w1')]
        tile_34_paths = [('n1', 'n2'), ('e1', 'e2'), ('s2', 's1'), ('w2', 'w1')]

        tile_15 = tile_list[0]
        tile_34 = tile_list[1]

        self.assertAlmostEqual(tile_15.paths, tile_15_paths)
        self.assertAlmostEqual(tile_34.paths, tile_34_paths)

if __name__ == '__main__':
    unittest.main()