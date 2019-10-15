import classes
import data
from levels import game_base_cycle as gbc


def run(gm, screen):
    # Установка игровых параметров
    player = classes.Human(gm, screen, data.PLAYER_NAME)
    enemy = classes.Robot_random(gm, screen, data.ROBOT_RANDOM_NAME)
    hbar = data.HIGH_BARS["level_1"]

    gm.set_settings(hbar, player, enemy)
    screen.add_players(gm)
    screen.add_high_bar(hbar)

    # Показ вводного сообщения
    if data.Game_Progress["level_1"]["losses"] == 0:
        screen.display_msg("1_welcomelvl", data.PLAYER_NAME)
        screen.display_msg_seq("1_welcomelvl_seq")

    # Цикл игры уровня
    gbc.main(gm)

    # Действия при победе/поражении
    winner = gm.player.__type__
    if winner == "Human":
        screen.display_msg("1_win1", data.PLAYER_NAME)
        screen.display_msg("1_win2")
        screen.display_msg("1_win3")
        data.Game_Progress["level_1"]["is_complete"] = True
    else:
        screen.display_msg_seq("1_loose_seq")
        data.Game_Progress["level_1"]["losses"] += 1

    gm.add_dices()
    screen.init_zones()
