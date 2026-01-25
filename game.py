import arcade
import csv
from arcade.gui import UIManager, UITextureButton, UIImage
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from fade_class import FadeView
from constants import *

SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Wandering Paws"


class GameWindow(arcade.Window):
    """ Главное окно игры """
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.start_music = arcade.load_sound("sounds/start_window.mp3")
        self.music_player = arcade.play_sound(self.start_music, loop=True)


class StartView(FadeView):
    def __init__(self):
        super().__init__()

        self.background = arcade.load_texture("images/windows/start_window.png")
        self.click_btn_sound = arcade.load_sound("sounds/click_btn.ogg")

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=12)
        self.box_layout = self.box_layout.with_padding(top=460, left=25)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout, anchor_x="center", anchor_y="top")
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        # Кнопки главного экрана (Начать, достижения, выход)
        texture1_normal = arcade.load_texture("images/buttons/start_button/normal.png")
        texture1_hovered = arcade.load_texture("images/buttons/start_button/hovered.png")
        texture1_pressed = arcade.load_texture("images/buttons/start_button/pressed.png")

        texture2_normal = arcade.load_texture("images/buttons/achievements_button/normal.png")
        texture2_hovered = arcade.load_texture("images/buttons/achievements_button/hovered.png")
        texture2_pressed = arcade.load_texture("images/buttons/achievements_button/pressed.png")

        texture3_normal = arcade.load_texture("images/buttons/end_button/normal.png")
        texture3_hovered = arcade.load_texture("images/buttons/end_button/hovered.png")
        texture3_pressed = arcade.load_texture("images/buttons/end_button/pressed.png")

        # Кнопка Начать
        self.btn1 = UITextureButton(texture=texture1_normal,
                               texture_hovered=texture1_hovered,
                               texture_pressed=texture1_pressed,
                               scale=0.5,
                               anchor_x="center")
        self.btn1.on_click = self.start_game
        self.box_layout.add(self.btn1)

        # Кнопка Достижения
        self.btn2 = UITextureButton(texture=texture2_normal,
                               texture_hovered=texture2_hovered,
                               texture_pressed=texture2_pressed,
                               scale=0.5,
                               anchor_x="center")
        self.btn2.on_click = self.achievements_window
        self.box_layout.add(self.btn2)

        # Кнопка Выход
        self.btn3 = UITextureButton(texture=texture3_normal,
                               texture_hovered=texture3_hovered,
                               texture_pressed=texture3_pressed,
                               scale=0.5,
                               anchor_x="center")
        self.btn3.on_click = self.exit_game
        self.box_layout.add(self.btn3)

    def start_game(self, event):
        arcade.play_sound(self.click_btn_sound)
        self.start_fade_out(IntroDialogView())
        self.manager.disable()

    def achievements_window(self, event):
        arcade.play_sound(self.click_btn_sound)
        self.start_fade_out(AchievementsView())
        self.manager.disable()

    def exit_game(self, event):
        arcade.play_sound(self.click_btn_sound)
        arcade.exit()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.LBWH(
            0, 0, self.width, self.height))
        self.manager.draw()
        self.draw_fade()


