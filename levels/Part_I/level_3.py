import time

import classes
import data
import tools as tls
from levels import game_base_turn as gbt


def run(gm, screen):
    # Установка игровых параметров
    player = classes.Human(gm, screen, data.PLAYER_NAME)
    robname = data.ROBOT_CALCULATOR_NAME
    enemy = classes.Robot_random(gm, screen, robname)
    hbar = data.HIGH_BARS["level_3"]

    gm.set_settings(hbar, player, enemy)
    screen.add_players(gm)
    screen.add_high_bar(hbar)

    # Показ вводного сообщения
    screen.display_msg_seq("3_welcomelvl_seq")

    # Цикл игры, идущий до тех пор, пока игрок не наберет hbar - 500 очков
    while gm.player.type == "Robot" or gm.player.score_total < hbar - 500:
        gbt.main(gm, new_dfh=new_dfh, new_dfr=new_dfr)

    # Кости, которые будут далее выпадать игроку
    special_dices = [
        [2, 2, 2, 3, 4, 6],
        [1, 6, 2],
        [5, 4],
        [3]
    ]
    i = 0

    # Цикл, идущий до тех пор, пока игрок не закончит ход, взяв особые кости
    while (gm.player.type == "Human" or
           gm.second_player.score_total < hbar - 300):
        if i == 3:
            special_dices[i] = tls.cheat_bad_dices(1)
        gbt.main(gm, new_dfh=special_dices[i].copy())

        if gm.player.type == "Human" and gm.player.score_turn != 0:
            i += 1
        else:
            i = 0

    # Финальный бросок костей робота
    robot_last_dices = tls.cheat_bad_dices(6)
    robot_good_dices = [1, 1, 1, 1, 1, 1]
    screen.anim_diceroll(6)
    screen.display_dices(robot_last_dices)
    time.sleep(4)
    screen.display_dices(robot_good_dices)
    screen.display_msg("empty", wait=False)
    time.sleep(1.5)
    screen.effect_hldices(robot_good_dices)
    gm.player.add_scorepick(4000)
    screen.display_msg("a_robturnF", delay=-1.2)
    screen.effect_hldices(robot_good_dices, cp_id=6)
    gm.player.add_scoreturn()
    screen.display_msg("a_scrpick", robname, 4000, delay=-1.2)
    gm.player.add_scoretotal()
    screen.display_msg("a_scrtotl", robname, gm.player.score_total, delay=-1.2)
    screen.display_msg("3_robwin", robname)
    screen.display_msg("empty", wait=False)
    time.sleep(2.5)
    data.Game_Progress["level_3"]["is_complete"] = True
    screen.clear_zone(screen.ZONE_SCORE)


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
