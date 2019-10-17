"""Здесь происходит объединение всех модулей в полноценную игру."""
import sys

import classes
import data
import graphics
from levels import intro, level_1, level_2, level_3, unreliable_host

screen = graphics.Screen()
gm = classes.Game(screen)  # game_mode
progress = data.Game_Progress
args = sys.argv

# Аргументы запуска. Определяют, с какого уровня начнется игра.
if len(args) != 1:
    screen.init_zones()
    if args[1] == "-lvl2":
        progress["level_1"]["is_complete"] = True
    elif args[1] == "-lvl3":
        progress["level_1"]["is_complete"] = True
        progress["level_2"]["is_complete"] = True
else:
    intro.run(screen)

# Цикл, запускающий уровни игры
while True:
    if progress["level_1"]["is_complete"] is False:
        level_1.run(gm, screen)
    elif progress["level_2"]["is_complete"] is False:
        level_2.run(gm, screen)
    elif progress["level_3"]["is_complete"] is False:
        level_3.run(gm, screen)
    else:
        break
    gm.game_flag = True

# Запуск финальной (на данный момент) части
unreliable_host.run(screen)

# Конец игры
screen.anim_ending()
del screen
