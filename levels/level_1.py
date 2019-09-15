import classes
import data


def run(gm, screen):
    enemy = classes.AI_easy(gm, screen, "zX01")
    player = classes.Human(gm, screen, data.PLAYER_NAME)

    screen.display_msg("03_robhello", data.PLAYER_NAME, enemy.name)
    screen.display_msg("04_0_gethbar", wait=False)

    while True:
        hbar = screen.input_str()
        if not hbar.isdigit():
            screen.display_msg("04_2_errint",
                               delay=data.TIMINGS["DELAY-ERR"])
        elif int(hbar) < 400 or int(hbar) > 20000:
            screen.display_msg("04_3_badval")
        else:
            hbar = int(hbar)
            break
        screen.display_msg("04_1_getaehbar", wait=False)

    gm.set_settings(hbar, player, enemy)
    screen.add_players(gm)
    screen.add_high_bar(hbar)

    screen.display_msg("05_gamestart")

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
                if gm.check_win() is True:
                    screen.display_msg("14_won", gm.player.name)
                    screen.display_msg("15_gameend")
                break

        if action_choice == data.KEYCODES["TURN_END"] and gm.game_flag:
            gm.add_dices()
            gm.switch_player()

        elif (action_choice == data.KEYCODES["TURN_CONTINUE"] and
              len(gm.dices) == 0 and gm.game_flag):
            gm.add_dices()

    gm.add_dices()
    screen.init_zones()
