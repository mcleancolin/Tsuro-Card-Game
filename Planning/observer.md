# Observing Component

Component in control of rendering the current state of a Referee (game manager).

- Displays the state of a game as it waits for players to join. 
- Displays an ongoing game
  - Current state of the Board
      - Tiles: paths and placements
      - Players: colors and locations
      
- Displays and ended game
  - shows the winners
  - shows the loosers
  
Observing Method
  
  takes a referee object and renders its current state 
  ```
  observe_game_state(referee)
  ```
  
Public Methods that render before, during, and after a game
```
  # draws the players that have asked to join a game before it starts
  # could potentially contain an interface to initiate start of game
  draw_waiting_room(players)
  
  # draws the state of an ongoing game given:
  # the board, current live players, and player whos turn it is
  draw_ongoing_game(board, players, current_player)
  
  # displays the names of who won and who lost
  # could potentially contain an interface to exit or start a new game
  draw_game_over(winners, loosers)
  ```
  
  Likely implementation specfic helper methods
  
  ```
    draw_tile(tile, ...)
    
    draw_board(board, ...)
    
    draw_player(player, ...)
  ```
