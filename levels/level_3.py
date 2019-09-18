import random

import classes
import data
import tools


def run(gm, screen):
    player = classes.Human(gm, screen, data.PLAYER_NAME)
    enemy = classes.AI_easy(gm, screen, data.ROBOT_CALCULATOR_NAME)
    hbar = 4000

    gm.set_settings(hbar, player, enemy)
    screen.add_players(gm)
    screen.add_high_bar(hbar)

    if data.Level_Progress[3][1] == 0:
        screen.display_msg("3_welcomelvl1")
        screen.display_msg("3_welcomelvl1.1")
        screen.display_msg("3_welcomelvl1.2")
        screen.display_msg("3_welcomelvl1.3")
        screen.display_msg("3_welcomelvl1.4", data.ROBOT_CALCULATOR_NAME)
    elif data.Level_Progress[3][1] == 1:
        screen.display_msg("3_welcomelvl2")
        screen.display_msg("3_welcomelvl2.1", speedup=0.75)
    elif data.Level_Progress[3][1] == 2:
        screen.display_msg("3_welcomelvl3")
        screen.display_msg("3_welcomelvl3.1")
    elif data.Level_Progress[3][1] == 3:
        screen.display_msg("3_welcomelvl4")
    else:
        screen.display_msg("3_welcomelvl5")
        screen.display_msg("3_welcomelvl5.1")

    if data.Level_Progress[3][1] < 4:
        while gm.game_flag:
            if gm.player.__type__ == "Robot":
                any_combos = roll_dices_for_robot(gm)
            else:
                any_combos = gm.roll_dices()

            if any_combos is False:
                gm.switch_player()
                gm.add_dices()
                continue

            while True:
                pick_score = gm.get_pick()
                if pick_score == 0:
                    continue

                action_choice = gm.get_action_choice()
                if action_choice != data.KEYCODES["TURN_CANCEL"]:
                    gm.add_scores(pick_score, action_choice)
                    gm.check_win()
                    break

            if action_choice == data.KEYCODES["TURN_END"] and gm.game_flag:
                gm.add_dices()
                gm.switch_player()

            elif (action_choice == data.KEYCODES["TURN_CONTINUE"] and
                  len(gm.dices) == 0 and gm.game_flag):
                gm.add_dices()

        if gm.player.__type__ == "Human":
            screen.display_msg("3_win1", dealy=1.5, speedup=1.5)
            screen.display_msg("3_win2", dealy=1.5, speedup=1.5)
            screen.display_msg("3_win3", dealy=1.5, speedup=1.5)
            screen.display_msg("3_win4", dealy=1.5, speedup=1.5)
            screen.display_msg("3_win5", dealy=1.5, speedup=1.5)
            screen.display_msg("3_win6", delay=2)
            screen.display_msg("3_win7")
            screen.display_msg("3_win8")
            screen.display_msg("3_win9")
            data.Level_Progress[3][0] = True
            data.Level_Progress[3][2] += 1
        elif data.Level_Progress[3][1] == 0:
            screen.display_msg("3_loosefirst1")
            screen.display_msg("3_loosefirst2")
            screen.display_msg("3_loosefirst3")
            data.Level_Progress[2][0] = False
        else:
            screen.display_msg("3_loosenotfirst", "Вы вновь проиграли")
            data.Level_Progress[2][0] = False

    else:
        screen.display_msg("", delay=4)
        screen.display_msg("3_final1", delay=1.5)
        screen.display_msg("3_final2", delay=1, speedup=1.5)
        screen.display_msg("$_loading1", delay=0.5)
        screen.display_msg("$_loading2", delay=0.5)
        screen.display_msg("$_loading3", delay=0.5)
        screen.display_msg("$_loading4", delay=0.5)
        screen.display_msg("debug", "ERR: RUN OUT OF MEMORY",
                           delay=1.5, speedup=100)
        screen.display_msg("3_final3", delay=1)
        screen.display_msg("3_final4", delay=1)
        screen.display_msg("3_final5")
        screen.display_msg("3_final6", delay=3)
        screen.display_msg("3_final7")
        screen.display_msg("3_final8")
        data.Level_Progress[3][0] = True

    data.Level_Progress[3][1] += 1

    gm.add_dices()
    screen.init_zones()


def roll_dices_for_robot(gm):
    screen = gm.screen

    screen.anim_diceroll(len(gm.dices))
    if tools.chance(36):
        gm.dices = tools.cheat_good_dices(len(gm.dices))
    else:
        for i in range(len(gm.dices)):
            gm.dices[i] = random.randint(1, 6)

    gm.temp_dices = gm.dices[:]

    screen.display_dices(gm.dices)
    if tools.check_combos_any(gm.dices) is False:
        screen.display_msg("07_nocombos")
        gm.player.clear_scoreturn()

    return tools.check_combos_any(gm.dices)
