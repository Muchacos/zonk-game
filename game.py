import classes as cls
import graphics

gm = cls.Game()  # game_mode
screen = graphics.Screen()
p_human = cls.Human(gm, screen, 'Human')
p_robot = cls.Robot(gm, screen, 'zX01')
gm.set_settings(p_human, p_robot, 1000, screen)

# Основной цикл игры
while gm.game_flag:
    # Совершение дейстие в ход. Выясняется, нужно ли добавить кости
    action_result = gm.action()
    if action_result in (-2, -1, 2):
        gm.add_dices()
    if action_result < 0 and gm.game_flag is True:
        gm.switch_player()
