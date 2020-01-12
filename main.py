"""
Snake Game in Python arcade
"""

import random
import arcade
import math
import PIL
from PIL import Image

random.seed()

DIRECTION_UP = 1
DIRECTION_RIGHT = 2
DIRECTION_DOWN = -1
DIRECTION_LEFT = -2

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 50

ROWS = math.floor(HEIGHT / CELL_SIZE)
COLUMNS = math.floor(WIDTH / CELL_SIZE)

print(ROWS)
print(COLUMNS)

textures = []
image = PIL.Image.new('RGB', (CELL_SIZE, CELL_SIZE), (0, 0, 0))
textures.append(arcade.Texture(str((0, 0, 0)), image=image))
textures.append(arcade.load_texture("res/snake.jpg", scale=CELL_SIZE / Image.open("res/snake.jpg").size[1]))


def max2d_i(arr):
    max_i = 0
    max_j = 0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[max_i][max_j] < arr[i][j]:
                max_i = i
                max_j = j

    return max_i, max_j


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Snake")
        arcade.set_background_color(arcade.color.BLACK)
        self.board_sprite_list = None

        self.field = []

        self.expand = 3
        self.change_direction = 1
        self.last_direction = 1

        self.frame_count = 0

    def setup(self):
        self.board_sprite_list = arcade.SpriteList()

        self.field = [[0] * COLUMNS for _ in range(ROWS)]
        self.field[random.randint(2, ROWS-3)][random.randint(2, COLUMNS-3)] = 1

        for i in self.field:
            print(i)

        for row in range(len(self.field)):
            for column in range(len(self.field[0])):
                sprite = arcade.Sprite()
                for texture in textures:
                    sprite.append_texture(texture)
                sprite.set_texture(0)
                sprite.center_x = CELL_SIZE * column + CELL_SIZE // 2
                sprite.center_y = HEIGHT - CELL_SIZE * (row + 1) + CELL_SIZE // 2

                self.board_sprite_list.append(sprite)
        self.update_board()

    def move(self):
        head = max2d_i(self.field)

        if self.change_direction == DIRECTION_UP:
            self.field[head[0] - 1][head[1]] = self.field[head[0]][head[1]] + 1
        if self.change_direction == DIRECTION_RIGHT:
            self.field[head[0]][head[1] + 1] = self.field[head[0]][head[1]] + 1
        if self.change_direction == DIRECTION_DOWN:
            self.field[head[0] + 1][head[1]] = self.field[head[0]][head[1]] + 1
        if self.change_direction == DIRECTION_LEFT:
            self.field[head[0]][head[1] - 1] = self.field[head[0]][head[1]] + 1

        if self.expand == 0:
            for i in range(len(self.field)):
                for j in range(len(self.field[0])):
                    if self.field[i][j] > 0:
                        self.field[i][j] -= 1
        else:
            self.expand -= 1

        self.last_direction = self.change_direction

        self.update_board()

    def on_update(self, dt):
        self.frame_count += 1
        if self.frame_count % 20 == 0:
            self.move()
            print(self.change_direction)
            self.frame_count = 0

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP and self.last_direction != DIRECTION_DOWN:
            self.change_direction = DIRECTION_UP
        elif key == arcade.key.RIGHT and self.last_direction != DIRECTION_LEFT:
            self.change_direction = DIRECTION_RIGHT
        elif key == arcade.key.DOWN and self.last_direction != DIRECTION_UP:
            self.change_direction = DIRECTION_DOWN
        elif key == arcade.key.LEFT and self.last_direction != DIRECTION_RIGHT:
            self.change_direction = DIRECTION_LEFT

    def update_board(self):
        for row in range(len(self.field)):
            for column in range(len(self.field[0])):
                v = self.field[row][column]
                i = row * COLUMNS + column
                self.board_sprite_list[i].set_texture(min(v, 1))

    def on_draw(self):
        arcade.start_render()
        self.board_sprite_list.draw()


def main():
    win = Game()
    win.setup()
    arcade.run()


if __name__ == "__main__":
    main()
