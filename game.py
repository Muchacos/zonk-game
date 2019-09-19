"""Здесь происходит объединение всех модулей в полноценную игру."""
import sys

import classes
import data
import graphics
from levels import intro, level_1, level_2, level_3

screen = graphics.Screen()
gm = classes.Game(screen)  # game_mode

args = sys.argv

if len(args) != 1:
    screen.init_zones()
    if args[1] == "-lvl2":
        data.Level_Progress[1][0] = True
    elif args[1] == "lvl3":
        data.Level_Progress[1][0] = True
        data.Level_Progress[2][0] = True
else:
    intro.run(screen)

while True:
    if data.Level_Progress[1][0] is False:
        level_1.run(gm, screen)
    elif data.Level_Progress[2][0] is False:
        level_2.run(gm, screen)
    elif data.Level_Progress[3][0] is False:
        level_3.run(gm, screen)
    else:
        break
    gm.game_flag = True


screen.anim_ending()
del screen
