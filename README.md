# Tsuro Architecture 

Authors of code: Colin McLean, Jack Wilkin, Anubhav Sharma, and Coleen Ross

The following gives an explanation on the different data structures, rules, and interfaces used throughout the project.
For further explanations on the code, refer to the markdown files in the planning/ folder. 

## turn_spec_json
turn_spec_json is the tile index, rotation, board_coordinate, and starting_port of a turn that can be executed by the game_state

ex: turn_spec_json

```
[2, 0, 'a1', 'n1']

[20, 0, 'a3']

```

## rule_check_json
rule_check_json is a dictionary that reports on the legality of a rule check

ex: rule_check_json

```
 {
  "legal" : True
  "rules broken" : None
 }
 
  {
  "legal" : True
  "rules broken" : ['coordinate is already occupied', 'starting port is invalid', 'tile placement is avoidable suicide']
 }

```

illegal first turns are:

```
     first_turn_legality = { 
         "coordinate is invalid" : invalid_coordinate, 
         "coordinate is already occupied" : is_occupied, 
         "tile placement is not on the board's edge" : doesnt_border_edge,
         "tile placement has neighbors" : has_neighbors,
         "starting port is invalid" : invalid_starting_port,
         "tile placement is avoidable suicide" : is_placement_suicide
     }
     
```

illegal intermediate turns are:

```
     intermediate_turn_legality = { 
            "coordinate is invalid" : invalid_coordinate, 
            "coordinate is already occupied" : is_occupied, 
            "tile placement is not in front of given player" : not is_correct_coordinate,
            "tile placement is avoidable suicide" : is_tile_selection_suicidal
     }
     
```
## turn_result_json
turn_result_json is a dictionary that reports on the outcome of a turn
if illegal will be a rule_check_json
if legal it will have this shape

ex: turn_result_json

```
  {
    "legal" : True,  
    "players killed": [], 
    "game over" : False 
  }
  
  {
    "legal" : True,  
    "players killed": ["white", "black"], 
    "game over" : False 
  }
  
  {
    "legal" : True,  
    "players killed": ["red"], 
    "game over" : True 
  }

```
## Game State interface

the gamestate controls all actions affecting the state of a game of tsuro.
It enacts the initial placments and the turns of the players.
Keeping reference to all the parts of the game play in this class. 

```
GameState
  - Deck        
  - Board
  - Dictionary<string, Avatar>
  - RuleChecker
  
  # checks if an initial tile placement is legal
  # tile_index -> int : 0 - 34 (represents the index in all_tiles)
  # rotation -> int : 0, 90, 180, 270 (represents the number of roations for the given tile)
  # boar_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
  # starting_port -> string : valid_port() (port on the edge of the board the player starts at)
   initial_placement_check(tile_index, rotation, board_coordinate, starting_port)
  -> returns rule_check_json
  
  # performs a players first turn, returns the validity of that turn (if not valid kills player)
  # player_color -> string : valid_color() (the color of the player making the turn)
  # tile_index -> int : 0 - 34 (represents the index in all_tiles)
  # rotation -> int : 0, 90, 180, 270 (represents the number of roations for the given tile)
  # boar_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
  # starting_port -> string : valid_port() (port on the edge of the board the player starts at)
   player_first_turn(player_color, tile_index, rotation, board_coordinate, starting_port)
  -> returns turn_result_json
  
  # checks if an players turn is legal
  # player_color -> string : valid_color() (the color of the player making the turn)
  # tile_index -> int : 0 - 34 (represents the index in all_tiles)
  # rotation -> int : 0 - 3 (represents the number of roations for the given tile)
  # board_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
  # tile_choices -> array[int] : 2 - 3 (tile options the player had to choose from)
   rule_check(player_color, tile_index, rotation, board_coordinate, tile_choices)
  -> returns rule_check_json
  
  # performs a players turn, returns the result or validity of that turn (if not valid kills player)
  # player_color -> string : valid_color() (the color of the player making the turn)
  # tile_index -> int : 0 - 34 (represents the index in all_tiles)
  # rotation -> int : 0 - 3 (represents the number of roations for the given tile)
  # boar_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
  # tile_choices -> array[int] : 2 - 3 (tile options the player had to choose from)
   player_take_turn(player_color, tile_index, rotation, board_coordinate, tile_choices)
  -> returns turn_result_json
```

## Rule Checker Interface

the rulechecker is the source of truth for the legality of a move in a game of tsuro.
the rulechecker knows the rules of a valid first turn and a player's intermediate turn.
given a 

```
   # checks the legality of an initial tile placement on a board
   # board -> Board 
   # tile -> HandTile
   # board_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
   # starting_port -> string : valid_port() (port on the edge of the board the player starts at)
    check_first_turn(board, tile, board_coordinate, starting_port)
   -> returns rule_check_json
   
   # checks the legality of an intermediate tile placement on a board for the given player
   # board -> Board 
   # tile -> HandTile
   # board_coordinate -> string : valid_cooridinate() (coordinate the tile is placed at)
   # player -> Avatar 
    check_turn(board, tile, board_coordinate, player)
   -> returns rule_check_json
   
```

## Deck Interface

The deck is in control of the tiles in a game of tsuro.
The deck can deal out tile in order or randomly.
The deck can get a tile given an index or a list of indexes. 

```

    # deals random tile indexes from the deck
    # tile_quantity -> int : number of tiles requested
     deal_random_tiles(tile_quantity)
    -> returns an array of the given size of random integers 0 - 34
    
    # deals the next tile indexes from the deck
     deal_tiles(tile_quantity)
    -> returns an array of the given size of sequential integers 0 - 34
    
    # gets a copy of the tile at the given index from the deck
    # tile_index -> int : 0 - 34
     get_tile(tile_index)
    -> returns HandTile
    
    # gets copoes of tiles from the deck based on the given indexes
    # tile_index_list -> array[int]
     get_tiles(tile_index_list)
    -> returns an array of HandTile
    
```

## Avatar Interface

Avatar represents the players location on the board. 
It knows its color, its port and tile on the board and can determine what board coordinate it connects to. 

```

    # places and avatar on the board. setting its current_port and current_tile 
    # board_coordinate -> string : valid_coordinate()
    # starting_port -> string : valid_port()
     place_avatar(board_coordinate, starting_port)
     
    # checks if player has fallen off board
     is_player_dead()
    -> returns boolean
    
    # get the board_coordinate that connects to the players current port and tile
     get_connecting_coordinate()
    -> return board_coordinate string 

```
