import classes
import data


def run(gm, screen):
    player = classes.Human(gm, screen, data.PLAYER_NAME)
    enemy = classes.Robot_tactic(gm, screen, data.ROBOT_TACTIC_NAME)
    hbar = 3000

    gm.set_settings(hbar, player, enemy)
    screen.add_players(gm)
    screen.add_high_bar(hbar)

    if data.Level_Progress[2][1] == 0:
        screen.display_msg("2_welcomelvl1")
        screen.display_msg("2_lvlinfo1", data.ROBOT_TACTIC_NAME)
        screen.display_msg("2_lvlinfo2")
        screen.display_msg("2_lvlinfo3", hbar)
    elif data.Level_Progress[3][1] == 0:
        screen.display_msg("2_welcomelvl2")
        screen.display_msg("2_welcomelvl2.1")
    else:
        screen.display_msg("2_welcomelvl3")

    while gm.game_flag:
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
        if data.Level_Progress[2][2] == 0:
            screen.display_msg("2_winfirst1")
            screen.display_msg("2_winfirst2")
        else:
            screen.display_msg("2_winnotfirst")

        data.Level_Progress[2][0] = True
        data.Level_Progress[2][2] += 1

    else:
        screen.display_msg("2_loose1")
        screen.display_msg("2_loose2", data.ROBOT_TACTIC_NAME)
        screen.display_msg("2_loosechoose1", wait=False)
        inp = screen.input_str()

        if inp not in ("1", "0"):
            screen.display_msg("2_loosechoose2")
            inp = "1"
        if inp == "1":
            screen.display_msg("2_loosechoose3")
        else:
            screen.display_msg("2_loosechoose4", wait=False)
            inp = screen.input_str()

            if inp == "1":
                screen.display_msg("2_loosechoose5")
            else:
                screen.display_msg("2_loosechoose6")
        data.Level_Progress[1][0] = False

    data.Level_Progress[2][1] += 1

    gm.add_dices()
    screen.init_zones()
