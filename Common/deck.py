#!/usr/bin/env python3

import sys, random, logging
from tiles import HandTile
from all_tiles import create_tiles
from game_constants import DECK_SIZE

class Deck:

    def __init__(self):
        self.deck = create_tiles()        
        self.last_index_delt = 0

    # returns an array of the given size of random indexes 0 - 34
    def deal_random_tiles(self, tile_quantity):
        tile_indexes = []
        while 0 < tile_quantity:
            tile_indexes.append(random.randint(0, DECK_SIZE - 1))
            tile_quantity = tile_quantity - 1
        return tile_indexes

    # returns an array of the given size of the next tiles in the deck
    def deal_tiles(self, tile_quantity):
        tile_indexes = []
        while 0 < tile_quantity:
            tile_quantity = tile_quantity - 1
            tile_indexes.append(self.last_index_delt)
            if self.last_index_delt == DECK_SIZE - 1:
                self.last_index_delt = 0
            else:
                self.last_index_delt = self.last_index_delt + 1
        return tile_indexes

    def get_tile(self, tile_index):
        deck_tile = self.deck[tile_index]
        player_tile = HandTile(list(deck_tile.paths))
        return player_tile

    # returns a list of tiles from the deck based on the given indexes
    def get_tiles(self, tile_index_list):
        tile_list = []

        for tile_index in tile_index_list:
            tile = self.get_tile(tile_index)
            tile_list.append(tile)

        return tile_list
    