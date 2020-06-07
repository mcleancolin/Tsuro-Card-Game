# Player Interface

This is a description of the interface representing the component for a player
in a game of Tsuro.

## Fields

<ol>

<li> String color: represents the color of this player</li>

<li> List of Tiles tiles: represents the tiles that the player has</li>

<li> BoardTile current_tile: represents the tile on the board that this player is currently occupying</li>

<li> String current_port: represents the current port that the player is occupying. Port must be one of the following: N1, N2, E1, E2, S1, S2, W1, W2.</li>

</ol>

## Methods

**place_avatar(board_coordinate, starting_port): board_coordinate, starting_port -> void**  <br/>
Updates the current_tile field of this player to match the given tile coordinate. Updates the current_port field of this player to match the given port. This method is called whenever this player's avatar must continue along a path of a tile placed in front of it.

**recieve_tiles(tiles): tiles -> void** <br/>
Updates the tiles field of this player to represent the player receiving tiles for their turn. This is called when this player is notified when it is there turn.

**rotate_tile(tile, degrees):** tile, degrees -> tile <br/>
Rotates the given tile from this player's list of tiles by the number of degrees (clockwise) that this player specifies. Returns the updated rotated tile.

**choose_tiles(): void -> void** <br/>
Chooses a tile in this player's list of tiles to play on the board.

**send_to_referee(tile, coordinate): tile, coordinate -> void** <br/>
Sends the decision of the choosing of a tile to the referee in order to perform the desired move.
