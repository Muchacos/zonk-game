import classes
import data
import tools as t
from Levels.Part_I import scripts as s


def run(gm):
    scr = gm.screen
    player = classes.Human(gm, scr, data.PLAYER_NAME)
    enemy = classes.RobotTactic(gm, scr, data.ROBOT_RANDOM_NAME)
    hbar = data.HIGH_BARS["level_2"]
    embed_funcs = {
                   "anim_diceroll": scr.anim_diceroll,
                   "get_human_dices": s.get_human_dices_lev12,
                   "get_robot_dices": s.get_robot_dices_lev12,
                   "display_dices": scr.display_dices,
    }

    gm.set_settings(hbar, player, enemy)
    scr.add_players(gm)
    scr.add_high_bar(hbar)

    if t.games_count("level_2") == 0:
        scr.display_msg_seq("2_welcomelvl_seq")
        scr.display_msg("2_robotname", data.PLAYER_NAME,
                        data.ROBOT_TACTIC_NAME)

    while gm.game_flag:
        gm.action(embed_funcs=embed_funcs)

    winner = gm.player.type
    if winner == "Human":
        scr.display_msg_seq("2_win_seq")
        data.Game_Progress["level_2"]["is_complete"] = True
    else:
        scr.display_msg_seq("2_loose_seq")
        data.Game_Progress["level_2"]["losses"] += 1

    scr.add_zonescore()
    scr.clear_zone(scr.ZONE_DICES)
    scr.clear_zone(scr.ZONE_MSG)
