import data
import tools as t
from .c_robot_meta import RobotMeta


class RobotTactic(RobotMeta):
    """Представляет робота-тактика."""

    def get_dicechoose(self):
        gm = RobotMeta.gm
        self.dices_for_pick = gm.dices[:]
        self.claw = []
        dices = self.dices_for_pick
        singles = dices.count(1) + dices.count(5)

        if t.has_rangecombo(dices):
            self.take_range()
            if t.has_singlecombo(dices):
                self.take_single()

        elif t.has_rowcombo(dices):
            self.take_row()
            if t.has_singlecombo(dices) and t.chance(25):
                self.take_single()

        # Забирам все единичные кости, если остались только они
        elif singles == len(dices):
            self.take_single()

        # Если костей больше трех, то забираем одну с шансом 75% или все
        elif len(dices) > 3:
            if t.chance(75) or singles == 1:
                self.take_single(1)
            else:
                self.take_single()

        # Если кости три или меньше, то забираем все с шансом 75% или одну
        elif len(dices) <= 3:
            if singles > 1 and t.chance(75):
                self.take_single()
            else:
                self.take_single(1)

        # Забираем единичные кости, если таковые остались и принесут победу
        possible_points = t.dices_info(dices)["score"]
        if (t.has_singlecombo(dices) and possible_points +
           self.score_turn + self.score_total >= gm.high_bar):
            self.take_single()

        if self.thinking is True:
            delay = (r.uniform(0.7, 1.5) + len(dices) / 10) * -1
            RobotMeta.screen.display_msg("a_robthink", delay=delay)
        return self.claw

    def get_actchoice(self):
        def chance_curve(x):
            """Возвращает шанс продолжить ход, вычисляемый функцией 'y'."""
            # x - кол-во очков, y - шанс
            if x < 200:
                y = 100
            elif x > 1800:
                y = 0
            else:
                y = round(-2.5 * (x - 200)**(1 / 2) + 100)
            return y

        dices = RobotMeta.gm.dices
        n_dices = len(dices)
        chance_to_continue = chance_curve(self.score_turn)

        # Нюансы, увеличивающие или уменьшающие шанс продолжить ход
        if (self.score_total + self.score_turn
           + self.score_pick >= RobotMeta.gm.high_bar):
            chance_to_continue = 0
        elif n_dices == 0:
            chance_to_continue += 90
        elif n_dices == 5:
            chance_to_continue += 30
        elif n_dices < 3:
            chance_to_continue -= 30

        choice = t.chance(chance_to_continue)
        if choice is True:
            return data.KEYCODES["TURN_CONTINUE"]
        else:
            return data.KEYCODES["TURN_END"]
