# Rule Checker
The Rule Checker will decide the legality of a move in the game. The referee must use the Rule Checker, but a player may or may not use it to check if its move is allowed. The methods that check for validity will return true for a valid move, false for an invalid move. If the Rule Checker finds that a player is breaking a rule, that player will be disqualified and removed from the game.

## Rule Checker Class

valid_coordinate(): (coordinate -> boolean) ensures a given coordinate is valid considering a 10x10 board size.

A coordinate is valid if:
  - columns are valid if coordinates begin with letters A - J
  - rows are valid if coordinates end with numbers 1-10

is_edge(): (coordinate -> boolean) decides if the given board coordinate is an edge by checking it's neighbors.

port_to_side(): (port -> side) converts a given port to the side that port is on. for example, given "n1", it would return "north"

valid_port(): (board, board_coordinate, starting_port -> boolean) checks to make sure the player has chosen a valid starting port (must be on an edge of an edge tile).


### Turn Validity
The rules for the first turn of the game are more strict than in succeeding turns, so there are different methods for checking validity.

check_first_turn(): (board, coordinate, player -> boolean) decides if the turn was valid - only to be used during the first turn of the game.

A first turn is valid if the tile:
  - does not neighbor other tiles
  - is placed on the edge of the board
  - is placed in front of the port the player is on ("where the avatar does not occupy a port that faces the board’s interior")

check_turn(): (board, coordinate, player -> boolean) decides if a turn was valid - not to be used on first turns. A turn is valid if the tile is placed in front of the player.

