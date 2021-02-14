import random as r

import data
import tools as t
from .c_robot_meta import RobotMeta


class RobotRandom(RobotMeta):
    """Представляет робота, полагающегося на случайность."""

    def get_dicechoose(self):
        gm = RobotMeta.gm
        self.claw = []
        self.dices_for_pick = gm.dices[:]
        dices = self.dices_for_pick
        ones, fives = dices.count(1), dices.count(5)

        if t.has_rangecombo(dices):
            if t.chance(37):
                self.take_range()
                if ones + fives > 2 and t.chance(40):
                    self.take_single()
            elif ones + fives > 2 and t.chance(65):
                self.take_single()
            else:
                self.take_single(r.choice([1, 2]))

        elif t.has_rowcombo(dices):
            # Если костей два ряда, то забираем оба с шансом 90%
            if len(self.rowcombo_dice()) > 1 and t.chance(90):
                self.take_row()
            else:
                row_dice = self.rowcombo_dice()[0]
                # Вместо ряда забираем единичные кости, если ряд состоит из них
                if ((row_dice == 1 and fives != 0 and t.chance(36))
                   or (row_dice == 5 and ones != 0 and t.chance(40))):
                    self.take_single(2)
                elif row_dice not in (1, 5):
                    self.take_row()
                    # Забираем ещи и единичные с шансом 40%
                    if ones + fives > 0 and t.chance(40):
                        self.take_single()
                else:
                    self.take_row()

        # Если остались единичные и мы брали кости
        if t.has_singlecombo(dices) and len(self.claw) != 0:
            # Если все оставшиеся кости - единичные
            if len(dices) == ones + fives:
                if t.chance(84):  # То берем их все с шансом 84%
                    self.take_single()
                else:  # Либо забираем их случайное количество (но не все)
                    self.take_single(r.choice(range(1, len(dices))))
            elif ones + fives > 2 and t.chance(50):
                self.take_single(2)
            elif t.chance(50):
                self.take_single(1)

        if len(self.claw) == 0:
            if len(dices) == ones + fives:
                if len(dices) == 1 or t.chance(84):
                    self.take_single()
                else:
                    self.take_single(r.choice(range(1, len(dices))))
            # Забираем 3/2/1/все единичные кости по условиям
            elif ones + fives == 4 and t.chance(73):
                self.take_single(3)
            elif ones + fives > 2 and t.chance(52):
                self.take_single(2)
            elif t.chance(31):
                self.take_single(1)
            else:
                self.take_single()

        if self.thinking is True:
            delay = (r.uniform(0.7, 1.5) + len(dices) / 10) * -1
            RobotMeta.screen.display_msg("a_robthink", delay=delay)
        return self.claw

    def get_actchoice(self):
        gm = RobotMeta.gm
        n_dices = len(t.exclude_array(gm.dices, self.claw))
        chance_to_continue = 0

        if n_dices == 0:
            chance_to_continue = 93
        elif n_dices in (4, 5):
            chance_to_continue = r.randint(70, 90)
        elif n_dices == 3:
            chance_to_continue = r.randint(60, 70)
        elif n_dices == 2:
            chance_to_continue = r.randint(20, 50)
        else:
            chance_to_continue = r.randint(10, 30)

        scores = self.score_pick + self.score_turn + self.score_total
        if scores >= gm.high_bar:
            chance_to_continue = r.randint(1, 10)
        elif scores >= gm.second_player.score_total:
            chance_to_continue += r.randint(9, 24)

        turn_score = self.score_pick + self.score_turn
        if turn_score >= r.randint(700, 1000):
            chance_to_continue -= r.randint(21, 39)
        elif turn_score >= r.randint(300, 600):
            chance_to_continue -= r.randint(15, 21)
        else:
            chance_to_continue += r.randint(10, 40)

        choice = t.chance(chance_to_continue)
        if choice is True:
            return data.KEYCODES["TURN_CONTINUE"]
        else:
            return data.KEYCODES["TURN_END"]
