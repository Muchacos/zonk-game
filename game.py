"""Здесь происходит объединение всех модулей в полноценную игру."""
import sys

import classes
import data
import graphics
import tools as t
from Levels.Part_I import intro, level_1, level_2, level_3, unreliable_host

screen = graphics.Screen()
colorist = classes.Colorist(screen)
screen.set_colorist(colorist)
gm = classes.Game(screen, colorist)  # game_mode

progress = data.Game_Progress
args = sys.argv  # аргументы определяют, с какого уровня начнется игра

if len(args) != 1:
    screen.add_interface()
    if args[1] == "-lvl2":
        progress["level_1"]["is_complete"] = True
    elif args[1] == "-lvl3":
        progress["level_1"]["is_complete"] = True
        progress["level_2"]["is_complete"] = True
else:
    intro.run(screen)

# Цикл, запускающий уровни игры
while True:
    if not t.is_complete("level_1"):
        level_1.run(gm)
    elif not t.is_complete("level_2"):
        level_2.run(gm)
    elif not t.is_complete("level_3"):
        level_3.run(gm)
    else:
        break
    gm.game_flag = True

unreliable_host.run(screen)
screen.anim_ending()
del screen
