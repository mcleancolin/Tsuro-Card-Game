#!/usr/bin/env python3

import sys, random, pickle, logging, socket, json, time
import referee_input_parsing
import referee_game_management
import messages as tcp_messages
from observer import Observer
sys.path.append("../Common")
import game_constants
from game_state import GameState
sys.path.append("../Player")
from strategy import strategy_factory

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('server')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('xserver.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# notifies players killed and updates the losers of the game
def kill_player(referee, player_color):
    connection = referee.player_connections[player_color]
    connection.sendall(pickle.dumps(tcp_messages.client_killed))
    referee.loosers.append(player_color)

# announces the color of the player that is the given connection
def announce_player_color(connection, color):
    connection.sendall(pickle.dumps(tcp_messages.client_joined_game))
    time.sleep(1)
    connection.sendall(pickle.dumps(color))

# checks the legality of the players move
def check_legality(referee, placement_result, player_color):
    connection = referee.player_connections[player_color]
    if placement_result["legal"]:
        connection.sendall(pickle.dumps(tcp_messages.legal_turn))
        logger.info("%s << %s", player_color, tcp_messages.legal_turn)
    else:
        logger.info("%s << %s", player_color, tcp_messages.illegal_turn)
        logger.info("%s << %s", player_color, placement_result["rules broken"])
        reprimand_cheater(referee, player_color, connection, placement_result["rules broken"])

# sends the necessary messages to a player who gets kicked out
def reprimand_cheater(referee, player_color, connection, rules_broken):
    connection.sendall(pickle.dumps(tcp_messages.illegal_turn))
    time.sleep(1)
    connection.sendall(pickle.dumps(rules_broken))
    referee.loosers.append(player_color)


# sends the message to the players as to who won the game
def send_game_over_messages(referee, player_color, winner_name):
    connection = referee.player_connections[player_color]
    connection.sendall(pickle.dumps(tcp_messages.winners))
    time.sleep(1)
    connection.sendall(pickle.dumps(winner_name))
    time.sleep(1)
    connection.close()
