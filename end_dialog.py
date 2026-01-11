import arcade
import csv


class EndDialogView(arcade.View):
    def __init__(self):
        super().__init__()
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

        self.is_typing = False
        self.load_dialogue()

    def load_dialogue(self):
        self.dialog = []
        self.dialogue_index = 0
        with open("dialogs/end_dialog.csv", 'r', encoding="utf-8") as file:
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
        if self.dialogue_index < 9:
            arcade.draw_texture_rect(self.background, arcade.rect.LBWH(
            0, 0, self.window.width, self.window.height))
        else:
            arcade.draw_texture_rect(self.background_with_islands, arcade.rect.LBWH(
                0, 0, self.window.width, self.window.height))

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

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_typing:
            self.visible_text = self.full_text
            self.is_typing = False
        else:
            self.dialogue_index += 1

            if self.dialogue_index < len(self.dialog):
                self.start_typing()
            else:
                ...