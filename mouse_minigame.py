import arcade
import random
import math

from constants import *
from fade_class import FadeView

SCREEN_TITLE = "Лови мышей!"

GAME_TIME = 30
MICE_NEEDED_FOR_WIN = 10
STARS = {10: 1, 15: 2, 20: 3}

HOLE_SIZE = 40
MOUSE_SIZE = 30
CAT_SIZE = 60

MOUSE_SCALE = 0.15
MOUSE_ANIM_SPEED = 0.2

class Mouse(arcade.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, speed=400):
        super().__init__("images/minigame1/mouse.png", scale=MOUSE_SCALE)

        self.mouse_texture1 = arcade.load_texture("images/minigame1/mouse1.png")
        self.frames = [self.texture, self.mouse_texture1]

        self.cur_frame_index = 0
        self.time_since_last_frame = 0

        # параметры движения
        self.center_x = start_x
        self.center_y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.speed = speed
        self.traveled = 0
        self.total_distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5

    def update(self, delta_time):
        if self.total_distance == 0:
            return

        distance_per_frame = self.speed * delta_time
        self.traveled += distance_per_frame
        progress = min(self.traveled / self.total_distance, 1.0)

        self.center_x = self.start_x + (self.end_x - self.start_x) * progress
        self.center_y = self.start_y + (self.end_y - self.start_y) * progress

        dx = self.end_x - self.start_x
        dy = self.end_y - self.start_y
        angle = math.atan2(dy, dx)
        angle_deg = math.degrees(angle)

        angle_deg = angle_deg % 360
        if angle_deg > 180:
            angle_deg -= 360
        elif angle_deg < -180:
            angle_deg += 360

        self.angle = angle_deg * -1

        self.time_since_last_frame += delta_time
        if self.time_since_last_frame >= MOUSE_ANIM_SPEED:
            self.time_since_last_frame = 0
            self.cur_frame_index = (self.cur_frame_index + 1) % 2
            self.texture = self.frames[self.cur_frame_index]

        if progress >= 1.0:
            self.kill()


