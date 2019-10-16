import classes
import data
from levels import game_base_turn as gbt


def run(gm, screen):
    # Установка игровых параметров
    player = classes.Human(gm, screen, data.PLAYER_NAME)
    enemy = classes.Robot_tactic(gm, screen, data.ROBOT_TACTIC_NAME)
    hbar = data.HIGH_BARS["level_2"]

    gm.set_settings(hbar, player, enemy)
    screen.add_players(gm)
    screen.add_high_bar(hbar)

    # Показ вводного сообщения
    if data.Game_Progress["level_2"]["losses"] == 0:
        screen.display_msg_seq("2_welcomelvl_seq")
        screen.display_msg("2_robotname", data.PLAYER_NAME,
                           data.ROBOT_TACTIC_NAME)

    # Цикл игры уровня
    while gm.game_flag:
        gbt.main(gm)

    # Действия при победе/поражении
    winner = gm.player.__type__
    if winner == "Human":
        screen.display_msg_seq("2_win_seq")
        data.Game_Progress["level_2"]["is_complete"] = True
    else:
        screen.display_msg_seq("2_loose_seq")
        data.Game_Progress["level_2"]["losses"] += 1

    gm.add_dices()
    screen.init_zones()
