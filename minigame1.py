import arcade
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Лови мышей!"

GAME_TIME = 30
MICE_NEEDED_FOR_WIN = 10
STARS = {10: 1, 15: 2, 20: 3}

HOLE_SIZE = 40
MOUSE_SIZE = 30
CAT_SIZE = 60


class Mouse(arcade.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, speed=400):
        super().__init__("images/minigame1/mouse.png", scale=0.1)

        self.center_x = start_x
        self.center_y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.speed = speed  # пиксели в секунду
        self.traveled = 0
        self.total_distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5

    def update(self, delta_time):
        if self.total_distance == 0:
            return

        distance_per_frame = self.speed * delta_time
        self.traveled += distance_per_frame

        progress = min(self.traveled / self.total_distance, 1.0)

        # Интерполируем позицию
        self.center_x = self.start_x + (self.end_x - self.start_x) * progress
        self.center_y = self.start_y + (self.end_y - self.start_y) * progress

        dx = self.end_x - self.start_x
        dy = self.end_y - self.start_y
        angle = math.atan2(dy, dx)
        self.angle = -angle  # отрицательный угол, потому что y-ось перевернута

        if progress >= 1.0:
            self.kill()


class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

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
            (SCREEN_WIDTH - HOLE_SIZE, 100),
            (SCREEN_WIDTH - HOLE_SIZE, 350),
            (SCREEN_WIDTH - HOLE_SIZE, 600),
            (200, SCREEN_HEIGHT - HOLE_SIZE),
            (500, SCREEN_HEIGHT - HOLE_SIZE),
            (800, SCREEN_HEIGHT - HOLE_SIZE),
            (200, HOLE_SIZE),
            (500, HOLE_SIZE),
            (800, HOLE_SIZE),
        ]

        arcade.set_background_color(arcade.color.DARK_BROWN)

        self.set_mouse_visible(False)

    def setup(self):
        self.cat_sprite = arcade.Sprite("images/minigame1/cat.png", scale=0.2)
        self.all_sprites_list.append(self.cat_sprite)

    def on_draw(self):
        self.clear()

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
        time_text = f"Время: {int(self.time_left)}s"
        arcade.draw_text(time_text, 20, SCREEN_HEIGHT - 40,
                         arcade.color.WHITE, 18, bold=True)

        score_text = f"Мышек: {self.score}/{GAME_TIME * 2}"
        arcade.draw_text(score_text, 20, SCREEN_HEIGHT - 80,
                         arcade.color.LIGHT_CYAN, 18, bold=True)

        needed_text = f"Нужно: {MICE_NEEDED_FOR_WIN}"
        arcade.draw_text(needed_text, SCREEN_WIDTH - 220, SCREEN_HEIGHT - 40,
                         arcade.color.YELLOW, 18, bold=True)

        if self.game_state == "won":
            self.draw_win_screen()
        elif self.game_state == "lost":
            self.draw_lose_screen()

    def draw_win_screen(self):
        arcade.draw_lbwh_rectangle_filled(
            100, 100,
            SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200,
            (100, 20, 20, 200)
        )

        arcade.draw_text(
            "ПОБЕДА!",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
            arcade.color.GOLD, 60, bold=True, anchor_x="center"
        )

        stars = STARS.get(min(self.score, 20), 0)
        if self.score >= 20:
            stars = 3
        elif self.score >= 15:
            stars = 2
        elif self.score >= 10:
            stars = 1

        stars_text = "⭐" * stars
        arcade.draw_text(
            stars_text,
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
            arcade.color.GOLD, 50, anchor_x="center"
        )

        stats_text = f"Поймано мышек: {self.score}\n Уровень: {stars}/3 ⭐"
        arcade.draw_text(
            stats_text,
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
            arcade.color.WHITE, 24, anchor_x="center"
        )

        arcade.draw_text(
            "Нажмите R для перезагрузки",
            SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 150,
            arcade.color.WHITE, 18, anchor_x="center"
        )

    def draw_lose_screen(self):
        arcade.draw_lbwh_rectangle_filled(
            150, 150,
            SCREEN_WIDTH - 300, SCREEN_HEIGHT - 300,
            (100, 20, 20, 200)
        )

        arcade.draw_text(
            "КОНЕЦ ИГРЫ!",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
            arcade.color.YELLOW, 60, bold=True, anchor_x="center"
        )

        stats_text = f"Поймано мышек: {self.score}  Нужно было: {MICE_NEEDED_FOR_WIN}"
        arcade.draw_text(
            stats_text,
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            arcade.color.LIGHT_CYAN, 28, anchor_x="center"
        )

        arcade.draw_text(
            "Нажмите R для перезагрузки",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120,
            arcade.color.WHITE, 18, anchor_x="center"
        )

    def on_update(self, delta_time):
        if self.game_state != "playing":
            return

        self.time_left -= delta_time

        self.all_sprites_list.update()
        self.mice_list.update()

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

        hit_list = arcade.check_for_collision_with_list(
            arcade.Sprite("images/minigame1/cat.png"),
            self.mice_list,
            (x, y)
        )

        for mouse in self.mice_list:
            distance = ((mouse.center_x - x) ** 2 + (mouse.center_y - y) ** 2) ** 0.5
            if distance < MOUSE_SIZE + 20:  # Зона клика
                mouse.kill()
                self.score += 1
                break

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.reset_game()

    def reset_game(self):
        self.score = 0
        self.time_left = GAME_TIME
        self.game_state = "playing"
        self.mouse_spawn_timer = 0

        self.mice_list.clear()


def main():
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()