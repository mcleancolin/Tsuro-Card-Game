Player-Referee Interaction Sketch

To see examples of turn_spec_json, turn_result_json, rule_check_json go to the README.md in the Tsuro Directory.

```
GameState            Referee                 Player 1                ... Player N
|                       |                                                   starting server on <address:port>
|                       |<----------------------                            client: <player_name>
.                       .                       .                        .
|                       |<----------------------|                        |  Added <player_name> to the game.
|                       |---------------------->|                        |  Joined game as color: <player_color>
.                       .                       .                        .  occurs 2-4 more times based on # of players 
|                       |                       |                        |
|                       |-----------------------|----------------------->|  The players in the game are [<player_1_name>..., <player_n_name>]
|                       |---------------------->|                        |  First Turn: Your tiles are: [tile_choices]
|                       |<----------------------|                        |  turn: {"name": <player_name>, "strategy": <player_strategy>}
|<----------------------|                       |                        |  send <strategy> string
|---------------------->|                       |                        |  returns <turn_spec_json>
|<----------------------|                       |                        |  sends <turn_spec_json>
|---------------------->|                       |                        |  returns <turn_result_json>
|                       |---------------------->|                        |  Turn request was legal: turn response: <turn_result_json>
.                       .                       .                        .  occurs for all legal moves 
|                       |                       |                        |
|                       |---------------------->|                        |  Next Turn: Your tiles are: [tile choices]
|                       |<----------------------|                        |  Turn: <turn_spec_json>
|<----------------------|                       |                        |  send <strategy> string
|---------------------->|                       |                        |  returns <turn_spec_json>
|<----------------------|                       |                        |  sends <turn_spec_json>
|---------------------->|                       |                        |  returns illegal <rule_check_json>
|                       |---------------------->|                        |  You're kicked out from performing an illegal move: <rules_broken>
.                       .                       .                        .  occurs for all illegal moves
|                       |                       |                        |
|                       |---------------------->|                        |  Next Turn: Your tiles are: [tile choices]
|                       |<----------------------|                        |  Turn: <turn_spec_json>
|<----------------------|                       |                        |  send <strategy> string
|---------------------->|                       |                        |  eturns <turn_spec_json>
|<----------------------|                       |                        |  sends <turn_spec_json>
|---------------------->|                       |                        |  returns <turn_result_json> with players_killed > 0
|                       |---------------------->|----------------------->|  You've fallen of the board
.                       .                       .                        .  occurs when a player reaches the edge of the board 
|                       |-----------------------|----------------------->|  The game has now finished. 
|                       |-----------------------|----------------------->|  The winner is: <player_name>

```
