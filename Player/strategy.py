#!/usr/bin/env python3
import sys
sys.path.append('../runtime-terror/Tsuro/Common')
from game_constants import VALID_PORTS, DEGREE_TO_NUMBER_OF_ROTATIONS, LEGAL
from board_physics import get_all_edge_coordinates, get_connecting_coordinate

# given a string return the specified strategy
# default to dumb if strategy doesn't exist
def strategy_factory(strategy_name):

    if strategy_name == "second":
        return SecondStrategy()
    else:
        return DumbStrategy()

class DumbStrategy:

    def __init__(self):
        self.name = "dumb"

    # game_state, tile choices -> tile_index, rotation, board_coordinate, starting_port
    # dumb strategy for first turn: uses the third given tile without rotation
    # and searches for the first legal spot clockwise
    def first_turn(self, game_state, tile_choices):
        tile_index = tile_choices[2]
        rotation = 0

        coordinate = "a1"
        starting_port = "n1"

        # for every port on the tile check if its a valid move. if not go to the next port
        # if there are no valid ports go to the next tile
        for board_coordinate in get_all_edge_coordinates():
            for port in VALID_PORTS:
                valid_move = game_state.initial_placement_check(tile_index, rotation, board_coordinate, port)[LEGAL]
                if valid_move:
                    coordinate = board_coordinate
                    starting_port = port
                    return [tile_index, rotation, coordinate, starting_port]

        return [tile_index, rotation, coordinate, starting_port]

    # game_state, tile choices -> tile_index, rotation, board_coordinate
    # dumb strategy for intermediate turns: the first given tile without
    # rotating it and places it on the square adjacent to the player’s avatar
    # does not check the legality of this action
    def intermediate_turn(self, game_state, tile_choices, player_color):
        current_player = game_state.player_dictionary[player_color]
        tile_index = tile_choices[0]
        # TODO: check if each player current tile is an edge

        neighbor = get_connecting_coordinate(current_player.current_tile, current_player.current_port)
        rotation = 0
        
        return [tile_index, rotation, neighbor]

##############################################################

class SecondStrategy:

    def __init__(self):
        self.name = "second"

    # game_state, tile choices -> tile_index, rotation, board_coordinate, starting_port
    # second strategy for first turn: uses the third given tile without rotation
    # and searches for the first legal spot counter clockwise
    def first_turn(self, game_state, tile_choices):
        tile_index = tile_choices[2]
        rotation = 0

        all_edges = get_all_edge_coordinates()
        all_edges.reverse()
        all_edges.insert(0, all_edges.pop())

        all_ports = list(VALID_PORTS)
        all_ports.reverse()
        all_ports.insert(0, all_ports.pop())

        # for every port on the tile check if its a valid move. if not go to the next port
        # if there are no valid ports go to the next tile
        for board_coordinate in all_edges:
            for port in all_ports:
                valid_move = game_state.initial_placement_check(tile_index, rotation, board_coordinate, port)[LEGAL]
                if valid_move:
                    return [tile_index, rotation, board_coordinate, port]

        return [tile_index, rotation, "a1", "n1"]

    # game_state, tile choices, player_color -> tile_index, rotation, board_coordinate
    # second strategy for intermediate turns: check all moves starting with the second
    # given tile without rotating it and places the first legal move on the square
    # adjacent to the player’s avatar, if no legal moves exist default to 2nd tile with no rotation
    def intermediate_turn(self, game_state, tile_choices, player_color):
        player = game_state.player_dictionary[player_color]
        neighboring_coordinate = player.get_connecting_coordinate()

        tile_indices_to_check = [1, 0]

        for index in tile_indices_to_check:
            tile_index = tile_choices[index]
            for degree in DEGREE_TO_NUMBER_OF_ROTATIONS.keys():
                is_valid_move = game_state.rule_check(player_color, tile_index, degree, neighboring_coordinate, tile_choices)[LEGAL]
                if is_valid_move:
                    return [tile_index, degree, neighboring_coordinate]

        tile_index = tile_choices[1]
        rotation = 0

        return [tile_index, rotation, neighboring_coordinate]
