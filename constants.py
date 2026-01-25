import arcade


ISLANDS_PROGRESS = {
    1: True,
    2: False,
    3: False,
    4: False,
    5: False
}

EMPTY_TEXTURE = arcade.make_soft_square_texture(size=1, color=arcade.color.WHITE,
                                                outer_alpha=0, center_alpha=0)
ACHIEVEMENTS = [
    {
        "name" : "Забытая попытка",
        "icon" : "images/achievements/unlocked/achievement1_1.png",
        "icon_locked" : "images/achievements/locked/achievement1_1.png"
    },

    {
        "name" : "Первый шаг",
        "icon" : "images/achievements/unlocked/achievement1_2.png",
        "icon_locked" : "images/achievements/locked/achievement1_2.png"
    },

    {
        "name" : "Кости моря",
        "icon" : "images/achievements/unlocked/achievement2_1.png",
        "icon_locked" : "images/achievements/locked/achievement2_1.png"
    },

    {
        "name" : "Нет пути назад",
        "icon" : "images/achievements/unlocked/achievement2_2.png",
        "icon_locked" : "images/achievements/locked/achievement2_2.png"
    },

    {
        "name" : "Заброшенный дом",
        "icon" : "images/achievements/unlocked/achievement3_1.png",
        "icon_locked" : "images/achievements/locked/achievement3_1.png"
    },

    {
        "name" : "Следы на песке",
        "icon" : "images/achievements/unlocked/achievement3_2.png",
        "icon_locked" : "images/achievements/locked/achievement3_2.png"
    },

    {
        "name" : "Скрытое найдено",
        "icon" : "images/achievements/unlocked/achievement4_1.png",
        "icon_locked" : "images/achievements/locked/achievement4_1.png"
    },

    {
        "name" : "Чужие берега",
        "icon" : "images/achievements/unlocked/achievement4_2.png",
        "icon_locked" : "images/achievements/locked/achievement4_2.png"
    },

    {
        "name" : "Экспедиция завершена",
        "icon" : "images/achievements/unlocked/achievement5_1.png",
        "icon_locked" : "images/achievements/locked/achievement5_1.png"
    }
]

players_achievements = {
    "Забытая попытка" : False,
    "Первый шаг" : False,
    "Кости моря" : False,
    "Нет пути назад" : False,
    "Заброшенный дом" : False,
    "Следы на песке" : False,
    "Скрытое найдено" : False,
    "Чужие берега" : False,
    "Экспедиция завершена" : False
}

