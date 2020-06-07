import sys, json
sys.path.append("../Common")
import board_physics
from game_constants import STRATEGY
from json import JSONDecodeError

# converts the given (x,y) coordinate to a battleship coordinate
def convert_to_battleship(x, y):
    letter = board_physics.column_number_to_letter(x)
    board_coordinate = letter + str(y)
    return board_coordinate

# checks to see if the given string is a valid JSON array
def is_valid_array(object):
    is_array = isinstance(object, list)
    if is_array:
        return len(object) > 0 and isinstance(object[0], str)
    else:
        return False

# parses the given input from a string to a JSON object
def parse_input(input):

    input_in_one_line = ""
    for input_string in input:
        input_string = input_string.strip()
        input_in_one_line = input_in_one_line + input_string

    temp = ""
    map_of_well_formed_jsons_to_key = {}
    for character in input_in_one_line:
        temp = temp + character
        try:
            temp_json = json.loads(temp)
            key = ""
            if is_valid_array(temp_json):
                key = temp_json[0]
            # add key and object to dictionary
            map_of_well_formed_jsons_to_key[key] = temp
            temp = ""
        except JSONDecodeError:
            # load throws JSONDecodeError if json is invalid
            continue

    sorted_keys = map_of_well_formed_jsons_to_key.keys()
    for key in sorted_keys:
        return map_of_well_formed_jsons_to_key[key]

# extracts the input fields from the input JSON array
def extract_initial_input_human(input_array):
    tile_index = input_array[0]
    tile_index = int(tile_index)
    degrees = input_array[1]
    rotation = int(degrees)
    starting_port = input_array[3]
    x = input_array[4]
    y = input_array[5]
    board_coordinate = convert_to_battleship(x, y)
    return tile_index, rotation, starting_port, board_coordinate

def extract_initial_input_ai(input_array):
    tile_index = input_array[0]
    tile_index = int(tile_index)
    rotation = input_array[1]
    coordinate = input_array[2]
    starting_port = input_array[3]
    return tile_index, rotation, starting_port, coordinate

def get_strategy(input_dictionary):
    strategy = input_dictionary[STRATEGY]
    return strategy

# extracts the fields from the intermediate input json
def extract_intermediate_input(input_array):
    tile_index = input_array[1]
    tile_index = int(tile_index)
    degrees = input_array[2]
    rotation = int(degrees)

    x = input_array[3]
    y = input_array[4]
    board_coordinate = convert_to_battleship(x, y)
    return tile_index, rotation, board_coordinate

# extracts the fields from the intermediate input json
def extract_intermediate_input_ai(input_array):
    tile_index = input_array[0]
    tile_index = int(tile_index)
    rotation = input_array[1]
    coordinate = input_array[2]
    return tile_index, rotation, coordinate
