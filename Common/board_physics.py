from game_constants import NORTH, SOUTH, EAST, WEST, OUR_PORTS_TO_ALPHA, PORT_SIDE_TO_DIRECTION, VALID_BOARD_COLUMNS, CONNECTING_PORTS, DEGREE_TO_NUMBER_OF_ROTATIONS, board_column_number_to_letter, EDGE

################## Validity ####################################
# valid_port -- checks to make sure the port is a vlid port:
# ['n1', 'n2', 's1', 's2', 'e1', 'e2', 'w1', 'w2']
def valid_port(port):
    side = port[0]
    space = port[1:]
    valid_sides = PORT_SIDE_TO_DIRECTION.keys()
    valid_side = side in valid_sides
    valid_space = int(space) in (1, 2)
    return valid_side and valid_space

# checks to make sure the given board coordinate is valid given 10x10 board
# Columns: a - j
# Rows: 1 - 10
# coordinate -> boolean
def valid_coordinate(board_coordinate):
    given_column = board_coordinate[0]
    given_row = board_coordinate[1:]
    row_int = int(given_row)
    return (given_column in VALID_BOARD_COLUMNS) and (row_int in range(1, 11))

################## Board Physics ####################################

# port_to_side -- converts a port to the side that it is on
# port -> side
def port_to_side(port):
    port_side = port[0]
    side = PORT_SIDE_TO_DIRECTION[port_side]
    return side

# gets the opposite of the given side for a board/tile
def get_opposite_side(side):
    connecting_port = CONNECTING_PORTS[side[0]]
    return PORT_SIDE_TO_DIRECTION[connecting_port]

# given a port on a tile, return the port on the adjacent tile that a player would move to
def get_connecting_port(port):
    port_side = port[0]
    port_number = port[1]
    new_port_side = CONNECTING_PORTS[port_side]
    new_port = new_port_side + port_number
    return new_port

# returns the coordinate that connects at the given port or edge if there is none
def get_connecting_coordinate(board_coordinate, port):
    side = port_to_side(port)
    neighboring_coordinate = get_coordinate_neighbor(board_coordinate, side)
    return neighboring_coordinate

# is_edge -- is the given board coordinate an edge?
# coordinate -> boolean
def is_edge(board_coordinate):
    directions = PORT_SIDE_TO_DIRECTION.values()
    # valid coordinate & if any neighbor is EDGE
    has_edge_neighbor = any(map(lambda side: get_coordinate_neighbor(board_coordinate, side) == EDGE, directions))
    return valid_coordinate(board_coordinate) and has_edge_neighbor

# returns boardcoordinate that is the neighbor of the given
# coordinate on the given side
def get_coordinate_neighbor(coordinate, side):
    column = coordinate[0]
    row = coordinate[1:]

    # Converts lowercase letter to its column number (1 indexed)
    column_int = ord(column) - 96
    row_int = int(row)

    coordinate_template = '{0}{1}'

    if side == NORTH and row_int != 1:
        return coordinate_template.format(column, row_int - 1)

    elif side == SOUTH and row_int != 10:
        return coordinate_template.format(column, row_int + 1)

    elif side == EAST and column_int != 10:
        new_column = chr(column_int + 1 + 96)
        return coordinate_template.format(new_column, row)

    elif side == WEST and column_int != 1:
        new_column = chr(column_int - 1 + 96)
        return coordinate_template.format(new_column, row )

    else:
        return EDGE

def do_coordinates_neighbor(board_coordinate, potential_neighbor):
    valid_sides = PORT_SIDE_TO_DIRECTION.keys()
    does_neighbor = False
    for side in valid_sides:
        if get_coordinate_neighbor(board_coordinate, side) == potential_neighbor:
            does_neighbor = True
    return does_neighbor

# returns all the edge coordinates on the board clockwise from a1
def get_all_edge_coordinates():
    edge_coordinates = []

    for column in VALID_BOARD_COLUMNS:
        north_edge = column + "1"
        edge_coordinates.append(north_edge)

    for row in range(2, 10):
        east_edge = "j" + str(row)
        edge_coordinates.append(east_edge)

    for column in VALID_BOARD_COLUMNS[::-1]:
        south_edge = column + "10"
        edge_coordinates.append(south_edge)

    for row in range(2, 10)[::-1]:
        west_edge = "a" + str(row)
        edge_coordinates.append(west_edge)

    return edge_coordinates

################## Conversions ####################################

# gets the number of rotations for a specific degree
# int -> int
def get_number_of_rotations(degree):
    degree = int(degree)
    number_of_rotations = DEGREE_TO_NUMBER_OF_ROTATIONS[degree]
    return number_of_rotations

# gets the letter of the corresponding x coord number
def column_number_to_letter(number):
    letter = board_column_number_to_letter[number]
    return letter

# Convert from board_coordinate to cardinal
# returns x, y values of the board_coordinate
# x and y are 0 indexed
def board_coordinate_to_cardinal(board_coordinate):
    column = board_coordinate[0]
    row = board_coordinate[1:]

    x_int = ord(column) - 97
    y_int = int(row) - 1 

    return x_int, y_int

# Convert from cardinal to board_coordinate
# returns board_coordinate that corresponds to given, x y 
# x and y are 0 indexed
def cardinal_coordinate_to_board(x, y):
    column = chr(x + 97)
    row = str(y + 1)

    board_coordinate = column + row
    return board_coordinate

# converts a port from our representation to alpha and vise versa
def convert_port_string(port_string):
    our_ports = list(OUR_PORTS_TO_ALPHA.keys()) 
    alpha_ports = list(OUR_PORTS_TO_ALPHA.values()) 

    if port_string in our_ports:
        return OUR_PORTS_TO_ALPHA[port_string]
    elif port_string in alpha_ports:
        return our_ports[alpha_ports.index(port_string)]
    else:
        return "invalid port string"
       