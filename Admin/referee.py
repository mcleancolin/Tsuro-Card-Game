#!/usr/bin/env python3

import sys, random, pickle, logging, socket, json, time
import referee_input_parsing
import referee_game_management
import referee_connection_helpers
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

class Referee:

    def __init__(self):
        self.player_names = []
        self.player_connections = {}
        self.game_state = GameState()
        self.winners = []
        self.loosers = []
        self.game_over = False

    # initializes the server for the referee to run the game on
    def initialize_server(self, address, port):
        # Create Server Socket
        sock = self.create_and_bind_socket(address, port)
        sock.listen()

        while True:
            # Waiting for a new connection
            logging.info(tcp_messages.waiting_for_clients)
            try:
                connection, client_address = sock.accept()
                self.receive_name_and_strategy(connection)
                color = game_constants.COLOR_RANGE[len(self.player_connections)]
                referee_connection_helpers.announce_player_color(connection, color)
                self.player_connections[color] = connection
                referee_game_management.check_game_start(self, sock)
            except:
                self.conduct_game()
                break

    # creates the socket for the server to run on
    def create_and_bind_socket(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (address, port)
        logging.info(tcp_messages.starting_server % server_address)
        sock.bind(server_address)
        return sock

    # receives and saves the names of the client over the given connection
    def receive_name_and_strategy(self, connection):
        input_dictionary = pickle.loads(connection.recv(512))
        name = input_dictionary[game_constants.NAME]
        self.player_names.append(name)
        logger.info("Added " + name + " to the game.")

    # conducts a game
    def conduct_game(self):
        logger.info("The players in the game are " + str(self.player_names))
        self.start_game()
        logger.info("Initial moves have finished.")

        self.perform_game()

        logger.info("The game has now finished.")
        obs = Observer()
        obs.observe_game_state(self.game_state)
        referee_game_management.end_game(self)

    # conducts the first moves of the game
    def start_game(self):
        for player_color in self.player_connections.keys():
            input_array, tile_choices = self.get_first_move_from_client(player_color)
            strategy = referee_input_parsing.get_strategy(input_array)
            logger.info("%s << dealt tiles: %s", player_color, tile_choices)
            logger.info("%s >> turn: %s", player_color, input_array)
            initial_placement_result = self.execute_first_move(player_color, strategy, tile_choices)
            logger.info("%s << turn response: %s", player_color, initial_placement_result)
            referee_connection_helpers.check_legality(self, initial_placement_result, player_color)

    # conducts the intermediate moves of the game
    def perform_game(self):
        while not self.game_over:
            # assume players are in sorted order
            for player_color in self.game_state.get_living_players():
                connection = self.player_connections[player_color]

                tile_choices = self.game_state.deck.deal_tiles(2)
                player_info = self.send_and_receive_input(connection, tile_choices, \
                tcp_messages.client_intermediate_turn)

                strategy = referee_input_parsing.get_strategy(player_info)

                self.execute_intermediate_move(player_color, strategy, tile_choices)

                if not self.game_over and len(self.game_state.get_living_players()) < 2:
                    self.game_over = True
                    self.winners = self.game_state.get_living_players()

    # gets the input array for the first move of the given player
    def get_first_move_from_client(self, player_color):
        tile_choices = self.game_state.deck.deal_tiles(3)
        connection = self.player_connections[player_color]
        input_array = self.send_and_receive_input(connection, tile_choices, tcp_messages.client_first_turn)
        return input_array, tile_choices

    # deals the tiles, sends and receives move output/input, and then processes
    # the input for the move the player wants to perform
    def execute_first_move(self, player_color, strategy, tile_choices):
        turn_array = self.get_turn_array(tcp_messages.client_first_turn, player_color, strategy, tile_choices)

        tile_index, rotation, starting_port, coordinate = \
        referee_input_parsing.extract_initial_input_ai(turn_array)

        # TODO: allow player to check rule before turn is executed
        initial_placement_result = \
        self.game_state.player_first_turn(player_color, tile_index, rotation, coordinate, starting_port)

        return initial_placement_result

    # gets the input from the user regarding which tile they want to place and where
    def execute_intermediate_move(self, player_color, strategy, tile_choices):
        turn_array = self.get_turn_array(tcp_messages.client_intermediate_turn, player_color, strategy, tile_choices)

        tile_index, rotation, board_coordinate = \
        referee_input_parsing.extract_intermediate_input_ai(turn_array)
        logger.info("%s << Your tiles are: %s", player_color, tile_choices)
        logger.info("%s >> Turn: %s", player_color, turn_array)
        # TODO: allow player to check rule before turn is executed
        placement_result = \
        self.game_state.player_take_turn(player_color, tile_index, \
        rotation, board_coordinate, tile_choices)
        referee_connection_helpers.check_legality(self, placement_result, player_color)


    # sends and receives the message to the player for the initial move
    def send_and_receive_input(self, connection, tile_choices, turn_type):
        connection.sendall(pickle.dumps(turn_type))
        time.sleep(1)
        connection.sendall(pickle.dumps(str(tile_choices)))
        input = pickle.loads(connection.recv(512))
        return input

    # gets the turn array from the player based on their strategy
    def get_turn_array(self, turn_type, player_color, strategy, tile_choices):
        if strategy == game_constants.HUMAN:
            turn_array = self.get_human_turn_spec(player_color)
        else:
            turn_array = referee_game_management.get_ai_turn_spec(self, \
            player_color, turn_type, strategy, tile_choices)
        return turn_array

    # gets the turn spec from a human player via tcp ip messages
    def get_human_turn_spec(self, player_color):
        connection = self.player_connections[player_color]
        connection.sendall(pickle.dumps(tcp_messages.human_turn))
        time.sleep(1)
        input = pickle.loads(connection.recv(512))
        turn_array = json.loads(input)
        return turn_array


if __name__ == '__main__':
    port = 8000
    address = 'localhost'
    if len(sys.argv) == 2:
        port = sys.argv[1]
    elif len(sys.argv) == 3:
        port = sys.argv[1]
        address = sys.argv[2]
    referee = Referee()
    referee.initialize_server(address, port)
