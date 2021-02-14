from .c_player_meta import PlayerMeta


class RobotMeta(PlayerMeta):
    """Представляет базовый класс Роботов.

    Поля:
    claw -- клешня робота, в которой он хранит выбранные кости
    dices_for_pick -- копия списка с выпавшими костями. Ее использование
                      освобождает от передачи списка dices как аргумента в
                      функции take_*
    thinking -- булевая переменная, определяющая, будет ли робот думать,
                задерживая свой ход

    """

    type = "Robot"

    def __init__(self, game_mode, screen, name, thinking=False):
        PlayerMeta.__init__(self, game_mode, screen, name)
        self.claw = []
        self.dices_for_pick = []
        self.thinking = thinking

    def take_range(self):
        """Забирает в claw наибольший диапазон костей."""
        claw = self.claw
        dices = self.dices_for_pick
        if 6 in dices:
            claw.extend(range(1, 7))
            dices.clear()
        else:
            for d in range(1, 6):
                claw.append(d)
                dices.remove(d)

    def take_row(self):
        """Забирает в claw ряд(ы) костей."""
        claw = self.claw
        dices = self.dices_for_pick[:]
        for d in dices:
            if dices.count(d) >= 3:
                claw.append(d)
                self.dices_for_pick.remove(d)

    def take_single(self, amount=4):
        """Забирает в claw единичные кости, где amount - количество."""
        claw = self.claw
        dices = self.dices_for_pick
        # По умолчанию amount = 4, т.к. это максимальное число единичных косей
        for i in (1, 5):  # Сначала забираются кости со значением "1"
            for d in dices[:]:
                if amount == 0:
                    break
                if d == i:
                    claw.append(d)
                    dices.remove(d)
                    amount -= 1

    def rowcombo_dice(self):
        """Возвращает значение костей, образующих комбо 'row'."""
        dices = self.dices_for_pick
        out = []
        for d in dices:
            if dices.count(d) >= 3 and d not in out:
                out.append(d)
        return out
