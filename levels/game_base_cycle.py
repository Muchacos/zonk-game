import data
import tools as tls


def main(gm):
    hbar = gm.high_bar

    while gm.game_flag:
        is_human = gm.player.__type__ == "Human"
        dices_amount = len(gm.dices)

        if is_human:
            human_scr = gm.player.score_total + gm.player.score_turn
            robot_scr = (gm.second_player.score_total +
                         gm.second_player.score_turn)
            if human_scr >= hbar and tls.chance(40):
                dices = tls.cheat_good_dices(dices_amount, clear=False)
            elif robot_scr - human_scr > 500:
                if tls.chance(80):
                    dices = tls.cheat_good_dices(dices_amount, clear=False)
                elif dices_amount <= 4 and tls.chance(80):
                    dices = tls.cheat_good_dices(dices_amount, clear=True)
                else:
                    dices = tls.rand_dices(dices_amount)
            elif hbar - robot_scr < 300 and tls.chance(75):
                dices = tls.cheat_good_dices(dices_amount, clear=False)
            else:
                dices = tls.rand_dices(dices_amount)

        else:
            human_scr = (gm.second_player.score_total +
                         gm.second_player.score_turn)
            robot_scr = gm.player.score_total + gm.player.score_turn
            score_to_win = hbar - robot_scr

            for i in range(50):
                possible_dices = tls.rand_dices(dices_amount)
                possible_dices_score = tls.dices_score(possible_dices)
                if possible_dices_score != 0:
                    if possible_dices_score < score_to_win:
                        print(possible_dices_score, score_to_win, robot_scr)
                        break
                elif tls.chance(70):
                    continue
                else:
                    break

            else:
                gm.screen.beep()
                if tls.chance(90):
                    possible_dices = tls.cheat_bad_dices(dices_amount)
                elif tls.chance(90):
                    possible_dices = tls.cheat_bad_dices(dices_amount,
                                                         onefive=True)
            dices = possible_dices

        gm.remdis_dices(dices)
        any_combos = gm.nocombos_managing()

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
