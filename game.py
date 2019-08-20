import graphics

screen = graphics.Screen()
gm = classes.Game(screen)  # game_mode

# Основной цикл игры
while gm.game_flag:
    # Совершение дейстие в ход. Выясняется, нужно ли добавить кости
    action_result = gm.action()
    if action_result in (-2, -1, 2):
        gm.add_dices()
    if action_result < 0 and gm.game_flag is True:
        gm.switch_player()

screen.ending()
del screen
