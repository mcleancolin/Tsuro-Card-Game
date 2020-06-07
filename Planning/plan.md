# Part 1

## Components
Player
  - string: color (either white, black, red, green, blue)
  - array[2]: tiles (array of max size 2 full player's handtiles)
  - string: current_tile (cartesian coordinates on the board)
  - string: current_port (port on the current_tile)

Tile
A tile has four sides: north, south, east, west
and eight ports: n1, n2, s1, s2, e1, e2, w1, w2
A tile also has four paths, which are tuples of all of the ports (ex. [n1, e2])
they must be pairwise distinct, and all ports must be represented in the paths.

Handtile
Extends Tile
  - rotate(): handtile -> handtile; rotates a handtile by 90, 180, or 270 degrees

Boardtile
Extends Tile
A board tiles has four neighbors: north, south, east, west
A neighbor can be another tile, the edge of the board, or null.

Board
  - dictionary of Tiles: tiles mapped to board location (cartesian coordinates on the board)
  - place_tile(): handtile, location on the board -> add tile to list of board tiles and update all neighbors
  - move_player(): move players along new paths created once a tile is placed

# Part 2

A new player would be generated when someone connects to the server. The player will be assigned one of the five colors. When all players have joined, a game will start.

Players will pick their starting port, and then will be dealt 3 cards. The first person to join the game will start first. A turn is placing a tile on the cartesian coordinate that neighbors the side of the tile the player's avatar is on.
For example, if a player is at cartesian coordinate A2, port S1, a tile can only be placed at cartesian coordinate B2. (like battleship cartesian coordinates)

Moving a piece would require checking the neighbor of the side the player is on (if the player is on port w1, check the west neighbor's e1 port). North ports correspond to south ports and east ports correspond to west ports. The player moves from their current port to the corresponding port on the neighboring tile. They then move along the path of that tile (the path tuple); once they reach the new port on the new tile, check for neighbors. If there is a neighbor, iterate through the same process. If the neighbor is the edge of the board, the player LOSES.