class MouseMinigame(FadeView):
    def __init__(self):
        super().__init__()

        self.cur_game = None
        self.complete = False
        self.start_music = arcade.load_sound("sounds/mario.mp3")
        self.music_player = arcade.play_sound(self.start_music, loop=True)

        self.all_sprites_list = arcade.SpriteList()
        self.mice_list = arcade.SpriteList()

        self.cat_sprite = None

        self.score = 0
        self.time_left = GAME_TIME
        self.game_state = "playing"  # "playing", "won", "lost"
        self.mouse_spawn_timer = 0
        self.spawn_interval = 0.5

        self.holes = [
            (HOLE_SIZE, 100),
            (HOLE_SIZE, 350),
            (HOLE_SIZE, 600),
            (self.width - HOLE_SIZE, 100),
            (self.width - HOLE_SIZE, 350),
            (self.width - HOLE_SIZE, 600),
            (200, self.height - HOLE_SIZE),
            (500, self.height - HOLE_SIZE),
            (800, self.height - HOLE_SIZE),
            (200, HOLE_SIZE),
            (500, HOLE_SIZE),
            (800, HOLE_SIZE),
        ]

        arcade.set_background_color(arcade.color.DARK_BROWN)
        self.background_texture = arcade.load_texture("images/minigame1/floor.png")

        self.set_mouse_visible(False)

    def setup(self):
        self.cat_sprite = arcade.Sprite("images/minigame1/cat.png", scale=0.15)
        self.all_sprites_list.append(self.cat_sprite)

        self.mice_list = arcade.SpriteList()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(self.width // 2, self.height // 2, self.width, self.height))

        self.draw_walls()

        self.all_sprites_list.draw()
        self.mice_list.draw()

        self.draw_ui()

    def draw_walls(self):
        # draw walls
        # wall_thickness = 30
        #
        # arcade.draw_lbwh_rectangle_filled(
        #     wall_thickness // 2, SCREEN_HEIGHT // 2,
        #     wall_thickness, SCREEN_HEIGHT,
        #     arcade.color.DARK_SLATE_GRAY
        # )
        #
        # arcade.draw_lbwh_rectangle_filled(
        #     SCREEN_WIDTH - wall_thickness // 2, SCREEN_HEIGHT // 2,
        #     wall_thickness, SCREEN_HEIGHT,
        #     arcade.color.DARK_SLATE_GRAY
        # )
        #
        # arcade.draw_lbwh_rectangle_filled(
        #     SCREEN_WIDTH // 2, SCREEN_HEIGHT - wall_thickness // 2,
        #     SCREEN_WIDTH, wall_thickness,
        #     arcade.color.DARK_SLATE_GRAY
        # )
        #
        # arcade.draw_lbwh_rectangle_filled(
        #     SCREEN_WIDTH // 2, wall_thickness // 2,
        #     SCREEN_WIDTH, wall_thickness,
        #     arcade.color.DARK_SLATE_GRAY
        # )
        for hole_x, hole_y in self.holes:
            arcade.draw_circle_filled(hole_x, hole_y, HOLE_SIZE // 2, arcade.color.BLACK)
            arcade.draw_circle_outline(hole_x, hole_y, HOLE_SIZE // 2, arcade.color.LIGHT_BROWN, 2)

    def draw_ui(self):
        needed_text = f"ЛОВИ МЫШЕЙ!"
        arcade.draw_text(needed_text, self.width // 2 - 180, self.height - 40,
                         arcade.color.YELLOW, 42, bold=True)

        time_text = f"{int(self.time_left)}s"
        arcade.draw_text(time_text, self.width // 2 - 25, self.height - 100,
                         arcade.color.WHITE, 36, bold=True)

        if self.game_state == "won":
            self.draw_win_screen()
        elif self.game_state == "lost":
            self.draw_lose_screen()

    def draw_win_screen(self):

        self.all_sprites_list.clear()
        self.mice_list.clear()

        arcade.draw_lbwh_rectangle_filled(
            100, 100,
            self.width - 200, self.height - 200,
            (20, 150, 20, 200)
        )

        arcade.draw_text(
            "ПОБЕДА!",
            self.width // 2, self.height // 2 + 100,
            arcade.color.GOLD, 60, bold=True, anchor_x="center"
        )

        stars = STARS.get(min(self.score, 20), 0)
        if self.score >= 30:
            stars = 3
        elif self.score >= 20:
            stars = 2
        elif self.score >= 10:
            stars = 1

        stars_text = "⭐" * stars
        arcade.draw_text(
            stars_text,
            self.width // 2, self.height // 2 + 20,
            arcade.color.GOLD, 50, anchor_x="center"
        )

        stats_text = f"Поймано мышек: {self.score}\n Уровень: {stars}/3 ⭐"
        arcade.draw_text(
            stats_text,
            self.width // 2, self.height // 2 - 60,
            arcade.color.WHITE, 24, anchor_x="center"
        )

        arcade.draw_text(
            "Нажмите R для перезагрузки",
            self.width // 2 - 180, self.height // 2 - 150,
            arcade.color.WHITE, 18, anchor_x="center"
        )

    def draw_lose_screen(self):

        self.all_sprites_list.clear()
        self.mice_list.clear()

        arcade.draw_rect_filled(arcade.rect.LBWH(self.width / 2 - 300, self.height / 2 - 175, 600, 400), (255, 255, 255, 220))

        arcade.draw_text(
            "КОНЕЦ ИГРЫ!",
            self.width // 2, self.height // 2 + 100,
            arcade.color.YELLOW, 60, bold=True, anchor_x="center"
        )

        stats_text = f"Поймано мышек: {self.score}  Нужно было: {MICE_NEEDED_FOR_WIN}"
        arcade.draw_text(
            stats_text,
            self.width // 2, self.height // 2,
            arcade.color.GOLD, 28, anchor_x="center"
        )

        arcade.draw_text(
            "Нажмите R для перезагрузки",
            self.width // 2, self.height // 2 - 120,
            arcade.color.GOLD, 18, anchor_x="center"
        )

        self.complete = True
        arcade.draw_text(
            "Нажмите esc чтобы вернуться на экран выбора",
            self.width / 2, self.height / 2 - 150,
            arcade.color.BLACK, 16, anchor_x="center"
        )

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.game_state != "playing":
            return

        self.time_left -= delta_time

        self.all_sprites_list.update()
        self.mice_list.update()
        self.mice_list.update_animation(delta_time)

        self.mouse_spawn_timer += delta_time
        if self.mouse_spawn_timer >= self.spawn_interval:
            self.spawn_mouse()
            self.mouse_spawn_timer = 0

        if self.time_left <= 0:
            self.time_left = 0
            if self.score >= MICE_NEEDED_FOR_WIN:
                self.game_state = "won"
            else:
                self.game_state = "lost"

    def spawn_mouse(self):
        if self.game_state != "playing":
            return

        start_hole = random.choice(self.holes)

        end_hole = random.choice([h for h in self.holes if h != start_hole])

        start_x = start_hole[0] + random.randint(-10, 10)
        start_y = start_hole[1] + random.randint(-10, 10)

        end_x = end_hole[0] + random.randint(-10, 10)
        end_y = end_hole[1] + random.randint(-10, 10)

        speed = random.randint(300, 600)

        mouse = Mouse(start_x, start_y, end_x, end_y, speed)
        self.mice_list.append(mouse)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.game_state == "playing":
            self.cat_sprite.center_x = x
            self.cat_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state != "playing":
            return

        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        for mouse in self.mice_list:
            distance = ((mouse.center_x - x) ** 2 + (mouse.center_y - y) ** 2) ** 0.5
            if distance < MOUSE_SIZE + 20:  # Зона клика
                mouse.kill()
                self.score += 1
                break

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.reset_game()
        if key == arcade.key.ESCAPE and self.complete:
            ISLANDS_PROGRESS[4] = True
            self.window.go_to_map()


    def reset_game(self):
        self.score = 0
        self.time_left = GAME_TIME
        self.game_state = "playing"
        self.mouse_spawn_timer = 0

        self.mice_list.clear()