class IntroDialogView(FadeView):
    def __init__(self):
        super().__init__()
        arcade.stop_sound(self.window.music_player)
        arcade.play_sound(arcade.load_sound("sounds/dialogue.mp3"), loop=True)
        self.background = arcade.load_texture("images/windows/dialogs_background.jpg")
        self.background_with_islands = arcade.load_texture("images/windows/dialogs_background_with_islands.jpg")

        self.cat = arcade.Sprite()
        self.cat.scale = 0.8
        self.cat_talk = arcade.load_texture("images/dialogue_sprites/cat_talk.png")
        self.cat.position = (290, 370)
        self.cat_not_talk = arcade.load_texture("images/dialogue_sprites/cat_not_talk.png")

        self.dialogue_box = arcade.Sprite("images/dialogue_sprites/dialogue_box.png", 1.245)
        self.dialogue_box.bottom = 23
        self.dialogue_box.left = 10

        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.cat)
        self.all_sprites.append(self.dialogue_box)

        self.islands_alpha = 0
        self.islands_fade_speed = 10
        self.show_islands = False

        self.is_typing = False
        self.load_dialogue()

        if self.dialogue_index <= 6:
            self.show_islands = True

    def load_dialogue(self):
        self.dialog = []
        self.dialogue_index = 0
        with open("dialogs/start_dialog.csv", 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                self.dialog.append({
                    "speaker": row["speaker"],
                    "text": row["text"]})
        self.start_typing()

    def start_typing(self):
        # Старт эффекта печати текста
        self.visible_text = ''
        self.text_index = 0
        self.text_timer = 0
        self.text_speed = 0.03
        self.is_typing = True
        current = self.dialog[self.dialogue_index]
        self.full_text = current["text"]

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.show_islands and self.islands_alpha < 255:
            # Плавное появление островов
            self.islands_alpha += self.islands_fade_speed * delta_time
            self.islands_alpha = min(self.islands_alpha, 255)
        if self.is_typing:
            self.text_timer += delta_time
            if self.text_timer >= self.text_speed:
                self.text_timer = 0

                if self.text_index < len(self.full_text):
                    self.visible_text += self.full_text[self.text_index]
                    self.text_index += 1
                else:
                    self.is_typing = False

    def on_draw(self):
        self.clear()
        if self.dialogue_index >= len(self.dialog):
            return

        arcade.draw_texture_rect(self.background, arcade.rect.LBWH(
            0, 0, self.window.width, self.window.height))

        if self.show_islands:
            arcade.draw_texture_rect(self.background_with_islands, arcade.rect.LBWH(
                0, 0, self.window.width, self.window.height), alpha=self.islands_alpha)

        # Диалог
        current = self.dialog[self.dialogue_index]
        speaker = current["speaker"]
        if speaker == "Кот":
            self.cat.texture = self.cat_not_talk
        elif speaker == "Напарник":
            self.cat.texture = self.cat_talk

        self.all_sprites.draw()
        arcade.draw_text(speaker, 85, 260, arcade.color.WHITE, 30)
        arcade.draw_text(self.visible_text, 100, 130, arcade.color.WHITE, 26, width=1400, multiline=True)

        self.draw_fade()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_typing:
            self.visible_text = self.full_text
            self.is_typing = False
        else:
            self.dialogue_index += 1

            if self.dialogue_index < len(self.dialog):
                self.start_typing()
            else:
                self.start_fade_out(IslandsMapView())


class AchievementsView(FadeView):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("images/windows/achievements_window.jpg")
        self.click_btn_sound = arcade.load_sound("sounds/click_btn.ogg")

        self.manager = UIManager()
        self.manager.enable()

        self.row1_layout = UIBoxLayout(vertical=False, space_between=20)
        self.row2_layout = UIBoxLayout(vertical=False, space_between=20)

        self.vertical_box = UIBoxLayout(vertical=True, space_between=20)
        self.vertical_box.add(self.row1_layout)
        self.vertical_box.add(self.row2_layout)
        self.vertical_box = self.vertical_box.with_padding(top=100)

        self.anchor_layout = UIAnchorLayout()
        self.anchor_layout.add(self.vertical_box)

        self.manager.add(self.anchor_layout)
        self.load_achievements()
        self.setup_widgets()

    def load_achievements(self):
        self.images = []
        for achievement in ACHIEVEMENTS:
            ach = achievement["name"]
            if players_achievements.get(ach, False):
                texture = arcade.load_texture(achievement["icon"])
                image = UIImage(texture=texture, width=230, height=230)
            else:
                texture = arcade.load_texture(achievement["icon_locked"])
                image = UIImage(texture=texture, width=230, height=230, alpha=200)

            self.images.append(image)

        for i in range(0, 5):
            self.row1_layout.add(self.images[i])

        for i in range(5, 9):
            self.row2_layout.add(self.images[i])

    def setup_widgets(self):
        # Кнопка Назад
        texture1_normal = arcade.load_texture("images/buttons/back_button/normal.png").flip_horizontally()
        texture1_hovered = arcade.load_texture("images/buttons/back_button/hovered.PNG").flip_horizontally()
        texture1_pressed = arcade.load_texture("images/buttons/back_button/pressed.PNG").flip_horizontally()

        self.back_btn = UITextureButton(texture=texture1_normal,
                                        texture_hovered=texture1_hovered,
                                        texture_pressed=texture1_pressed,
                                        scale=0.15,
                                        anchor_x="center",
                                        x=20, y=725)

        self.back_btn.on_click = self.back_to_main
        self.manager.add(self.back_btn)

    def back_to_main(self, event):
        arcade.play_sound(self.click_btn_sound)
        self.start_fade_out(StartView())
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.LBWH(
            0, 0, self.window.width, self.window.height))
        self.manager.draw()
        self.draw_fade()


