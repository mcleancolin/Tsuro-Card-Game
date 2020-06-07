The Referee will be the mediator between all components of the game.
A referee class is instantiated when the server is started. None of the fields are populated until the create_game method is called. This will create an instance of the player, board, and tile classes, and add them to the game.

Referee Class
  - Board: game_board (representaiton of the state of the board)
  - Array<Tiles>: deck (35 possible tiles)
  - array<Players>: players (minimum 3, maximum 5)
  - dictionary: player_map (a player's session ID mapped to player)
  - current_turn: session id of a player

  create_game(): generates players based on who joined
  
  start_game(): starts the first turn of player 1; begin the iteration of turns
  
  take_turn(player_id): takes the player's session id to allow player to rotate hand tile and place tile on board. at the end, it switches the turn to the next player
    - ex. referee.take_turn() -> player.rotate() -> board.place_tile()
    
  end_game(): announce the winner(s) and close the connection

Referencing our initial plan for the board:
  - dictionary of Tiles: tiles mapped to board location (cartesian coordinates on the board)
  - place_tile(): handtile, location on the board -> add tile to list of board tiles and update all neighbors
    - place_tiles converts a handtile to a boardtile, which finalizes it's ports into the grid structure described below.
      as hand tiles rotate, the position of north, south, east, and west will change, but once converted to board tiles those positions will be finalized to line up with the north, south, east, and west sides of the board.
  - move_player(): move players along new paths created once a tile is placed

Each tile on the board is located by battleship coordinates: A-J for the columns and 1-10 for the rows. 

```
 ___________________________
|        |        |        |
|   A1   |   B1   |   C1   |
|________|________|________|
|        |
|   A2   |
|________|
|        |
|   A3   |
|________|

```

Ports are lined up like magnets; opposites connect to each other (n1 connects to s1, n2 connects to s2, e1 connects to w1, etc.)
When placed on the board, ports on tiles will map to these exactly. The graph will be traversed using these ports as nodes and by looking at their board tile's neighboring nodes.

```
       s1  s2
     ___|__|___ 
    |          |
e1 -           |
    |    A1    |
e2 -           |
    |__________|
          
     __________ 
    |          |
e1 -           |
    |    A3    |
e2 -           |
    |__________|
    
     __________ 
    |          |
    |          - w1
    |    J10   |
    |          - w2
    |___|___|__|
       n1   n2
  
```
