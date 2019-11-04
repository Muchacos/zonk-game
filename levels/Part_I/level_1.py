import classes
import data
import tools as t
from Levels.Part_I import scripts as s


def run(gm):
    scr = gm.screen
    player = classes.Human(gm, scr, data.PLAYER_NAME)
    enemy = classes.RobotRandom(gm, scr, data.ROBOT_RANDOM_NAME)
    hbar = data.HIGH_BARS["level_1"]
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

    if t.games_count("level_1") == 0:
        scr.display_msg("1_welcomelvl", data.PLAYER_NAME)
        scr.display_msg_seq("1_welcomelvl_seq")

    while gm.game_flag:
        gm.action(embed_funcs, event_msgs)

    winner = gm.player.type
    if winner == "Human":
        scr.display_msg("1_win1", data.PLAYER_NAME)
        scr.display_msg("1_win2")
        scr.display_msg("1_win3")
        data.Game_Progress["level_1"]["is_complete"] = True
    else:
        scr.display_msg_seq("1_loose_seq")
        data.Game_Progress["level_1"]["games"] += 1

    scr.add_zonescore()
    scr.clear_zone(scr.ZONE_DICES)
    scr.clear_zone(scr.ZONE_MSG)
