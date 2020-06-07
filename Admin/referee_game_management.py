#!/usr/bin/env python3

import sys, random, pickle, logging, socket, json, time
import referee_input_parsing
import referee_connection_helpers
import messages as tcp_messages
from observer import Observer
sys.path.append("../Common")
import game_constants
from game_state import GameState
sys.path.append("../Player")
from strategy import strategy_factory

# announces the winner at thee end of the game
def end_game(referee):
    winner_name = get_winners_name(referee)
    for player_color in referee.player_connections.keys():
        referee_connection_helpers.send_game_over_messages(referee, player_color, winner_name)

# gets the name of the winner
def get_winners_name(referee):
    winner_color = referee.winners.pop()
    color_index = game_constants.COLOR_RANGE.index(winner_color)
    winner_name = referee.player_names[color_index]
    return winner_name

# execute the outcome of a legal move
def execute_turn_outcome(referee, turn_result):
    if turn_result[game_constants.GAME_OVER]:
        update_game_results(referee, turn_result)
    else:
        for player_color in turn_result[game_constants.PLAYERS_KILLED]:
            referee_connection_helpers.kill_player(referee, player_color)

# updates the winners, losers, and status of the game
def update_game_results(referee, turn_result):
    referee.game_over = True
    referee.winners = turn_result[game_constants.WINNERS]
    referee.loosers = turn_result[game_constants.LOSERS]

def get_ai_turn_spec(referee, player_color, turn_type, strategy, tile_choices):
    strategy_object = strategy_factory(strategy)
    if turn_type == tcp_messages.client_first_turn:
        turn_array = strategy_object.first_turn(referee.game_state, tile_choices)
    else:
        turn_array = strategy_object.intermediate_turn(referee.game_state, tile_choices, player_color)
    return turn_array

# checks to see if the game should start
def check_game_start(referee, sock):
    if(len(referee.player_connections) == 3):
        sock.settimeout(5)
    if(len(referee.player_connections) == 5):
        referee.conduct_game()
