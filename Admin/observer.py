#!/usr/bin/env python3

import json, sys, socket, pickle
from tkinter import Tk, Canvas, Frame, BOTH
sys.path.append('../runtime-terror/Tsuro/Common')
from game_state import GameState
from board_physics import board_coordinate_to_cardinal
import observer_physics


class Observer(Frame):
    tile_color = "#CC9966"
    edge_color = "#654321"
    edge_width = 2
    player_avatar_size = 4

    def __init__(self):
        self.root = Tk()
        self.root.geometry("800x800")
        super().__init__()

    def observe_game_state(self, game_state):
        self.create_canvas()
        self.draw_board(game_state)
        self.root.mainloop()

    # creates a canvas for tkninter to draw on
    def create_canvas(self):
        self.master.title("Tiles")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)

    # draws the given list of tiles
    # tile_list  -> canvas
    def draw_board(self, game_state):
        self.draw_tiles(game_state)
        self.draw_horizontal_lines()
        self.draw_vertical_lines()
        self.draw_players(game_state)

    # draws the horizontal lines of the board grid
    def draw_horizontal_lines(self):
        for row in range(0, 11):
            first_point = observer_physics.get_horizontal_start_point(row)
            second_point = observer_physics.get_horizontal_end_point(row)
            self.canvas.create_line(first_point[0], first_point[1], \
            second_point[0], second_point[1], fill=self.edge_color, width = 2)

    # draws the vertical lines of the board grid
    def draw_vertical_lines(self):
        for col in range(0, 11):
            first_point = observer_physics.get_vertical_start_point(col)
            second_point = observer_physics.get_vertical_end_point(col)
            self.canvas.create_line(first_point[0], first_point[1], \
            second_point[0], second_point[1], fill=self.edge_color, width = 2)

    # draws the given list of tiles
    # tile_list  -> canvas
    def draw_tiles(self, game_state):
        tiles_on_board = game_state.board.tiles
        for coordinate in tiles_on_board:
            tile = tiles_on_board[coordinate]
            edges = tile.paths
            x, y = board_coordinate_to_cardinal(coordinate)
            self.draw_square(x, y)
            self.draw_edges(edges, x, y)
        self.canvas.pack(fill=BOTH, expand=1)

    #  create a square on the canvas at the given coordinates
    def draw_square(self, x, y):
        x1, y1, x2, y2 = observer_physics.calculate_tile_points(x,y)
        self.canvas.create_rectangle(x1, y1, x2, y2, \
        outline=self.edge_color, fill=self.tile_color, width=self.edge_width)

    # draws the given edges of a tile on the given canvas at the given x coord
    def draw_edges(self, edges, x, y):
        for e in edges:
            if(e[0][0] == e[1][0]):
                self.create_curved_path(e[0][0], x, y)
            first_point = observer_physics.get_point(e[0], x, y)
            second_point = observer_physics.get_point(e[1], x, y)
            self.canvas.create_line(first_point[0], first_point[1], \
            second_point[0], second_point[1], fill=self.edge_color, width = 2)

    # creates a curved edge from one port to another on a tile
    def create_curved_path(self, direction, x, y):
        x1,y1,x2,y2,x3,y3 = observer_physics.get_curved_path_points(direction, x, y)
        self.canvas.create_line(x1,y1,x2,y2,x3,y3, \
        smooth = 'true', width = 2, fill=self.edge_color)

    # draws all of the players at their ports
    def draw_players(self, game_state):
        for player_color in game_state.get_living_players():
            player = game_state.player_dictionary[player_color]
            self.draw_player(player)

    # draws one players avatar on the canvas
    def draw_player(self, player):
        x, y = board_coordinate_to_cardinal(player.current_tile)
        avatar_location = observer_physics.get_point(player.current_port, x, y)
        self.create_circle(avatar_location[0], avatar_location[1], \
        self.player_avatar_size, player.color)

    # creates a circle on the canvas at the given x and y with the given radius r
    def create_circle(self, x, y, r, color):
        self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=self.edge_color, \
        fill=color, width=2)

def main():
    game_state = GameState()
    game_state.player_first_turn("white", 0, 0, "c10", "s1")
    game_state.player_first_turn("black", 1, 0, "d1", "n1")
    game_state.player_take_turn("white", 31, 0, "c9", [0,25])
    observer = Observer()
    observer.observe_game_state(game_state)

if __name__ == '__main__':
    main()
