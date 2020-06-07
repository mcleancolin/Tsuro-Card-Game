#!/usr/bin/env python3

import sys
from tiles import BoardTile
from rulechecker import RuleChecker
import logging
from game_constants import EDGE, TILE, PORT, LEGAL, NORTH, SOUTH, EAST, WEST
from board_physics import get_opposite_side, port_to_side, get_connecting_port, get_connecting_coordinate, get_coordinate_neighbor
logging.basicConfig(level=logging.DEBUG)


class Board:

    # Constructor
    def __init__(self):
        self.tiles = {}
        self.rule_checker = RuleChecker()

    # returns true if the given board coordinate has a tile on it 
    def is_coordinate_occupied(self, board_coordinate):
        return board_coordinate in self.tiles.keys()
    
    # returns dictionary of north, south, east, west neighbors of the given square
    def get_board_coordinate_neighbors(self, board_coordinate):
        neighbors = { NORTH: None, SOUTH: None, WEST: None, EAST: None}
        for side in neighbors.keys():
            neighbor = get_coordinate_neighbor(board_coordinate, side)
            if self.is_coordinate_occupied(neighbor):
                neighbor = self.tiles[neighbor]
            elif neighbor != EDGE:
                neighbor = None
            neighbors[side] = neighbor

        return neighbors

    # Converts hand_tile to a BoardTile and initializes its neighbors
    def convert_to_board_tile(self, hand_tile, board_coordinate):
        tile_neighbors = self.get_board_coordinate_neighbors(board_coordinate)
        board_tile = BoardTile(hand_tile.paths, tile_neighbors)
        return board_tile

    # hand_tile is a HandTile , board_coordinate is a string of 2 characters
    # in battleship coordiates -> 10x10 board is A-J 1-10
    # returns the generated board tile
    def place_tile(self, hand_tile, board_coordinate):
        board_tile = self.convert_to_board_tile(hand_tile, board_coordinate)
        self.tiles[board_coordinate] = board_tile

        # Link the newly created board tile to any of its neighbors currently on the board
        sides = [NORTH, SOUTH, EAST, WEST]
        for side in sides:
            new_neighbor_coordinate = get_coordinate_neighbor(board_coordinate, side)
            if self.is_coordinate_occupied(new_neighbor_coordinate):
                new_neighbor = self.tiles[new_neighbor_coordinate]
                new_neighbor.set_neighbor(get_opposite_side(side), board_tile)

        return board_tile

    # given a board coordinate and a starting port on the tile at that location
    # return the end board coordinate and port of that path on this board
    # or EDGE if they fall off the board
    # board_coordinate must have a tile on it (be in board.tiles)
    def end_of_path(self, board_coordinate, starting_port):
        board_tile = self.tiles[board_coordinate]
        end_port = board_tile.end_of_path(starting_port)
        neighboring_side = port_to_side(end_port)
        neighbor_to_move_to = board_tile.neighbors[neighboring_side]

        if neighbor_to_move_to == EDGE:
            return { TILE : EDGE, PORT: EDGE}
        elif neighbor_to_move_to == None:
            return { TILE : board_coordinate, PORT: end_port}
        else:
            new_tile_location = get_coordinate_neighbor(board_coordinate, neighboring_side)
            starting_port_on_new_tile = get_connecting_port(end_port)
            return self.end_of_path(new_tile_location, starting_port_on_new_tile)

    # moves given player to given board_coordinate and moves them along the path
    # throws exception if player cannot be moved (if there is no tile at the connecting side)
    def move_player(self, player):
        starting_port = player.current_port
        new_coordiate = get_connecting_coordinate(player.current_tile, starting_port)

        if self.is_coordinate_occupied(new_coordiate):
            port_on_new_tile = get_connecting_port(starting_port)
            ending_location = self.end_of_path(new_coordiate, port_on_new_tile)
            player.current_tile = ending_location[TILE]
            player.current_port = ending_location[PORT]
        else:
            logging.info("Player cannot be moved, no tile at: %s", new_coordiate)
            sys.exit(1)

    # places a player and a handtile on the board at the given coordinate and port
    # this is part of the players intial turn
    def first_turn(self, player, hand_tile, board_coordinate, starting_port):
        # Rule Checker : sees if tile location is valid
        first_turn_check = self.rule_checker.check_first_turn(self, hand_tile, board_coordinate, starting_port)[LEGAL]
        if first_turn_check:
            board_tile = self.place_tile(hand_tile, board_coordinate)
            end_port = board_tile.end_of_path(starting_port)
            player.place_avatar(board_coordinate, end_port)
        else:
            logging.info("Invalid initial tile placement: %s", board_coordinate)
            sys.exit(1)

    def take_turn(self, hand_tile, board_coordinate, player):
        # Rule Checker : sees if turn is valid
        turn_check = self.rule_checker.check_turn(self, hand_tile, board_coordinate, player)[LEGAL]
        if turn_check:
            self.place_tile(hand_tile, board_coordinate)
            self.move_player(player)
        else:
            logging.info("Invalid turn: %s", board_coordinate)
            sys.exit(1)

    
    def get_port_coordinate(self, port):
        return (0,0)
