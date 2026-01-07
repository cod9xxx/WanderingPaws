import arcade
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Wandering Paws"


class StartWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = arcade.load_texture("images/windows/start_window.png")

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.box_layout = self.box_layout.with_padding(top=450, left=25)

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

        btn1 = UITextureButton(texture=texture1_normal,
                               texture_hovered=texture1_hovered,
                               texture_pressed=texture1_pressed,
                               scale=0.5,
                               anchor_x="center")
        btn1.on_click = ...
        self.box_layout.add(btn1)

        btn2 = UITextureButton(texture=texture2_normal,
                               texture_hovered=texture2_hovered,
                               texture_pressed=texture2_pressed,
                               scale=0.5,
                               anchor_x="center")
        btn2.on_click = ...
        self.box_layout.add(btn2)

        btn3 = UITextureButton(texture=texture3_normal,
                               texture_hovered=texture3_hovered,
                               texture_pressed=texture3_pressed,
                               scale=0.5,
                               anchor_x="center")
        btn3.on_click = self.exit_game
        self.box_layout.add(btn3)

    def exit_game(self, event):
        arcade.exit()

    def setup(self):
        ...

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.LBWH(
            0, 0, self.width, self.height))
        self.manager.draw()


def setup_game(width=1920, height=1080, title="Wandering Paws"):
    game = StartWindow(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()