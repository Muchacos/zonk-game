import classes
import data


def run(gm, screen):
    # Установка игровых параметров
    player = classes.Human(gm, screen, data.PLAYER_NAME)
    enemy = classes.Robot_tactic(gm, screen, data.ROBOT_TACTIC_NAME)
    hbar = 110

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

    # Действия при победе/поражении
    if gm.player.__type__ == "Human":
        screen.display_msg_seq("2_win_seq")
        data.Game_Progress["level_2"]["is_complete"] = True
    else:
        screen.display_msg_seq("2_loose_seq")
        data.Game_Progress["level_2"]["losses"] += 1

    gm.add_dices()
    screen.init_zones()
