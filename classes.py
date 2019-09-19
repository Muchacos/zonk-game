"""Тут содержатся все классы, составляющие игровую логику."""
import random

import data
import tools

#   .d8888b.         d8888  888b     d888  8888888888
#  d88P  Y88b       d88888  8888b   d8888  888
#  888    888      d88P888  88888b.d88888  888
#  888            d88P 888  888Y88888P888  8888888
#  888  88888    d88P  888  888 Y888P 888  888
#  888    888   d88P   888  888  Y8P  888  888
#  Y88b  d88P  d8888888888  888   "   888  888
#   "Y8888P88 d88P     888  888       888  8888888888


class Game:
    """Представляет основной функционал игры.

    Термины:
    Ход (turn) -- событие, происходящее, пока игрок совершает действия (action)
    Действие (action) -- короткое событие, в котором игрок что-то делает
    Кости (dice/s) -- целч. переменные, представляющие игральные кости
    Очки для победы (high_bar) -- целч. значение, указывающее сколько итоговых
                                  очков необходимо набрать для победы.

    Поля класса:
    screen -- экземпляр класса Screen, представляющий экран игры

    Поля экземпляров:
    game_flag -- булевая переменная, указывающаяя может ли продолжаться игра
    dices -- список, содержащий от 1 до 6 игральных костей (их целочисленные
             значения)
    player -- текущий игрок (экземпляр класса Player)
    second_player -- второй игрок
    high_bar -- цел. значение очков необходимых для победы

    Методы:
    add_dices -- добавляет недостающие кости
    check_win -- проверяет, выйграл ли игрок

    Методы хода (функционал хода):
    roll_dices -- представляет бросок костей
    get_pick -- получет от игрока выбранные им кости
    get_action_choice -- получает от игрока выбранный им вариант действия
    add_scores -- добавляет очки за кости/ход


    """

    screen = None

    def __init__(self, screen):
        """Инициализация."""
        Game.screen = screen
        self.game_flag = True
        self.dices = [1] * 6
        self.temp_dices = []

    def set_settings(self, high_bar, player, enemy):
        self.player = player
        self.high_bar = high_bar
        self.second_player = enemy

    def switch_player(self):
        """Меняет игроков местами."""
        self.player, self.second_player = self.second_player, self.player
        Game.screen.anim_playerhl(self)
        Game.screen.display_msg("a_whoturn", self.player.name,
                                delay=data.TIMINGS["DELAY-FST"])

    def check_win(self):
        """Опускает game_flag в случае выйгрыша текущего игрока."""
        if self.player.score_total >= self.high_bar:
            self.game_flag = False
            return True
        return False

    def add_dices(self):
        """Добавляет недостающие кости (до 6 штук)."""
        self.dices.extend([1] * (6 - len(self.dices)))

