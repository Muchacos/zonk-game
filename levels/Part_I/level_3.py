import classes
import data
from Levels.Part_I import scripts as s


def run(gm):
    scr = gm.screen
    player = classes.Human(gm, scr, data.PLAYER_NAME)
    enemy = classes.RobotRandom(gm, scr, data.ROBOT_CALCULATOR_NAME)
    hbar = data.HIGH_BARS["level_3"]
    embed_funcs = {
                   "anim_diceroll": scr.anim_diceroll,
                   "get_human_dices": s.get_human_dices_lev3,
                   "get_robot_dices": s.get_robot_dices_lev3,
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

    scr.display_msg_seq("3_welcomelvl_seq")

    # Пока игрок не начнет ход со счетом больше hbar - 500
    while gm.player.type == "Robot" or gm.player.score_total < hbar - 500:
        gm.action(embed_funcs, event_msgs)

    embed_funcs["get_human_dices"] = s.get_human_last_dices

    # Пока игрок не закончит ход со счетом больше hbar - 300
    while (gm.player.type == "Human" or
           gm.second_player.score_total < hbar - 300):
        gm.action(embed_funcs=embed_funcs)

    # Финальный бросок костей робота
    s.cheat_twist(gm)
    data.Game_Progress["level_3"]["is_complete"] = True
