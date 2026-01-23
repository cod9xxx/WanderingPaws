import random
import arcade

from first_island import PlayerCharacter

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "second level"

PLAYER_MOVEMENT_SPEED = 4
RIGHT_FACING = 0
LEFT_FACING = 1
UP_FACING = 2
DOWN_FACING = 3
UPDATES_PER_FRAME = 10


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
        self.start_music = arcade.load_sound("sounds/dialogue.mp3")
        self.music_player = arcade.play_sound(self.start_music, loop=True)

        self.collision = None
        self.scene = None
        self.player_sprite = None

        self.physics_engine = None

        self.camera = None

        self.tile_map = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.camera = arcade.Camera2D()

        map_name = r'tilemaps\2_island.tmx'

        # collision
        layer_options = {
            "collision": {"use_spatial_hash": True, }
        }

        try:
            self.tile_map = arcade.load_tilemap(map_name, scaling=3, layer_options=layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
        except Exception as e:
            print(f"Критическая ошибка при загрузке карты: {e}")
            return

        self.collision = self.scene.get_sprite_list("collision")
        if self.collision:
            self.collision.visible = False

        self.player_sprite = PlayerCharacter()

        self.player_sprite.center_x = 1500
        self.player_sprite.center_y = 650

        self.scene.add_sprite("Player", self.player_sprite)

        if self.collision is None:
            print("Внимание: Слой 'collision' не найден в Tiled.")
            self.collision = arcade.SpriteList()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            self.collision,
        )

    def on_draw(self):
        self.clear()

        self.camera.use()

        if self.scene:
            self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        if self.physics_engine:
            self.physics_engine.update()

        self.player_sprite.update_animation(delta_time)

        # camera
        self.camera.position = self.player_sprite.position


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
