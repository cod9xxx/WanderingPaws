import random
import arcade

from basic_level_logic import *

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "third level"

PLAYER_MOVEMENT_SPEED = 4
RIGHT_FACING = 0
LEFT_FACING = 1
UP_FACING = 2
DOWN_FACING = 3
UPDATES_PER_FRAME = 10

MAP_NAME = "tilemaps/3_island.tmx"

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MAP_NAME, UPDATES_PER_FRAME, PLAYER_MOVEMENT_SPEED)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()