from classes import Game, Printer, Robot

game_mode = Game()
printer = Printer(game_mode)
player_human = printer.input_player()
player_ai = Robot(game_mode, printer, 'zX01')
game_mode.set_settings(player_human, player_ai,
                       printer.input_highbar(), printer)

# Основной цикл игры
while game_mode.game_flag:
    # Совершение дейстие в ход. Выясняется, нужно ли добавить кости
    action_result = game_mode.action()
    if action_result in (-2, -1, 2):
        game_mode.add_dices()
    if action_result < 0:
        game_mode.switch_player()
