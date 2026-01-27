import arcade


class FadeView(arcade.View):
    def __init__(self):
        super().__init__()

        self.fade_alpha = 255   # Текущая прозрачность
        self.fade_speed = 250
        self.fade_in = True     # Плавное появление
        self.fade_out = False   # Плавное исчезновение

        self.next_view = None   # Следующее окно
        self.block_click = True     # Блокировка клика при переходе

    def start_fade_in(self):
        """ Начало плавного появления"""
        self.fade_alpha = 255
        self.fade_in = True
        self.fade_out = False
        self.block_click = True

    def start_fade_out(self, next):
        """ Начало плавного исчезновения """
        self.next_view = next
        self.fade_out = True
        self.block_click = True
        self.fade_in = False

    def on_update(self, delta_time):
        # Плавное появление
        if self.fade_in:
            self.fade_alpha -= self.fade_speed * delta_time
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_in = False
                self.block_click = False

        if self.fade_out:
            self.fade_alpha += self.fade_speed * delta_time
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_out = False

                self.window.show_view(self.next_view)
                if hasattr(self.next_view, "bg_music"):
                    self.window.change_music(self.next_view.bg_music)

                self.next_view.start_fade_in()

    def draw_fade(self):
        """ Отрисовка тени """
        if self.window and self.fade_alpha > 0:
            arcade.draw_rect_filled(arcade.rect.XYWH(self.window.width // 2,
                    self.window.height // 2, self.window.width, self.window.height),
                    (0, 0, 0, int(self.fade_alpha)))