#
#                            888     d8b
#                            888     Y8P
#                            888
#         8888b.    .d8888b  888888  888   .d88b.   88888b.
#            "88b  d88P"     888     888  d88""88b  888 "88b
#        .d888888  888       888     888  888  888  888  888
#        888  888  Y88b.     Y88b.   888  Y88..88P  888  888
#        "Y888888   "Y8888P   "Y888  888   "Y88P"   888  888

    def roll_dices(self, *, auto_managing=True):
        """Бросок костей. Иногда они выпадают случайно."""
        screen = self.screen
        dices = self.dices
        screen.anim_diceroll(len(dices))
        for i in range(len(self.dices)):
            dices[i] = random.randint(1, 6)
        self.temp_dices = dices[:]

        if auto_managing is True:
            screen.display_dices(dices)
            if tools.check_combos_any(dices) is False:
                screen.display_msg("a_nocombos")
                self.player.clear_scoreturn()

        return tools.check_combos_any(dices)

    def get_pick(self, *, raise_bad_pick=True, raise_bad_all_pick=True):
        """Получает выбранне игроком кости и выводит очки за них."""
        screen = self.screen
        player = self.player
        pick_score = 0
        # ИИ/Человек берет в "руку" какие-то выпавшие кости
        hand = player.get_dicechoose()
        screen.effect_hldices(hand)  # выделение выбранных костей
        # Происходят проверки на комбинации в руке, приносящие очки (поря-
        # док имеет значение!). Кости, приносящие очки, удаляются из руки
        # и из основного списка костей класса Game (но возвращаются из
        # temp_dices, в случае повторного выбора).

        if tools.check_combos_range(hand):
            if 6 in hand:
                pick_score += 1500
                hand.clear()
                self.dices.clear()
            else:
                pick_score += 750
                for i in range(1, 6):
                    hand.remove(i)
                    self.dices.remove(i)

        if tools.check_combos_row(hand):
            for dice in hand[:]:
                score = 0
                row_len = hand.count(dice)

                if row_len >= 3:
                    if dice == 1:
                        score += 1000
                    else:
                        score += dice * 100
                    score *= (row_len - 2)
                    pick_score += score

                    for i in range(row_len):
                        hand.remove(dice)
                        self.dices.remove(dice)

        if tools.check_combos_single(hand):
            for dice in hand[:]:

                if dice == 1:
                    pick_score += 100
                    hand.remove(dice)
                    self.dices.remove(dice)

                elif dice == 5:
                    pick_score += 50
                    hand.remove(dice)
                    self.dices.remove(dice)

        # Выводится сообщение, если никакие кости не принесли очков.
        # Цикл тут же начинается сначала.
        if pick_score == 0:
            if raise_bad_all_pick:
                screen.effect_hldices(hand, cp_id=4)
                screen.display_msg("a_badallpick", player.name)
                screen.effect_hldices()
            return pick_score
        # Выводится сообщение, если в руке остались кости, которые не при-
        # несли очки (но они используются далее в игре).
        elif len(hand) > 0 and raise_bad_pick:
            screen.effect_hldices(hand, cp_id=4)
            screen.display_msg("a_badpick")

        # Добавление очков за выбранные кости
        player.add_scorepick(pick_score)
        return pick_score

    def get_action_choice(self, *, auto_managing=True):
        """Возвращает то, что хочет сделать игрок далее."""
        player = self.player
        screen = self.screen
        temp_dices = self.temp_dices

        action_choice = player.get_nextaction()
        screen.effect_hldices()

        if auto_managing:
            # При отмене выбора, цикл продолжается
            if action_choice == data.KEYCODES["TURN_CANCEL"]:
                self.dices = temp_dices[:]  # возвращение удаленных костей
                player.clear_scorepick()
            # Если игрок согласен использовать выбранные кости,
            # то они скрываются.
            else:
                removed_dices = tools.exclude_array(temp_dices, self.dices)
                screen.effect_hldices(removed_dices, cp_id=6)

        return action_choice

    def add_scores(self, pick_score, action_choice, *, auto_msg=True):
        """Занимается добавлением очков."""
        player = self.player
        screen = self.screen

        player.add_scoreturn()
        if auto_msg:
            screen.display_msg("a_scrpick", player.name, pick_score)

        # Если игрок хочет закончить ход и сохнанить набранные очки:
        if action_choice == data.KEYCODES["TURN_END"]:
            # Убираем оставшиеся кости. Новый игрок - чистый стол
            screen.effect_hldices(screen.scr_dices, cp_id=6)
            player.add_scoretotal()
            if auto_msg:
                screen.display_msg("a_scrtotl", player.name,
                                   player.score_total)


#  8888888b.   888             d8888  Y88b   d88P  8888888888  8888888b.
#  888   Y88b  888            d88888   Y88b d88P   888         888   Y88b
#  888    888  888           d88P888    Y88o88P    888         888    888
#  888   d88P  888          d88P 888     Y888P     8888888     888   d88P
#  8888888P"   888         d88P  888      888      888         8888888P"
#  888         888        d88P   888      888      888         888 T88b
#  888         888       d8888888888      888      888         888  T88b
#  888         88888888 d88P     888      888      8888888888  888   T88b


