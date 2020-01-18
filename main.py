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
image = PIL.Image.new('RGB', (CELL_SIZE, CELL_SIZE), (255, 0, 0))
textures.append(arcade.Texture(str((255, 0, 0)), image=image))

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

        self.last_score = 0

        self.is_game_over = False

        self.field = []

        self.expand = 0
        self.change_direction = 0
        self.last_direction = 0

        self.frame_count = 0

        self.length = 0

    def setup(self):
        self.board_sprite_list = arcade.SpriteList()

        self.field = [[0] * COLUMNS for _ in range(ROWS)]
        self.field[random.randint(0, ROWS-1)][random.randint(0, COLUMNS-1)] = -1

        self.field[ROWS // 2][COLUMNS // 2] = 1

        self.expand = 3
        self.change_direction = 1
        self.last_direction = 1

        self.frame_count = 0

        self.length = 1

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

        # UP
        if self.change_direction == DIRECTION_UP:
            if head[0] == 0 or self.field[head[0] - 1][head[1]] > 0:
                self.game_over()
                return

            if self.field[head[0] - 1][head[1]] < 0:
                self.ate_apple()
            self.field[head[0] - 1][head[1]] = self.field[head[0]][head[1]] + 1

        # RIGHT
        if self.change_direction == DIRECTION_RIGHT:
            if head[1] == COLUMNS - 1 or self.field[head[0]][head[1] + 1] > 0:
                self.game_over()
                return

            if self.field[head[0]][head[1] + 1] < 0:
                self.ate_apple()
            self.field[head[0]][head[1] + 1] = self.field[head[0]][head[1]] + 1

        # DOWN
        if self.change_direction == DIRECTION_DOWN:
            if head[0] == ROWS - 1 or self.field[head[0] + 1][head[1]] > 0:
                self.game_over()
                return

            if self.field[head[0] + 1][head[1]] < 0:
                self.ate_apple()
            self.field[head[0] + 1][head[1]] = self.field[head[0]][head[1]] + 1

        # LEFT
        if self.change_direction == DIRECTION_LEFT:
            if head[1] == 0 or self.field[head[0]][head[1] - 1] > 0:
                self.game_over()
                return

            if self.field[head[0]][head[1] - 1] < 0:
                self.ate_apple()
            self.field[head[0]][head[1] - 1] = self.field[head[0]][head[1]] + 1

        if self.expand == 0:
            for i in range(len(self.field)):
                for j in range(len(self.field[0])):
                    if self.field[i][j] > 0:
                        self.field[i][j] -= 1
        else:
            self.expand -= 1
            self.length += 1

        self.last_direction = self.change_direction

        self.update_board()

    def ate_apple(self):
        self.expand += 1
        new_i = random.randint(0, ROWS - 1)
        new_j = random.randint(0, COLUMNS - 1)

        while not self.field[new_i][new_j] == 0:
            new_i = random.randint(0, ROWS - 1)
            new_j = random.randint(0, COLUMNS - 1)

        self.field[new_i][new_j] = -1

    def on_update(self, dt):
        if not self.is_game_over:
            self.frame_count += 1
            if self.frame_count % 12 == 0:
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

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.is_game_over:
            self.is_game_over = False

    def update_board(self):
        for row in range(len(self.field)):
            for column in range(len(self.field[0])):
                v = self.field[row][column]
                i = row * COLUMNS + column
                self.board_sprite_list[i].set_texture(min(v, 1))

    def on_draw(self):
        arcade.start_render()
        if not self.is_game_over:
            self.board_sprite_list.draw()
            arcade.draw_text(f"Score: {self.length}.", 5, 5, arcade.color.WHITE_SMOKE, 16)
        else:
            arcade.draw_text("Game Over.",
                             WIDTH // 4, HEIGHT // 2 + 40, arcade.color.RED, 60, width=WIDTH // 2, align="center",
                             font_name='GARA')

            arcade.draw_text(f"Score: {self.last_score}.",
                             WIDTH // 4, HEIGHT // 2 - 50, arcade.color.WHITE_SMOKE, 24, width=WIDTH // 2, align="center",
                             font_name='GARA')

            arcade.draw_text("Click to restart.",
                             WIDTH // 4, HEIGHT // 2 - 130, arcade.color.WHITE_SMOKE, 28, width=WIDTH // 2, align="center",
                             font_name='GARA')

    def game_over(self):
        self.last_score = self.length
        self.is_game_over = True
        self.setup()


def main():
    win = Game()
    win.setup()
    arcade.run()


if __name__ == "__main__":
    main()
