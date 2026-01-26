import arcade
import time

from fade_class import FadeView

from constants import *

SCREEN_TITLE = "Поиск предметов"

class HiddenObjectGame(FadeView):
    def __init__(self):
        super().__init__()

        self.cur_game = None
        self.background = None
        self.items_to_find = arcade.SpriteList()
        self.found_items_count = 0

        # game items
        self.target_names = ["Компас", "Лупа", "Лампа", "Подзорная труба", "Сумка"]
        self.found_status = [False] * 5

        self.start_time = time.time()
        self.game_over = False
        self.final_time = 0

    def add_item(self, x, y, width, height):
        item = arcade.SpriteSolidColor(width, height, arcade.color.BLACK)
        item.center_x = x
        item.center_y = y
        item.item_index = len(self.items_to_find)
        self.items_to_find.append(item)


    def setup(self):
        self.background = arcade.load_texture("images/find_minigame/boat.jpg")

        # adding invisible sprites at objects coordinates
        self.add_item(912, 575, 100, 100)
        self.add_item(825, 510, 210, 30)
        self.add_item(1050, 610, 100, 190)
        self.add_item(480, 520, 350, 50)
        self.add_item(1150, 175, 325, 175)

    def on_draw(self):
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(1536 / 2, 960 / 2, 1536, 960))

        arcade.draw_rect_filled(arcade.rect.XYWH(1536 / 2, 40, 1536, 80), arcade.color.ALMOND)

        for i, name in enumerate(self.target_names):
            color = arcade.color.GRAY if self.found_status[i] else arcade.color.BLACK
            text = f"~~{name}~~" if self.found_status[i] else name
            arcade.draw_text(text, 20 + (i * 300), 30, color, 14)

        elapsed = int(time.time() - self.start_time) if not self.game_over else int(self.final_time)
        arcade.draw_text(f"Время: {elapsed} сек.", 1536 - 150, 960 - 30, arcade.color.WHITE, 16)

        if self.game_over:
            self.draw_victory_screen()

    def draw_victory_screen(self):
        arcade.draw_rect_filled(arcade.rect.LBWH(1536 / 2 - 300, 960 / 2 - 175, 600, 400), (255, 255, 255, 220))
        arcade.draw_text("ПОБЕДА!", 1536 / 2, 960 / 2 + 40, arcade.color.BLACK, 24, anchor_x="center")

        stars = 1
        if self.final_time <= 30:
            stars = 3
        elif self.final_time <= 60:
            stars = 2

        arcade.draw_text(f"Звезды: {'★' * stars}", 1536 / 2, 960 / 2 - 20, arcade.color.GOLD, 20,
                         anchor_x="center")

        arcade.draw_text(f"Нажмите esc чтобы вернуться на экран выбора", 1536 / 2, 960 / 2 - 60, arcade.color.BLACK, 16,
                         anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over:
            return

        hit_list = arcade.get_sprites_at_point((x, y), self.items_to_find)

        if len(hit_list) > 0:
            for item in hit_list:
                idx = item.item_index
                if not self.found_status[idx]:
                    self.found_status[idx] = True
                    self.found_items_count += 1
                    item.remove_from_sprite_lists()

            if self.found_items_count == 5:
                self.game_over = True
                self.final_time = time.time() - self.start_time
    
    def on_key_press(self, button, modifiers):
        if button == arcade.key.ESCAPE:
            ISLANDS_PROGRESS[2] = True
            from game import IslandsMapView
            self.cur_game = IslandsMapView()
            self.cur_game.bg_music = 'sounds/dialogue.mp3'
            self.start_fade_out(self.cur_game)