class Player:
    """Представляет родительский класс игрока.

    Поля класса:
    gm -- основной функционал игры
    screen -- экран с полем для ввода данных

    Поля экземпляра:
    name -- имя игрока
    score_total -- итоговое число очков
    score_turn -- число очков за ход
    score_pick -- число очков за выбранные кости

    Методы:
    (add_*score_type*
    clear_*score_type*) -- добавление/удаление очков. Все изменения
                           отображаются на экране.

    """

    gm = None
    screen = None

    def __init__(self, game_mode, screen, name):
        """Инициализация."""
        Player.gm = game_mode
        Player.screen = screen
        self.name = name
        self.score_total = 0
        self.score_turn = 0
        self.score_pick = 0

    def add_scoretotal(self):
        """Добавляет score_turn к score_total."""
        self.score_total += self.score_turn
        self.score_turn = 0
        Player.screen.display_score(self, "turn")  # удаление очков с экрана
        Player.screen.display_score(self, "total")

    def add_scoreturn(self):
        """Перемещает score_pick в score_turn."""
        self.score_turn += self.score_pick
        self.score_pick = 0
        Player.screen.display_score(self, "pick")  # удаление очков с экрана
        Player.screen.display_score(self, "turn")

    def add_scorepick(self, score):
        """Увеличивает score_pick на score"""
        self.score_pick += score
        Player.screen.display_score(self, "pick")

    def clear_scoreturn(self):
        """Отчищает score_turn (очки за ход)."""
        self.score_turn = 0
        Player.screen.display_score(self, "turn")

    def clear_scorepick(self):
        self.score_pick = 0
        Player.screen.display_score(self, "pick")


#  888    888  888     888  888b     d888         d8888  888b    888
#  888    888  888     888  8888b   d8888        d88888  8888b   888
#  888    888  888     888  88888b.d88888       d88P888  88888b  888
#  8888888888  888     888  888Y88888P888      d88P 888  888Y88b 888
#  888    888  888     888  888 Y888P 888     d88P  888  888 Y88b888
#  888    888  888     888  888  Y8P  888    d88P   888  888  Y88888
#  888    888  Y88b. .d88P  888   "   888   d8888888888  888   Y8888
#  888    888   "Y88888P"   888       888  d88P     888  888    Y888


class Human(Player):
    """Представляет игрока по ту сторону экрана.

    Методы:
    get_dicechoose -- получает ввод от игрока с выбранными костями
    get_nextaction -- получает ввод от игрока, хочет ли он продолжить ход

    """

    __type__ = "Human"

    def get_dicechoose(self):
        """Возвращает выбранные игроком кости, если те существуют."""
        dices = Player.gm.dices
        screen = Player.screen
        while True:
            screen.display_msg("a_getpick", wait=False)
            inp = screen.input_str()
            # Проверка, есть ли все выбранные кости среди выпавших костей
            if (inp.isdigit()
                    and all(inp.count(d) <= dices.count(int(d)) for d in inp)):
                return [int(d) for d in inp]
            else:
                screen.display_msg("a_errpick",
                                   delay=data.TIMINGS["DELAY-ERR"])

    def get_nextaction(self):
        """Узнает, готов ли игрок рискнуть продолжить ход."""
        screen = Player.screen
        while True:
            screen.display_msg("a_actchoose", wait=False, speedup=2)
            inp = screen.input_str()

            if inp in data.KEYCODES.values():
                return inp
            else:
                screen.display_msg("a_badans",
                                   delay=data.TIMINGS["DELAY-ERR"])


