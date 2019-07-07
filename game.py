from classes import *

game_mode = Game()
printer = Printer(game_mode)
settings = printer.get_settings()
player = settings[0]
high_bar = settings[1]
game_mode.set_settings(player, high_bar, printer)

while game_mode.game_flag:
    turn_result = game_mode.turn()
    if turn_result is False or len(game_mode.dices) == 0:
        game_mode.add_dices()
