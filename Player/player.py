#!/usr/bin/env python3

import sys, socket, pickle, time
sys.path.append('../Common')
from tiles import BoardTile
from game_constants import NAME, STRATEGY
sys.path.append('../Admin')
import messages as tcp_messages

colors = ['white', 'black', 'red', 'green', 'blue']

class Player:

    # Constructor
    def __init__(self, name, strategy):
        # TODO: takes in a ip address and a port
        self.name = name
        self.strategy = strategy

    # creates the socket to connect to the server with
    def create_client(self, port, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (address, port)
        self.sock.connect(server_address)
        self.send_name_and_strategy_dictionary()
        self.game_communication()

    # sends the  name and strategy of this player to the server
    def send_name_and_strategy_dictionary(self):
        name_strategy_dictionary = self.form_move()
        self.sock.sendall(pickle.dumps(name_strategy_dictionary))


    # function to perform server communication with throughout the game
    def game_communication(self):
        while True:
            input = pickle.loads(self.sock.recv(512))
            print(input)
            self.parse_input(input)
            if input == tcp_messages.winners:
                break


    # Checks to see which type of request the server has sent. Substrings each
    # of the inputs to see them stem of the message from the server. The stems
    # of the message follow a pattern, but the rest depends on current game.
    def parse_input(self, input):
        if input == tcp_messages.client_joined_game:
            self.read_color()
        elif input == tcp_messages.client_first_turn:
            self.read_tiles_dealt()
            self.create_turn_request()
        elif input == tcp_messages.client_intermediate_turn:
            self.read_tiles_dealt()
            self.create_turn_request()
        elif input == tcp_messages.human_turn:
            self.send_turn_spec()
        elif input == tcp_messages.illegal_turn:
            self.show_rules_broken()
        elif input == tcp_messages.winners:
            self.display_winners()

    # sets the color of this player to the color the server assigned them
    def read_color(self):
        color_from_server = pickle.loads(self.sock.recv(512))
        print(color_from_server)

    # reads the tiles that player was dealt
    def read_tiles_dealt(self):
        tiles_from_server = pickle.loads(self.sock.recv(512))
        print(tcp_messages.tiles_delt + tiles_from_server)

    # reponse of an intermediate move in a game of Tsuro
    def create_turn_request(self):
        turn_request = self.form_move()
        self.sock.sendall(pickle.dumps(turn_request))

    def send_turn_spec(self):
        turn_spec = input()
        self.sock.sendall(pickle.dumps(turn_spec))

    # shows the name of the winner of the game
    def display_winners(self):
        winner_name = pickle.loads(self.sock.recv(512))
        print(winner_name)
        self.sock.close()

    # creates a json object with the name of this player and the strategy of this player
    def form_move(self):
        move = {}
        move[NAME] = self.name
        move[STRATEGY] = self.strategy
        return move

    # shows this player the rules that they broke in their latets turn
    def show_rules_broken(self):
        rules_broken = pickle.loads(self.sock.recv(512))
        print(tcp_messages.rules_broken + str(rules_broken))


if __name__ == '__main__':
    port = sys.argv[1]
    port = int(port)
    address = sys.argv[2]
    name = sys.argv[3]
    strategy = sys.argv[4]
    player = Player(name, strategy)
    player.create_client(port, address)
