import arcade

class StartWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height)
        self.background = arcade.load_texture("images/windows/start_window.PNG")

    def on_draw(self):
        ...