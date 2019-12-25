"""
Snake Game in Python arcade
"""

import random
import arcade
import math

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 50

ROWS = math.floor(HEIGHT / CELL_SIZE)
COLUMNS = math.floor(WIDTH / CELL_SIZE)


class SnakePart(arcade.Sprite):
    def __init__(self):
        super().__init__("res/snake.jpg")
        self.scale = CELL_SIZE / self.height


class Game(arcade.Window):
    direction = 1

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Snake")
        arcade.set_background_color(arcade.color.BLACK)
        self.field = []

    def setup(self):
        self.field = [[0] * COLUMNS] * ROWS
        self.field[random.randint(0, ROWS)][random.randint(0, COLUMNS)] = 1

    def on_draw(self):
        arcade.start_render()

    def move(self):
        for i in range(0, ROWS):
            for j in range(0, COLUMNS):
                if self.field[i][j] > 0:
                    pass


    def on_update(self, dt):
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.frame_count = 0


def main():
    win = Game()
    win.setup()
    arcade.run()


if __name__ == "__main__":
    main()
