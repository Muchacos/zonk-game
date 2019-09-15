"""Здесь происходит объединение всех модулей в полноценную игру."""
import classes
import graphics
from levels import intro, level_1, level_2

screen = graphics.Screen()
gm = classes.Game(screen)  # game_mode

intro.run(screen)
level_1.run(gm, screen)
gm.game_flag = True
level_2.run(gm, screen)

# Конец игры
screen.anim_ending()
del screen
