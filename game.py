from classes import Game, Printer

game_mode = Game()
printer = Printer(game_mode)
player = printer.get_player()
game_mode.set_settings(player, printer.get_highbar(), printer)

# Основной цикл игры
while game_mode.game_flag:
    # Совершение дейстие в ход. Выясняется, нужно ли добавить кости
    need_dices = game_mode.action()
    if need_dices is True:
        game_mode.add_dices()
