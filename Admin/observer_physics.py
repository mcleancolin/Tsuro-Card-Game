tile_size = 60
buffer_size = 5
board_size = 10

# calculates the start point for a horizontal line at the given index
def get_horizontal_start_point(row):
    point = (buffer_size, (row * tile_size) + buffer_size)
    return point

# calculates the end point for a horizontal line at the given index
def get_horizontal_end_point(row):
    point = (buffer_size + (board_size * tile_size), \
    (row * tile_size) + buffer_size)
    return point

# calculates the start point for a vertical line at the given index
def get_vertical_start_point(col):
    point = ((col * tile_size) + buffer_size, buffer_size)
    return point

# calculates the end point for a vertical line at the given index
def get_vertical_end_point(col):
    point = ((col * tile_size) + buffer_size, \
    buffer_size + (board_size * tile_size))
    return point

# calculates the points for drawing a square tile on the board at the given x,y
def calculate_tile_points(x,y):
    x1 = (tile_size * x) + buffer_size
    y1 = (tile_size * y) + buffer_size
    x2 = (tile_size * (x + 1)) + buffer_size
    y2 = (tile_size * (y + 1)) + buffer_size
    return x1, y1, x2, y2

# returns the coordinate of the port that the given edge is at. Used when
# drawing the edges for the start and end point of an edge
def get_point(edge, x, y):
    if(edge == 'e1'):
        return ((tile_size * (x + 1)) + buffer_size,
        (tile_size * y) + (tile_size / 3) + buffer_size)
    elif(edge == 'e2'):
        return ((tile_size * (x + 1)) + buffer_size,
        (tile_size * y) + (tile_size * (2/3)) + buffer_size)
    elif(edge == 's1'):
        return ((tile_size * x)+(tile_size / 3)+buffer_size,
        (tile_size * (y + 1)) + buffer_size)
    elif(edge == 's2'):
        return ((tile_size * x)+(tile_size * (2/3))+buffer_size,
        (tile_size * (y + 1)) + buffer_size)
    elif(edge == 'w1'):
        return ((tile_size * x) + buffer_size,
        (tile_size * y) + (tile_size / 3) + buffer_size)
    elif(edge == 'w2'):
        return ((tile_size * x) + buffer_size,
        (tile_size * y) + (tile_size * (2/3)) + buffer_size)
    elif(edge == 'n1'):
        return ((tile_size * x)+(tile_size / 3)+buffer_size,
        (tile_size * y) + buffer_size)
    elif(edge == 'n2'):
        return ((tile_size * x)+(tile_size*(2/3))+buffer_size,
        (tile_size * y) + buffer_size)

# creates a curved edge from one port to another on a tile
def get_curved_path_points(direction, x, y):
    if(direction == 'e'):
        return get_curved_path_points_east(x, y)

    if(direction == 'w'):
        return get_curved_path_points_west(x, y)
        x1 = (tile_size * x) + buffer_size

    if(direction == 'n'):
        return get_curved_path_points_north(x, y)

    if(direction == 's'):
        return get_curved_path_points_south(x, y)

# calculated the points for a path connecting both of the east ports
def get_curved_path_points_east(x, y):
    x1 = (tile_size * (x + 1)) + buffer_size
    y1 = (tile_size * y) + (tile_size / 3) + buffer_size
    x2 = (tile_size * x) + (tile_size * (2/3)) + buffer_size
    y2 = (tile_size * y) + (tile_size / 2) + buffer_size
    x3 = (tile_size * (x + 1)) + buffer_size
    y3 = (tile_size * y) + (tile_size * (2/3)) + buffer_size
    return x1, y1, x2, y2, x3, y3

# calculated the points for a path connecting both of the west ports
def get_curved_path_points_west(x, y):
    x1 = (tile_size * x) + buffer_size
    y1 = (tile_size * y) + (tile_size / 3) + buffer_size
    x2 = (tile_size * x) + (tile_size / 3)  + buffer_size
    y2 = (tile_size * y) + (tile_size / 2) + buffer_size
    x3 = (tile_size * x) + buffer_size
    y3 = (tile_size * y) + ( tile_size * (2/3)) + buffer_size
    return x1, y1, x2, y2, x3, y3

# calculated the points for a path connecting both of the north ports
def get_curved_path_points_north(x, y):
    x1 = (tile_size * x) + (tile_size / 3) + buffer_size
    y1 = (tile_size * y) + buffer_size
    x2 = (tile_size * x) + (tile_size / 2) + buffer_size
    y2 = (tile_size * y) + (tile_size / 3) + buffer_size
    x3 = (tile_size * x) + (tile_size * (2/3)) + buffer_size
    y3 = (tile_size * y) + buffer_size
    return x1, y1, x2, y2, x3, y3

# calculated the points for a path connecting both of the south ports
def get_curved_path_points_south(x, y):
    x1 = (tile_size * x) + (tile_size / 3) + buffer_size
    y1 = (tile_size * (y+1)) + buffer_size
    x2 = (tile_size * x) + (tile_size / 2) + buffer_size
    y2 = (tile_size * y) + (tile_size * (2/3)) + buffer_size
    x3 = (tile_size * x) + (tile_size * (2/3)) + buffer_size
    y3 = (tile_size * (y+1)) + buffer_size
    return x1, y1, x2, y2, x3, y3