class IslandsMapView(FadeView):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("images/windows/main_islands_window.png")
        self.click_btn_sound = arcade.load_sound("sounds/click_btn.ogg")

        self.manager = UIManager()
        self.manager.enable()
        self.setup_widgets()

        first = IslandZone(178, 85, 378, 236, 1)
        second = IslandZone(555, 344, 402, 180, 2)
        third = IslandZone(992, 58, 503, 364, 3)
        fourth = IslandZone(987, 457, 451, 330, 4)
        fifth = IslandZone(503, 616, 425, 235, 5)

        self.island_zones = [first, second, third, fourth, fifth]

        self.timer = 2
        self.text1 = ""
        self.text2 = ""

    def setup_widgets(self):
        texture1_normal = arcade.load_texture("images/buttons/home_button/normal.png")
        texture1_hovered = arcade.load_texture("images/buttons/home_button/hovered.PNG")
        texture1_pressed = arcade.load_texture("images/buttons/home_button/pressed.PNG")

        self.home_btn = UITextureButton(texture=texture1_normal,
                                        texture_hovered=texture1_hovered,
                                        texture_pressed=texture1_pressed,
                                        scale=0.15,
                                        anchor_x="center",
                                        x=0, y=735)

        self.home_btn.on_click = self.back_to_main
        self.manager.add(self.home_btn)

    def back_to_main(self, event):
        arcade.play_sound(self.click_btn_sound)
        self.start_fade_out(StartView())
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.LBWH(
            0, 0, self.window.width, self.window.height))
        self.manager.draw()

        if self.timer > 0:
            arcade.draw_text(self.text1, self.window.width / 2, 70, arcade.color.RED, 30, anchor_x="center",
                             anchor_y="center")
            arcade.draw_text(self.text2, self.window.width / 2, 40, arcade.color.RED, 20, anchor_x="center",
                             anchor_y="center")

        self.draw_fade()

    def on_mouse_press(self, x, y, button, modifiers):
        for island in self.island_zones:
            if island.contains(x, y):
                self.island_click(island)
                return

    def island_click(self, island):
        arcade.play_sound(self.click_btn_sound)

        if ISLANDS_PROGRESS.get(island.island_id, False):
            self.open_island(island.island_id)
            self.manager.disable()
        else:
            self.text1 = (f"Остров {island.island_id} пока не доступен")
            self.text2 = ("Пройдите предыдущий остров для открытия")
            self.timer = 2

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.timer > 0:
            self.timer -= delta_time

    def open_island(self, island_id):
        if island_id == 1:
            self.start_fade_out(FirstIslandView())
        elif island_id == 2:
            self.start_fade_out(SecondIslandView())
        elif island_id == 3:
            self.start_fade_out(ThirdIslandView())
        elif island_id == 4:
            self.start_fade_out(FourthIslandView())
        elif island_id == 5:
            self.start_fade_out(FifthIslandView())


class IslandZone:
    def __init__(self, x, y, width, height, island_id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.island_id = island_id

    def contains(self, mouse_x, mouse_y):
        return (
            self.x <= mouse_x <= self.x + self.width and
            self.y <= mouse_y <= self.y + self.height
        )


class FirstIslandView(FadeView):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.RED)

    def on_draw(self):
        self.clear()
        self.draw_fade()


class SecondIslandView(FadeView):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ORANGE)


class ThirdIslandView(FadeView):
    def __init__(self):
        super().__init__()
        ...


class FourthIslandView(FadeView):
    def __init__(self):
        super().__init__()
        ...


class FifthIslandView(FadeView):
    def __init__(self):
        super().__init__()
        ...


def setup_game(width=1920, height=1080, title="Wandering Paws"):
    window = GameWindow(width, height, title)
    window.show_view(StartView())
    return window


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
