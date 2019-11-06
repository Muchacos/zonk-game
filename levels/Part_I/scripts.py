import curses
import random as r
import time

import tools as t


#  ██╗ ███╗   ██╗ ████████╗ ██████╗   ██████╗
#  ██║ ████╗  ██║ ╚══██╔══╝ ██╔══██╗ ██╔═══██╗
#  ██║ ██╔██╗ ██║    ██║    ██████╔╝ ██║   ██║
#  ██║ ██║╚██╗██║    ██║    ██╔══██╗ ██║   ██║
#  ██║ ██║ ╚████║    ██║    ██║  ██║ ╚██████╔╝
#  ╚═╝ ╚═╝  ╚═══╝    ╚═╝    ╚═╝  ╚═╝  ╚═════╝
#
def paint_interface(screen):
    """Постепенно прорисовывает интерфейс."""
    stdscr = screen.stdscr
    SH, SW = screen.SH, screen.SW
    ZONE_DICES = screen.ZONE_DICES
    ZONE_INPUT = screen.ZONE_INPUT
    ZONE_SCORE = screen.ZONE_SCORE
    ZONE_MSG = screen.ZONE_MSG

    for y in range(SH - 1):
        stdscr.addstr(y, 0, "∙" * SW, curses.color_pair(screen.colorist.bkgd))
        stdscr.refresh()
        time.sleep(0.06)
    time.sleep(0.75)

    for zone, head in ([ZONE_DICES, "┤dices├"], [ZONE_SCORE, "┤score├"],
                       [ZONE_INPUT, "┤input├"], [ZONE_MSG, "┤msg├"]):
        screen.add_zone(zone, head)
        time.sleep(0.3)
    time.sleep(0.9)

    zonescore = [" Tot _____    _____ ",
                 " Tur _____    _____ ",
                 "     +        +     ",
                 " Win     _____      "]
    for i, y in enumerate((3, 5, 6, 7)):
        stdscr.addstr(ZONE_SCORE[0] + y, ZONE_SCORE[1], zonescore[i])
        stdscr.refresh()
        time.sleep(0.2)

    stdscr.addstr(ZONE_INPUT[0], ZONE_INPUT[1] - 1, ">")
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    time.sleep(0.7)


#  ██╗      ███████╗ ██╗   ██╗ ███████╗ ██╗      ███████╗  ██╗        ██████╗
#  ██║      ██╔════╝ ██║   ██║ ██╔════╝ ██║      ██╔════╝ ███║        ╚════██╗
#  ██║      █████╗   ██║   ██║ █████╗   ██║      ███████╗ ╚██║ █████╗  █████╔╝
#  ██║      ██╔══╝   ╚██╗ ██╔╝ ██╔══╝   ██║      ╚════██║  ██║ ╚════╝ ██╔═══╝
#  ███████╗ ███████╗  ╚████╔╝  ███████╗ ███████╗ ███████║  ██║        ███████╗
#  ╚══════╝ ╚══════╝   ╚═══╝   ╚══════╝ ╚══════╝ ╚══════╝  ╚═╝        ╚══════╝
#
def get_human_dices_lev12(gm):
    n_dices = len(gm.dices)
    chance = r.randint(10, 90)
    if t.chance(chance):
        dices = t.good_dices(n_dices)
    else:
        dices = t.rand_dices(n_dices)
    return dices


def get_robot_dices_lev12(gm):
    n_dices = len(gm.dices)
    score_to_win = gm.high_bar - gm.player.score_total + gm.player.score_turn
    while True:
        dices = t.rand_dices(n_dices)
        possible_score = t.dices_info(dices)["score"]
        if possible_score == 0 and t.chance(25):
            continue
        if possible_score < score_to_win and possible_score < 1000:
            break
    return dices


#   ██╗      ███████╗ ██╗   ██╗ ███████╗ ██╗      ██████╗
#   ██║      ██╔════╝ ██║   ██║ ██╔════╝ ██║      ╚════██╗
#   ██║      █████╗   ██║   ██║ █████╗   ██║       █████╔╝
#   ██║      ██╔══╝   ╚██╗ ██╔╝ ██╔══╝   ██║       ╚═══██╗
#   ███████╗ ███████╗  ╚████╔╝  ███████╗ ███████╗ ██████╔╝
#   ╚══════╝ ╚══════╝   ╚═══╝   ╚══════╝ ╚══════╝ ╚═════╝
#
def get_human_dices_lev3(gm):
    while True:
        dices = get_human_dices_lev12(gm)
        possible_score = t.dices_info(dices)["score"]
        human_scr = gm.player.score_total + gm.player.score_turn
        if possible_score + human_scr <= gm.high_bar - 400:
            break
    return dices


def get_robot_dices_lev3(gm):
    while True:
        dices = get_robot_dices_lev12(gm)
        possible_score = t.dices_info(dices)["score"]
        robot_scr = gm.player.score_total + gm.player.score_turn
        if possible_score + robot_scr <= gm.high_bar - 250:
            break
    return dices


def get_human_last_dices(gm):
    n_dices = len(gm.dices)
    if n_dices == 6:
        return [2, 2, 2, 3, 4, 6]
    elif n_dices == 3:
        return [1, 6, 2]
    elif n_dices == 2:
        return [5, 4]
    else:
        return t.bad_dices(n_dices)


def cheat_twist(gm):
    scr = gm.screen
    robot = gm.player
    robname = robot.name
    dropped_dices = t.bad_dices(6)
    cheated_dices = [1, 1, 1, 1, 1, 1]

    scr.anim_diceroll(6)
    scr.display_dices(dropped_dices)
    time.sleep(4)
    scr.display_dices(cheated_dices)
    time.sleep(1.5)
    # иммитация взятия костей роботом и начисления очков
    scr.effect_hldices(cheated_dices)
    robot.add_scorepick(4000)
    scr.msg_display_attron(delay=3)
    scr.display_msg("a_robturnF")
    scr.effect_hldices(cheated_dices, cp=2)
    robot.add_scoreturn()
    scr.display_msg("a_scrpick", robname, 4000)
    robot.add_scoretotal()
    scr.display_msg("a_scrtotl", robname, robot.score_total)
    scr.display_msg("3_robwin", robname)
    scr.msg_display_attroff(delay=True)
    scr.clear_zone(scr.ZONE_MSG)
    scr.clear_zone(scr.ZONE_SCORE)
    time.sleep(2.5)


def interface_fade(screen):
    colorist = screen.colorist
    fade_palettes = [
                     (40, 204, 204, 204, 43, 46, 49, 40),
                     (41, 204, 204, 204, 44, 47, 50, 41),
                     (42, 204, 204, 204, 45, 48, 51, 42),
                     colorist.FIRST_LEVEL
    ]
    for palette in fade_palettes:
        colorist.change_color_palette(palette)
        screen.add_interface()
        time.sleep(2)
