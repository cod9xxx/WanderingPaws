import arcade
import csv
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Wandering Paws"


class GameWindow(arcade.Window):
    """ Главное окно игры """
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

    def setup(self):
        ...


class StartView(arcade.View):
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
        self.window.show_view(IntroDialogView())

    def achievements_window(self, event):
        arcade.play_sound(self.click_btn_sound)

    def exit_game(self, event):
        arcade.play_sound(self.click_btn_sound)
        arcade.exit()

    def setup(self):
        ...

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.LBWH(
            0, 0, self.width, self.height))
        self.manager.draw()


class IntroDialogView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("images/windows/dialogs_background.jpg")

        self.cat_talk = arcade.Sprite("images/dialogue_sprites/cat_talk.png", 0.8)
        self.cat_talk.position = (290, 370)
        self.cat_not_talk = arcade.Sprite("images/dialogue_sprites/cat_not_talk.png", 0.7)
        self.dialogue_box = arcade.Sprite("images/dialogue_sprites/dialogue_box.png", 1.245)
        self.dialogue_box.bottom = 23
        self.dialogue_box.left = 10

        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.cat_talk)
        # self.all_sprites.append(self.cat_not_talk)
        self.all_sprites.append(self.dialogue_box)
        self.load_dialogue()

    def load_dialogue(self):
        self.dialog = []
        self.dialogue_index = 0
        with open("dialogs/start_dialog.csv", 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                self.dialog.append({
                    "speaker": row["speaker"],
                    "text": row["text"]})

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.LBWH(
            0, 0, self.window.width, self.window.height))
        self.all_sprites.draw()

        # Диалог
        dialog = self.dialog
        current = dialog[self.dialogue_index]
        speaker = current["speaker"]
        text = current["text"]

        arcade.draw_text(text, 120, 90, arcade.color.WHITE, 26)
        arcade.draw_text(speaker, 80, 260, arcade.color.WHITE, 30)

    def on_mouse_press(self, x, y, button, modifiers):
        self.dialogue_index += 1



class IslandsMapView(arcade.View):
    def __init__(self):
        super().__init__()


def setup_game(width=1920, height=1080, title="Wandering Paws"):
    window = GameWindow(width, height, title)
    window.show_view(StartView())
    return window


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()



