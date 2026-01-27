import arcade
import random
import time
import math

from fade_class import FadeView

from constants import *

SCREEN_TITLE = "Прямоугольный пазл 6x4"

ROW_COUNT = 4
COL_COUNT = 6

IMAGE_PATH = "images/puzzle/puzzle_image.jpg"


class JigsawPiece(arcade.Sprite):
    def __init__(self, texture, correct_x, correct_y):
        super().__init__(texture)
        self.correct_x = correct_x
        self.correct_y = correct_y
        self.is_snapped = False


class Puzzle(FadeView):
    def __init__(self):
        super().__init__()

        self.cur_game = None
        self.piece_list = None
        self.background_list = None
        self.held_piece = None

        self.start_time = 0
        self.total_time = 0
        self.game_over = False
        self.stars = 0

        self.drag_offset_x = 0
        self.drag_offset_y = 0


    def setup(self):
        self.piece_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.game_over = False
        self.start_time = time.time()
        self.total_time = 0

        main_texture = arcade.load_texture(IMAGE_PATH)

        # texture scaling
        scale = min(self.width * 0.8 / main_texture.width, self.height * 0.8 / main_texture.height)

        piece_w = main_texture.width / COL_COUNT
        piece_h = main_texture.height / ROW_COUNT

        board_width = main_texture.width * scale
        board_height = main_texture.height * scale
        start_x = (self.width - board_width) / 2
        start_y = (self.height - board_height) / 2

        bg_sprite = arcade.Sprite(main_texture, scale)
        bg_sprite.center_x = self.width / 2
        bg_sprite.center_y = self.height / 2
        bg_sprite.alpha = 80
        self.background_list.append(bg_sprite)

        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                sub_texture = arcade.Texture(
                    name=f"p_{row}_{col}",
                    image=main_texture.image.crop((
                        col * piece_w,
                        (ROW_COUNT - 1 - row) * piece_h,
                        (col + 1) * piece_w,
                        (ROW_COUNT - row) * piece_h
                    ))
                )

                correct_x = start_x + (col + 0.5) * piece_w * scale
                correct_y = start_y + (row + 0.5) * piece_h * scale

                piece = JigsawPiece(sub_texture, correct_x, correct_y)
                piece.scale = scale

                piece.center_x = random.randint(50, int(self.width) - 50)
                piece.center_y = random.randint(50, int(self.height) - 50)

                self.piece_list.append(piece)

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.piece_list.draw()

        if not self.game_over:
            mins, secs = divmod(int(self.total_time), 60)
            arcade.draw_text(f"Время: {mins:02d}:{secs:02d}", 20, self.height - 40, arcade.color.WHITE, 18)
        else:
            arcade.draw_rect_filled(arcade.rect.LBWH(self.width / 2 - 300, self.height / 2 - 175, 600, 400), (255, 255, 255, 220))
            arcade.draw_text("ГОТОВО!", self.width / 2, self.height / 2 + 60, arcade.color.BLACK, 30,
                             anchor_x="center")

            stars_str = "★ " * self.stars + "☆ " * (3 - self.stars)
            arcade.draw_text(stars_str, self.width / 2, self.height / 2, arcade.color.GOLD, 40, anchor_x="center")
            arcade.draw_text("Нажми R для новой игры", self.width / 2, self.height / 2 - 70, arcade.color.GOLD, 20,
                             anchor_x="center")

            arcade.draw_text("Нажмите esc чтобы вернуться на экран выбора", self.width / 2, self.height / 2 - 100, arcade.color.BLACK, 16,
                             anchor_x="center")

            self.draw_fade()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if not self.game_over:
            self.total_time = time.time() - self.start_time
            if all(p.is_snapped for p in self.piece_list):
                self.game_over = True
                self.calculate_stars()

    def calculate_stars(self):
        if self.total_time <= 180:
            self.stars = 3
        elif self.total_time <= 300:
            self.stars = 2
        else:
            self.stars = 1

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over: return
        pieces = arcade.get_sprites_at_point((x, y), self.piece_list)
        if pieces:
            piece = pieces[-1]
            if not piece.is_snapped:
                self.held_piece = piece
                self.piece_list.remove(piece)
                self.piece_list.append(piece)
                self.drag_offset_x = piece.center_x - x
                self.drag_offset_y = piece.center_y - y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.held_piece:
            self.held_piece.center_x = x + self.drag_offset_x
            self.held_piece.center_y = y + self.drag_offset_y

    def on_mouse_release(self, x, y, button, modifiers):
        if self.held_piece:
            dist = math.hypot(self.held_piece.center_x - self.held_piece.correct_x,
                              self.held_piece.center_y - self.held_piece.correct_y)
            if dist < 40:
                self.held_piece.center_x = self.held_piece.correct_x
                self.held_piece.center_y = self.held_piece.correct_y
                self.held_piece.is_snapped = True
            self.held_piece = None

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.R:
            self.setup()
        if symbol == arcade.key.ESCAPE:
            if self.game_over:
                ISLANDS_PROGRESS[3] = True
            if self.window.music_player:
                arcade.stop_sound(self.window.music_player)
                self.window.music_player = None

            from game import IslandsMapView
            next_view = IslandsMapView()
            next_view.bg_music = 'sounds/dialogue.mp3'

            self.fade_alpha = 0
            self.fade_out = True
            self.fade_in = False
            self.next_view = next_view
