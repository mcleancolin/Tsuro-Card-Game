#!/usr/bin/env python3

import sys
from tiles import HandTile
from board_physics import valid_port, valid_coordinate, port_to_side, get_connecting_port, is_edge, get_coordinate_neighbor, get_connecting_coordinate
from game_constants import COLOR_RANGE, EDGE, TILE, LEGAL, RULES_BROKEN, INVALID_COORDINATE, OCCUPIED_COORDINATE, NOT_BORDERING_EDGE, PLACEMENT_HAS_NEIGHBORS, PLACEMENT_AVOIDABLE_SUICIDE, INVALID_STARTING_PORT, PLACEMENT_NOT_BORDERING_AVATAR


class RuleChecker:

    # Constructor
    # does not need to have it's own instances of board, coordinates or players
    # because they will be passed in? let me know if that is dumb
    def __init__(self):
        pass

    # check_player_color -- checks if the color is a valid player color
    def check_player_color(self, color):
        return color in COLOR_RANGE

    # valid_port -- checks to make sure the player has chosen a valid starting port
    # board, coordinate, port -> boolean
    def valid_starting_port(self, board_coordinate, starting_port):
        is_valid_port = valid_port(starting_port)
        if (is_valid_port):
            starting_port_side = port_to_side(starting_port)
            neighbor_on_that_side = get_coordinate_neighbor(board_coordinate, starting_port_side)
            return neighbor_on_that_side == EDGE
        else:
            return False

    # check_player_dead -- checks to see if the player would die if the tile is placed
    def check_player_dead(self, board, tile, board_coordinate, player):
        # get port on given tile
        new_tile_connecting_port = get_connecting_port(player.current_port)
        # get the end of the path on given tile
        end_port_on_tile = tile.end_of_path(new_tile_connecting_port)

        connecting_side = port_to_side(end_port_on_tile)
        connecting_neighbor_coordinate = get_coordinate_neighbor(board_coordinate, connecting_side)

        if connecting_neighbor_coordinate == EDGE:
            return True
        elif board.is_coordinate_occupied(connecting_neighbor_coordinate):
            board_connecting_port = get_connecting_port(end_port_on_tile)
            ending_location = board.end_of_path(connecting_neighbor_coordinate, board_connecting_port)
            return ending_location[TILE] == EDGE
        else:
            return False

    # with the given tiles the player has is there a turn
    # they could play that doesn't result in thier death
    # returns True if there is a non deadly move, False if not
    def is_player_death_avoidable(self, board, player):
        all_tile_options = []
        for tile in player.tiles:
            rotations_left = 4
            while rotations_left > 0:
                rotations_left = rotations_left - 1
                temp_tile = HandTile(tile.paths)
                temp_tile.rotate(rotations_left)
                all_tile_options.append(temp_tile)
    
        for tile in all_tile_options:
            board_coordinate = get_connecting_coordinate(player.current_tile, player.current_port)
            would_player_die = self.check_player_dead(board, tile, board_coordinate, player)
            if not would_player_die:
                return True

        return False

    # check_first_turn: in the first turn tiles must...
    #   - not neighbor other tiles
    #   - be placed on the edge of the board
    #   - not be placed where the avatar does not occupy a port that faces the board’s interior.
    # board, board_coordinate, starting_port -> boolean
    def check_first_turn(self, board, tile, board_coordinate, starting_port):
        invalid_coordinate = not valid_coordinate(board_coordinate)
        is_occupied = board.is_coordinate_occupied(board_coordinate)
        doesnt_border_edge = not is_edge(board_coordinate)
        # get neighbors
        neighbors = board.get_board_coordinate_neighbors(board_coordinate)
        has_neighbors = False
        for neighbor in neighbors.values():
            if neighbor != EDGE and neighbor != None:
                has_neighbors = True

        invalid_starting_port = not self.valid_starting_port(board_coordinate, starting_port)

        tile_end_port = tile.end_of_path(starting_port)
        is_placement_suicide = get_connecting_coordinate(board_coordinate, tile_end_port) == EDGE

        rule_is_broken_map = { 
            INVALID_COORDINATE : invalid_coordinate, 
            OCCUPIED_COORDINATE : is_occupied, 
            NOT_BORDERING_EDGE: doesnt_border_edge,
            PLACEMENT_HAS_NEIGHBORS : has_neighbors,
            INVALID_STARTING_PORT : invalid_starting_port,
            PLACEMENT_AVOIDABLE_SUICIDE : is_placement_suicide
        }

        is_first_turn_legal = not any(rule_is_broken_map.values())

        if is_first_turn_legal:
            return { LEGAL : True, RULES_BROKEN : None}
        else:
            broken_rules = [] 
            for broken_rule_message in rule_is_broken_map.keys():
                if rule_is_broken_map[broken_rule_message]:
                    broken_rules.append(broken_rule_message)
            return {LEGAL : False, RULES_BROKEN : broken_rules}

    # check_turn -- all other turns: tiles must be placed in front of the player
    # board, board_coordinate, player -> boolean
    def check_turn(self, board, tile, board_coordinate, player):
        invalid_coordinate = not valid_coordinate(board_coordinate)
        is_occupied = board.is_coordinate_occupied(board_coordinate)

        valid_tile_placement = player.get_connecting_coordinate()

        is_correct_coordinate = board_coordinate == valid_tile_placement

        would_player_die = self.check_player_dead(board, tile, board_coordinate, player)
        # This is always True if would_player_die is False
        is_player_death_avoidable = self.is_player_death_avoidable(board, player)

        is_tile_selection_suicidal = is_player_death_avoidable and would_player_die

        rule_is_broken_map = { 
            INVALID_COORDINATE : invalid_coordinate, 
            OCCUPIED_COORDINATE : is_occupied, 
            PLACEMENT_NOT_BORDERING_AVATAR : not is_correct_coordinate,
            PLACEMENT_AVOIDABLE_SUICIDE : is_tile_selection_suicidal
        }

        is_turn_legal = not any(rule_is_broken_map.values())

        if is_turn_legal:
            return { LEGAL : True, RULES_BROKEN : None}
        else:
            broken_rules = [] 
            for broken_rule_message in rule_is_broken_map.keys():
                if rule_is_broken_map[broken_rule_message]:
                    broken_rules.append(broken_rule_message)
            return { LEGAL : False, RULES_BROKEN : broken_rules}
