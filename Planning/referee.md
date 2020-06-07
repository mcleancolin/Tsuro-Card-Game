# Referee Interface

This is a description of the interface representing the component for a referee
in a game of Tsuro.

## Fields

List of Tiles deck: list of the Tsuro game tiles

Board board: reference to the Board object of the current game

Dictionary<Session ID, Player> players: dictionary containing the players in the current game with the key as the unique session id (time of entering the game) and the value being the player object that represents that player

List of String colors: list of the five possible player colors


## Methods

**add_player(): void -> void** <br/>
Adds a player to the players field with the session ID as a timestamp of when the player joined the game.

**create_game(): void -> void** <br/>
Initializes a new game with the current list of players. Starts by calling the start_game() method, then loops over all of the player to notify them when it is their turn, and then calls the end_game method when the game is finished and a winner is determined.

**start_game(): void -> void** <br/>
Conducts the first round of the game when each player is on the edge of the board. Calls the first_turn method in the board class and sends this method the player, tile, coordinate, and starting_port.

**take_turn(player): player -> void** <br/>
Requests turns from the given player by asking them for input.

**execute_turn(tile, coordinate, player): tile, coordinate, player -> void** <br/>
Executes placing the given tile on the board for the given player at the given coordinate by calling the take_turn method in the board class.

**notify_players(): void -> void** <br/>
Loops through all of the players in the current game and updates them about the current state of the game.

**end_game(): void -> void** <br/>
Signals the end of the game and announces who the winner is.
