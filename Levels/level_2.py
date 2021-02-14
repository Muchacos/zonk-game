import data
import tools as t
from . import scripts as s
from Classes.Players import c_human, c_robot_tactic


def run(gm):
    scr = gm.screen
    player = c_human.Human(gm, scr, data.PLAYER_NAME)
    enemy = c_robot_tactic.RobotTactic(gm, scr, data.ROBOT_TACTIC_NAME)
    hbar = data.HIGH_BARS["level_2"]
    embed_funcs = {
                   "anim_diceroll": scr.anim_diceroll,
                   "get_human_dices": s.get_human_dices_lev12,
                   "get_robot_dices": s.get_robot_dices_lev12,
                   "display_dices": scr.display_dices,
    }
    event_msgs = {
                  "whoturn": "a_whoturn",
                  "nocombos": "a_nocombos",
                  "getpick": "a_getpick",
                  "badpick": "a_badpick",
                  "badallpick": "a_badallpick",
                  "actchoice": "a_actchoice",
                  "h_scrpick": "a_scrpick",
                  "r_scrpick": "a_scrpick",
                  "h_scrtotl": "a_scrtotl",
                  "r_scrtotl": "a_scrtotl"
    }

    gm.set_settings(hbar, player, enemy)
    scr.add_players(gm)
    scr.add_high_bar(hbar)

    if t.games_count("level_2") == 0:
        scr.display_msg_seq("2_welcomelvl_seq")
        scr.display_msg("2_robotname", data.PLAYER_NAME,
                        data.ROBOT_TACTIC_NAME)

    while gm.game_flag:
        gm.action(embed_funcs, event_msgs)

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
