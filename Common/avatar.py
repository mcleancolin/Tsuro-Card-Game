#!/usr/bin/env python3

import sys, socket, pickle
from tiles import BoardTile
from game_constants import EDGE
from board_physics import get_connecting_coordinate

class Avatar:

    # Constructor
    def __init__(self, color):
        self.color = color
        self.tiles = []
        self.current_tile = None
        self.current_port = None

    # updates the place of this player after they complete a turn
    def place_avatar(self, board_coordinate, starting_port):
        self.current_tile = board_coordinate
        self.current_port = starting_port

    def is_player_dead(self):
        return self.current_tile == EDGE

    def get_connecting_coordinate(self):
        if self.current_tile == EDGE:
            return EDGE
        else:
            return get_connecting_coordinate(self.current_tile, self.current_port)
