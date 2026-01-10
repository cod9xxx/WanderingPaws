import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Котик"

ANIMATION_SPEED = 0.15


class Cat(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.load_texture("images/cat_animation/forward1.png")
        self.scale = 0.15
        self.center_x = x
        self.center_y = y

        self.speed = 230
        self.change_x = 0
        self.change_y = 0

        self.current_texture = 0
        self.animation_timer = 0
        self.direction = "down"

        # Анимации
        self.textures_forward = [
            arcade.load_texture("images/cat_animation/forward1.png"),
            arcade.load_texture("images/cat_animation/forward2.png"),
            arcade.load_texture("images/cat_animation/forward1.png"),
            arcade.load_texture("images/cat_animation/forward2.png").flip_horizontally()
        ]

        self.textures_backward = [
            arcade.load_texture("images/cat_animation/back1.png"),
            arcade.load_texture("images/cat_animation/back2.png"),
            arcade.load_texture("images/cat_animation/back1.png"),
            arcade.load_texture("images/cat_animation/back2.png").flip_horizontally()
        ]

        self.textures_right = [
            arcade.load_texture("images/cat_animation/right1.png"),
            arcade.load_texture("images/cat_animation/right2.png"),
            arcade.load_texture("images/cat_animation/right1.png"),
            arcade.load_texture("images/cat_animation/right3.png")
        ]

        self.textures_left = [
            arcade.load_texture("images/cat_animation/right1.png").flip_horizontally(),
            arcade.load_texture("images/cat_animation/right2.png").flip_horizontally(),
            arcade.load_texture("images/cat_animation/right1.png").flip_horizontally(),
            arcade.load_texture("images/cat_animation/right3.png").flip_horizontally()
        ]

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        if self.change_x == 0 and self.change_y == 0:
            self.current_texture = 0
            return

        self.animation_timer += delta_time
        if self.animation_timer < ANIMATION_SPEED:
            return

        self.animation_timer = 0
        self.current_texture = (self.current_texture + 1) % 4

        if self.direction == "down":
            self.texture = self.textures_forward[self.current_texture]
        elif self.direction == "up":
            self.texture = self.textures_backward[self.current_texture]
        elif self.direction == "right":
            self.texture = self.textures_right[self.current_texture]
        elif self.direction == "left":
            self.texture = self.textures_left[self.current_texture]


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BEIGE)

    def setup(self):
        self.cat_list = arcade.SpriteList()
        self.cat = Cat(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.cat_list.append(self.cat)

    def on_draw(self):
        self.clear()
        self.cat_list.draw()

    def on_update(self, delta_time):
        self.cat_list.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.cat.change_y = self.cat.speed
            self.cat.direction = "up"
        elif key == arcade.key.S:
            self.cat.change_y = -self.cat.speed
            self.cat.direction = "down"
        elif key == arcade.key.D:
            self.cat.change_x = self.cat.speed
            self.cat.direction = "right"
        elif key == arcade.key.A:
            self.cat.change_x = -self.cat.speed
            self.cat.direction = "left"

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.cat.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.cat.change_x = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()