#  8888888b.    .d88888b.   888888b.     .d88888b.  88888888888
#  888   Y88b  d88P" "Y88b  888  "88b   d88P" "Y88b     888
#  888    888  888     888  888  .88P   888     888     888
#  888   d88P  888     888  8888888K.   888     888     888
#  8888888P"   888     888  888  "Y88b  888     888     888
#  888 T88b    888     888  888    888  888     888     888
#  888  T88b   Y88b. .d88P  888   d88P  Y88b. .d88P     888
#  888   T88b   "Y88888P"   8888888P"    "Y88888P"      888

class Robot_meta(Player):
    """Представляет базовый класс Роботов.

    take_*combo* -- взятие роботом определенной комбинации костей

    """

    __type__ = "Robot"

    def __init__(self, game_mode, screen, name, thinking=False):
        Player.__init__(self, game_mode, screen, name)
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
        """Возвращает значения костей, образующих комбо 'row'."""
        dices = self.dices_for_pick
        out = []
        for d in dices:
            if dices.count(d) >= 3 and d not in out:
                out.append(d)
        return out


class Robot_random(Robot_meta):
    """Представляет робота, полагающегося на случайность."""

    def get_dicechoose(self):
        gm = Player.gm
        self.dices_for_pick = gm.dices[:]
        self.claw = []
        dices = self.dices_for_pick
        ones, fives = dices.count(1), dices.count(5)

        if tools.check_combos_range(dices):
            if tools.chance(37):
                self.take_range()
                if ones + fives > 2 and tools.chance(40):
                    self.take_single()
            elif ones + fives > 2 and tools.chance(65):
                self.take_single()
            else:
                self.take_single(random.choice([1, 2]))

        elif tools.check_combos_row(dices):
            if len(self.rowcombo_dice()) > 1 and tools.chance(90):
                self.take_row()
            else:
                row_dice = self.rowcombo_dice()[0]
                if ((row_dice == 1 and fives != 0 and tools.chance(36))
                   or (row_dice == 5 and ones != 0 and tools.chance(40))):
                    self.take_single()
                elif row_dice not in (1, 5):
                    if ones + fives > 0 and tools.chance(40):
                        self.take_single()
                        self.take_row()
                    else:
                        self.take_row()
                else:
                    self.take_row()

        if tools.check_combos_single(dices) and len(self.claw) != 0:
            if len(dices) == ones + fives:
                if tools.chance(84):
                    self.take_single()
                else:
                    self.take_single(random.choice(range(1, len(dices))))
            elif ones + fives > 2 and tools.chance(50):
                self.take_single(2)
            elif tools.chance(50):
                self.take_single(1)

        if len(self.claw) == 0:
            if len(dices) == ones + fives:
                if len(dices) == 1 or tools.chance(84):
                    self.take_single()
                else:
                    self.take_single(random.choice(range(1, len(dices))))
            elif ones + fives == 4 and tools.chance(73):
                self.take_single(3)
            elif ones + fives > 2 and tools.chance(52):
                self.take_single(2)
            elif tools.chance(31):
                self.take_single(1)
            else:
                self.take_single()

        if self.thinking is True:
            delay = (random.uniform(0.7, 1.5) + len(dices) / 10) * -1
            Player.screen.display_msg("a_robthink", delay=delay)
        return self.claw

    def get_nextaction(self):
        gm = Player.gm
        dices = gm.dices
        chance_to_continue = 0

        if len(dices) == 0:
            chance_to_continue = 93
        elif len(dices) in (4, 5):
            chance_to_continue = random.randint(70, 90)
        elif len(dices) == 3:
            chance_to_continue = random.randint(60, 70)
        elif len(dices) == 2:
            chance_to_continue = random.randint(20, 50)
        else:
            chance_to_continue = random.randint(10, 30)

        scores = self.score_pick + self.score_turn + self.score_total
        if scores >= gm.high_bar:
            chance_to_continue = random.randint(1, 10)
        elif scores >= gm.second_player.score_total:
            chance_to_continue += random.randint(9, 24)

        turn_score = self.score_pick + self.score_turn
        if turn_score >= random.randint(700, 1000):
            chance_to_continue -= random.randint(21, 39)
        elif turn_score >= random.randint(300, 600):
            chance_to_continue -= random.randint(15, 21)
        else:
            chance_to_continue += random.randint(10, 40)

        choice = tools.chance(chance_to_continue)
        if choice is True:
            Player.screen.display_msg("a_robturnT")
            return data.KEYCODES["TURN_CONTINUE"]
        else:
            Player.screen.display_msg("a_robturnF")
            return data.KEYCODES["TURN_END"]


