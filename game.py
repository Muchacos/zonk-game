"""Здесь происходит объединение всех модулей в полноценную игру."""
import classes
import data
import graphics

screen = graphics.Screen()
screen.init_zones()
gm = classes.Game(screen)  # game_mode

while gm.game_flag:
    any_combos = gm.roll_dices()
    if any_combos is False:
        screen.display_msg("07_nocombos")
        gm.player.clear_scoreturn()
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
            break

    if action_choice == data.KEYCODES["TURN_END"]:
        gm.add_dices()
        gm.switch_player()

    elif (action_choice == data.KEYCODES["TURN_CONTINUE"] and
          len(gm.dices) == 0):
        gm.add_dices()

# Конец игры
screen.anim_ending()
del screen
