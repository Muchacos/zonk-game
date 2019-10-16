import time

import classes
import data
import tools as tls
from levels import game_base_turn as gbt


def run(gm, screen):
    # Установка игровых параметров
    player = classes.Human(gm, screen, data.PLAYER_NAME)
    enemy = classes.Robot_random(gm, screen, data.ROBOT_CALCULATOR_NAME)
    hbar = data.HIGH_BARS["level_3"]

    gm.set_settings(hbar, player, enemy)
    screen.add_players(gm)
    screen.add_high_bar(hbar)

    # Показ вводного сообщения
    if data.Game_Progress["level_3"]["losses"] == 0:
        screen.display_msg_seq("3_welcomelvl_seq")

    # Цикл игры уровня
    while gm.player.__type__ == "Robot" or gm.player.score_total < hbar - 500:
        gbt.main(gm, new_dfh=new_dfh, new_dfr=new_dfr)

    special_dices = [
        [2, 2, 2, 3, 4, 6],
        [1, 6, 2],
        [5, 4],
        [3]
    ]
    i = 0

    while (gm.player.__type__ == "Human" or
           gm.second_player.score_total < hbar - 300):
        if i == 3:
            special_dices[i] = tls.cheat_bad_dices(1)
        gbt.main(gm, new_dfh=special_dices[i].copy())

        if gm.player.__type__ == "Human" and gm.player.score_turn != 0:
            i += 1
        else:
            i = 0

    robot_last_dices = tls.cheat_bad_dices(6)
    robot_good_dices = [1, 1, 1, 1, 1, 1]
    screen.anim_diceroll(6)
    screen.display_dices(robot_last_dices)
    time.sleep(2)
    screen.display_msg("empty", wait=False)
    time.sleep(2)
    screen.display_dices(robot_good_dices)
    time.sleep(2)
    screen.effect_hldices(robot_good_dices)
    gm.player.add_scorepick(4000)
    time.sleep(0.7)
    screen.effect_hldices(robot_good_dices, cp_id=6)
    gm.player.add_scoreturn()
    time.sleep(0.7)
    gm.player.add_scoretotal()
    time.sleep(2.5)
    data.Game_Progress["level_3"]["is_complete"] = True
    screen.init_zones()


def new_dfh(gm):
    while True:
        dices = gbt.dices_for_human(gm)
        possible_score = tls.dices_score(dices)
        human_scr = gm.player.score_total + gm.player.score_turn
        if possible_score + human_scr <= gm.high_bar - 400:
            break
    return dices


def new_dfr(gm):
    while True:
        dices = gbt.dices_for_robot(gm)
        possible_score = tls.dices_score(dices)
        robot_scr = gm.player.score_total + gm.player.score_turn
        if possible_score + robot_scr <= gm.high_bar - 250:
            break
    return dices
