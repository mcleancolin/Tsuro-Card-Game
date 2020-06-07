DECK_SIZE = 35
BOARD_SIZE = 10
VALID_BOARD_COLUMNS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
PORT_SIDE_TO_DIRECTION = {"n": "north", "s": "south", "e": "east", "w": "west"}
DEGREE_TO_NUMBER_OF_ROTATIONS = { 0: 0, 90: 3, 180: 2, 270: 1 }
CONNECTING_PORTS = {"n": "s", "s": "n", "e": "w", "w": "e"}
TILE_INDEX_RANGE = range(0, DECK_SIZE)
ROTATION_RANGE = [0, 90, 180, 270]
COLOR_RANGE = ["white", "black", "red", "green", "blue"]
ALPHA_PORT_RANGE = ["A", "B", "C", "D", "E", "F", "G", "H"]
CARDINAL_RANGE = range(0, BOARD_SIZE)

# TODO: consider 0 indexing everythings
# TODO: function that returns all valid ports in our syntax
# TODO: rename these to make more sense
OUR_PORTS_TO_ALPHA = {
    "n1": "A", "n2": "B", "e1": "C", "e2": "D", "s2": "E", "s1": "F", "w2": "G", "w1": "H"
}
ALPHA_TO_OUR_PORTS = {
    "A": "n1", "B": "n2", "C": "e1", "D": "e2", "E": "s2", "F": "s1", "G": "w2", "H": "w1"
}

VALID_PORTS = OUR_PORTS_TO_ALPHA.keys()

#############################################################

EDGE = "edge"
TILE = "tile"
PORT = "port"

NORTH = "north"
SOUTH = "south"
WEST = "west"
EAST = "east"

LEGAL = "legal"
RULES_BROKEN = "rules broken"
INVALID_COORDINATE =  "coordinate is invalid"
OCCUPIED_COORDINATE = "coordinate is already occupied"
NOT_BORDERING_EDGE = "tile placement is not on the board's edge"
PLACEMENT_HAS_NEIGHBORS = "tile placement has neighbors"
INVALID_STARTING_PORT = "starting port is invalid"
PLACEMENT_AVOIDABLE_SUICIDE = "tile placement is avoidable suicide"
PLACEMENT_NOT_BORDERING_AVATAR = "tile placement is not in front of given player"

GAME_OVER = "game over"
PLAYERS_KILLED = "players killed"
WINNERS = "winners"
LOSERS = "losers"

HUMAN = "human"
NAME = "name"
STRATEGY = "strategy"

#############################################################

# TODO: turn this into a fucnttion
# could be replaced by convert_coordinate_to_battleship
board_column_number_to_letter = {"1": "b", "2": "c", "3": "d", "4": "e", \
"5": "f", "6": "g", "7": "h", "8": "i", "9": "j", "0": "a"}
port_side_to_direction = {"n": "north", "s": "south", "e": "east", "w": "west"}
degree_to_number_of_rotations = {"90": "1", "180": "2", "270": "3"}
connecting_ports = {"n": "s", "s": "n", "e": "w", "w": "e"}
tile_index_range = range(0, 35)
rotation_range = [0, 90, 180, 270]
color_range = ["white", "black", "red", "green", "blue"]
port_range = ["A", "B", "C", "D", "E", "F", "G", "H"]
cardinal_range = range(0, 10)
x_list = VALID_BOARD_COLUMNS
battleship_dict = {
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9
}
ours_to_profs = {
    "n1": "A", "n2": "B", "e1": "C", "e2": "D", "s2": "E", "s1": "F", "w2": "G", "w1": "H"
}
prof_to_our_dict = {
    "A": "n1", "B": "n2", "C": "e1", "D": "e2", "E": "s2", "F": "s1", "G": "w2", "H": "w1"
}
