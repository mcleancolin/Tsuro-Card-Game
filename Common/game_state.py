#!/usr/bin/env python3

import sys, random, logging
from board import Board
from rulechecker import RuleChecker
from board_physics import get_connecting_coordinate, get_number_of_rotations
from rulechecker import RuleChecker
from avatar import Avatar
from deck import Deck
from game_constants import DEGREE_TO_NUMBER_OF_ROTATIONS, LEGAL, GAME_OVER, PLAYERS_KILLED, WINNERS, LOSERS

logging.basicConfig(level=logging.DEBUG)

class GameState:

    def __init__(self):
        self.deck = Deck()
        self.board = Board()
        self.player_dictionary = {}
        self.rule_checker = RuleChecker()
        self.dead_players = []

    #################### Public methods ###################################

    # checks if an initial tile placement is legal
    # tile_index -> int : 0 - 34 (represents the index in all_tiles)
    # rotation -> int : 0, 90, 180, 270 (represents the number of roations for the given tile)
    # boar_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
    # starting_port -> string : valid_port() (port on the edge of the board the player starts at)
    def initial_placement_check(self, tile_index, rotation, board_coordinate, starting_port):
        tile = self.deck.get_tile(tile_index)
        number_of_rotations = get_number_of_rotations(rotation)
        tile.rotate(number_of_rotations)
        return self.rule_checker.check_first_turn(self.board, tile, board_coordinate, starting_port)

    # performs a players first turn, returns the validity of that turn (if not valid kills player)
    # player_color -> string : valid_color() (the color of the player making the turn)
    # tile_index -> int : 0 - 34 (represents the index in all_tiles)
    # rotation -> int : 0, 90, 180, 270 (represents the number of roations for the given tile)
    # boar_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
    # starting_port -> string : valid_port() (port on the edge of the board the player starts at)
    def player_first_turn(self, player_color, tile_index, rotation, board_coordinate, starting_port):
        new_player = Avatar(player_color)
        self.player_dictionary[player_color] = new_player

        first_turn_rule_check = self.initial_placement_check(tile_index, rotation, board_coordinate, starting_port)
        if first_turn_rule_check[LEGAL]:
            tile = self.deck.get_tile(tile_index)
            number_of_rotations = get_number_of_rotations(rotation)
            tile.rotate(number_of_rotations)
            self.board.first_turn(new_player, tile, board_coordinate, starting_port)
        else:
            self.dead_players.append(player_color)

        return first_turn_rule_check

    # checks if an players turn is legal
    # player_color -> string : valid_color() (the color of the player making the turn)
    # tile_index -> int : 0 - 34 (represents the index in all_tiles)
    # rotation -> int : 0 - 3 (represents the number of roations for the given tile)
    # boar_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
    # tile_choices -> array[int] : 2 - 3 (tile options the player had to choose from)
    def rule_check(self, player_color, tile_index, rotation, board_coordinate, tile_choices):
        player = self.player_dictionary[player_color]
        players_tiles = self.deck.get_tiles(tile_choices)
        player.tiles = players_tiles

        tile = self.deck.get_tile(tile_index)
        number_of_rotations = get_number_of_rotations(rotation)
        tile.rotate(number_of_rotations)

        return self.rule_checker.check_turn(self.board, tile, board_coordinate, player)

    # performs a players turn, returns the result or validity of that turn (if not valid kills player)
    # player_color -> string : valid_color() (the color of the player making the turn)
    # tile_index -> int : 0 - 34 (represents the index in all_tiles)
    # rotation -> int : 0 - 3 (represents the number of roations for the given tile)
    # boar_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
    # tile_choices -> array[int] : 2 - 3 (tile options the player had to choose from)
    def player_take_turn(self, player_color, tile_index, rotation, board_coordinate, tile_choices):
        rule_check = self.rule_check(player_color, tile_index, rotation, board_coordinate, tile_choices)
        if rule_check[LEGAL]:
            player = self.player_dictionary[player_color]

            tile = self.deck.get_tile(tile_index)
            number_of_rotations = get_number_of_rotations(rotation)
            tile.rotate(number_of_rotations)

            self.board.take_turn(tile, board_coordinate, player)
            players_killed = self.update_other_players_positions(player, board_coordinate)
            result = self.get_turn_results(players_killed)
            self.dead_players.extend(players_killed)

            return result
        else:
            self.dead_players.append(player_color)
            return rule_check

    #################### Private methods #######################

    # returns a set of the remaining living player colors
    def get_living_players(self):
        players_set = set(self.player_dictionary.keys())
        dead_players_set = set(self.dead_players)
        living_players_set = players_set.difference(dead_players_set)
        return living_players_set

    # given a list of player colors move those players
    # expectation that these players are all moveable otherwise
    # throws an exception
    def move_players(self, players_to_move):
        for player_color in players_to_move:
            player = self.player_dictionary[player_color]
            self.board.move_player(player)

    # updates the positions of the other players still on the board
    # given the current player and where they placed the tile on their turn
    # returns the players killed in this turn
    def update_other_players_positions(self, current_player, board_coordinate):
            players_killed = []
            if current_player.is_player_dead():
                players_killed.append(current_player.color)

            living_players = self.get_living_players()
            living_players.discard(current_player.color)
            players_to_move = []

            for player_color in living_players:
                player = self.player_dictionary[player_color]
                if player.get_connecting_coordinate() == board_coordinate:
                    players_to_move.append(player.color)

            self.move_players(players_to_move)

            for player_color in players_to_move:
                if self.player_dictionary[player_color].is_player_dead():
                    players_killed.append(player_color)

            return players_killed

    # given the players killed during a turn return the results of a legal move
    def get_turn_results(self, players_killed):
        result = { LEGAL: True,  PLAYERS_KILLED: [], GAME_OVER: False }
        is_game_over = len(self.player_dictionary) - len(self.dead_players) < 2
        is_tie = len(self.player_dictionary) == len(self.dead_players)

        if is_game_over:
            result[GAME_OVER] = True
            if is_tie:
                result[WINNERS] = players_killed
                result[LOSERS] = self.dead_players
            else:
                result[WINNERS] = self.get_living_players()
                result[LOSERS] = self.dead_players
        else:
            self.dead_players.extend(players_killed)
            result[PLAYERS_KILLED] = players_killed

        return result
