import data
from .c_player_meta import PlayerMeta


class Human(PlayerMeta):
    """Представляет игрока по ту сторону экрана."""

    type = "Human"

    def get_dicechoose(self):
        dices = PlayerMeta.gm.dices
        screen = PlayerMeta.screen
        while True:
            inp = screen.input_str()
            # Проверка, есть ли все выбранные кости среди выпавших костей
            if (inp.isdigit() and
               all(inp.count(d) <= dices.count(int(d)) for d in inp)):
                return [int(d) for d in inp]
            else:
                pass  # FIXME: нужно сделать вывод сообщения об ошибке

    def get_actchoice(self):
        screen = PlayerMeta.screen
        while True:
            inp = screen.input_str()
            if inp in data.KEYCODES.values():
                return inp
            else:
                pass  # FIXME: нужно сделать вывод сообщения об ошибке