class Robot_tactic(Robot_meta):
    """Представляет робота-тактика."""

    def get_dicechoose(self):
        """Возвращает выбранные ИИ кости."""
        gm = Player.gm
        self.dices_for_pick = gm.dices[:]
        self.claw = []
        dices = self.dices_for_pick
        singles = dices.count(1) + dices.count(5)

        # Если есть диапазон костей, то забираем его
        if tools.check_combos_range(dices):
            self.take_range()
            # Если остались еще кости, то забираем их
            if tools.check_combos_single(dices):
                self.take_single()

        # Если есть ряд костей, то забрать весь (все) ряд(ы)
        elif tools.check_combos_row(dices):
            self.take_row()
            # Если еще остались единичные кости
            if tools.check_combos_single(dices):
                # Забирам их при условии, что всего косей меньше трех
                # (+ шанс 60%) или с шансом 25%.
                if (len(dices) < 3 and tools.chance(60)
                        or tools.chance(25)):
                    self.take_single()

        # Забирам все единичные кости, если остались только они
        elif singles == len(dices):
            self.take_single()

        # Если костей больше трех, то забираем одну с шансом 75% или все
        elif len(dices) > 3:
            if tools.chance(75) or singles == 1:
                self.take_single(1)
            else:
                self.take_single()

        # Если кости три или меньше, то забираем все с шансом 75% или одну
        elif len(dices) <= 3:
            if singles > 1 and tools.chance(75):
                self.take_single()
            else:
                self.take_single(1)

        new_ones, new_fives = dices.count(1), dices.count(5)
        if new_ones + new_fives > 0:
            possible_points = new_ones * 100 + new_fives * 50
            if (possible_points + self.score_pick + self.score_turn
               + self.score_total > gm.high_bar):
                self.take_single()

        if self.thinking is True:
            delay = (random.uniform(0.7, 1.5) + len(dices) / 10) * -1
            Player.screen.display_msg("a_robthink", delay=delay)
        return self.claw

    def get_nextaction(self):
        """Узнает, готов ли робот рискнуть продолжить ход."""

        # Возвращает шанс продолжить ход по графику y = -2.5(x-200)^1/2 + 100
        def chance_curve(x):
            if x < 200:
                y = 100
            elif x > 1800:
                y = 0
            else:
                y = round(-2.5 * (x - 200)**(1 / 2) + 100)
            return y

        dices = Player.gm.dices
        chance_to_continue = chance_curve(self.score_turn)
        # После вычисления шанса по формуле, рассматриваются нюансы, увеличива-
        # ющие или уменьшающие риск потерять накопленные очки. Они увеличивают,
        # либо уменьшают шанс продолжить ход:

        # Если текущее кол-во очнов больше кол-ва очков для победы, то
        # продолжать ход и рисковать не имеет смысла.
        if (self.score_total + self.score_turn
           + self.score_pick >= Player.gm.high_bar):
            chance_to_continue = 0
        elif len(dices) == 0:
            chance_to_continue += 90
        elif len(dices) == 5:
            chance_to_continue += 30
        elif len(dices) < 3:
            chance_to_continue -= 30

        choice = tools.chance(chance_to_continue)
        if choice is True:
            Player.screen.display_msg("a_robturnT")
            return data.KEYCODES["TURN_CONTINUE"]
        else:
            Player.screen.display_msg("a_robturnF")
            return data.KEYCODES["TURN_END"]
