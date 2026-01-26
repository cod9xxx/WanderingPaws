import random
import arcade

from fade_class import FadeView


class PlayerCharacter(arcade.Sprite):
    def __init__(self, updates_per_frame):
        super().__init__(scale=0.1)

        self.UPDATES_PER_FRAME = updates_per_frame

        self.character_face_direction = 0  # 0 - right, 1 - left, 2 - up, 3 - down
        self.cur_frame = 0

        self.step_sounds = [
            arcade.load_sound("sounds/sand_steps/1.mp3"),
            arcade.load_sound("sounds/sand_steps/2.mp3"),
            arcade.load_sound("sounds/sand_steps/3.mp3"),
            arcade.load_sound("sounds/sand_steps/4.mp3"),
            arcade.load_sound("sounds/sand_steps/5.mp3")
        ]
        self.step_timer = 0
        self.step_interval = 0.35

        main_path = "images/cat_animation/"

        self.idle_texture = arcade.load_texture(f"{main_path}cat.png")
        self.texture = self.idle_texture

        self.down_textures = [
            arcade.load_texture(f"{main_path}forward1.png"),
            arcade.load_texture(f"{main_path}forward2.png")
        ]

        self.up_textures = [
            arcade.load_texture(f"{main_path}back1.png"),
            arcade.load_texture(f"{main_path}back2.png")
        ]

        self.right_textures = [
            arcade.load_texture(f"{main_path}right1.png"),
            arcade.load_texture(f"{main_path}right2.png"),
            arcade.load_texture(f"{main_path}right3.png")
        ]

        self.left_textures = []
        for texture in self.right_textures:
            self.left_textures.append(texture.flip_left_right())

    def update_animation(self, delta_time: float = 1 / 60):

        is_moving = self.change_x != 0 or self.change_y != 0
        if not is_moving:
            self.texture = self.idle_texture
            self.scale = 0.09
            self.step_timer = self.step_interval
            return
        else:
            self.scale = 0.1

        # step sound
        self.step_timer += delta_time
        if self.step_timer >= self.step_interval:
            arcade.play_sound(random.choice(self.step_sounds), volume=0.2)
            self.step_timer = 0

        # direction
        if self.change_x < 0:
            self.character_face_direction = 1  # Left
        elif self.change_x > 0:
            self.character_face_direction = 0  # Right
        elif self.change_y > 0:
            self.character_face_direction = 2  # Up
        elif self.change_y < 0:
            self.character_face_direction = 3  # Down

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture
            return

        # frame updates
        self.cur_frame += 1

        if self.character_face_direction == 2:
            textures = self.up_textures
        elif self.character_face_direction == 3:
            textures = self.down_textures
        elif self.character_face_direction == 1:
            textures = self.left_textures
        else:
            textures = self.right_textures

        frame_index = (self.cur_frame // self.UPDATES_PER_FRAME) % len(textures)
        self.texture = textures[frame_index]


class IslandLevel(FadeView):
    def __init__(self, map_name):
        super().__init__()
        self.start_music = arcade.load_sound("sounds/sunshine.mp3")
        self.music_player = arcade.play_sound(self.start_music, volume=0.3, loop=True)

        self.updates_per_frame = 10
        self.map_name = map_name
        self.player_movement_speed = 4

        self.collision = None
        self.scene = None
        self.player_sprite = None

        self.physics_engine = None

        self.camera = None

        self.tile_map = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.camera = arcade.Camera2D()

        # collision
        layer_options = {
            "collision": {"use_spatial_hash": True, }
        }

        try:
            self.tile_map = arcade.load_tilemap(self.map_name, scaling=3, layer_options=layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)

        except Exception as e:
            print(f"Критическая ошибка при загрузке карты: {e}")
            return

        self.collision = self.scene.get_sprite_list("collision")
        if self.collision:
            self.collision.visible = False

        self.player_sprite = PlayerCharacter(self.updates_per_frame)

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
            self.scene.draw(pixelated=True)

        self.draw_fade()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = self.player_movement_speed
        elif key == arcade.key.S:
            self.player_sprite.change_y = -self.player_movement_speed
        elif key == arcade.key.A:
            self.player_sprite.change_x = -self.player_movement_speed
        elif key == arcade.key.D:
            self.player_sprite.change_x = self.player_movement_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.physics_engine:
            self.physics_engine.update()

        self.player_sprite.update_animation(delta_time)

        # camera
        self.camera.position = self.player_sprite.position