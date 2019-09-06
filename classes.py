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
    game_flag -- булевая переменная, указывающаяя может ли продолжаться игра
    screen -- экземпляр класса Screen, представляющий экран игры
    dices -- список, содержащий от 1 до 6 игральных костей (их целочисленные
             значения)

    Поля экземпляров:
    player -- текущий игрок (экземпляр класса Player)
    second_player -- второй игрок
    high_bar -- цел. значение очков необходимых для победы

    Методы:
    action -- основной функционал действия
    add_dices -- добавляет недостающие кости
    check_win -- проверяет, выйграл ли игрок
    check_combos -- проверяет, есть ли хоть одно комбо среди костей
    (check_combosrow,
    check_combosrange,
    check_combossingle) -- проверка комбинаций среди костей

    """

    game_flag = True
    screen = None
    dices = [1] * 6

    def __init__(self, screen):
        """Инициализация со вступлением."""
        Game.screen = screen
        # Приветствие
        screen.display_msg("01_hello")

        # Получение имени игрока
        while True:
            screen.display_msg("02_0_getname", wait=False)
            name = screen.input_str()
            if len(name) == 0:
                screen.display_msg("02_2_stdname")
                name = "Человек"
                break
            elif len(name) <= 6 and len(name) >= 3:
                break
            else:
                screen.display_msg("02_1_badname",
                                   delay=data.TIMINGS["DELAY-ERR"])
        self.player = Human(self, screen, name)

        # Приветствие робота
        self.second_player = AI_hard(self, screen, "zX01")
        screen.display_msg("03_robhello", name, self.second_player.name)
        screen.add_players(self)  # Вывод имен игроков

        # Установка очков для победы
        screen.display_msg("04_0_gethbar", wait=False)
        while True:
            hbar = screen.input_str()
            if not hbar.isdigit():
                screen.display_msg("04_2_errint",
                                   delay=data.TIMINGS["DELAY-ERR"])
            elif int(hbar) < 400 or int(hbar) > 20000:
                screen.display_msg("04_3_badval")
            else:
                self.high_bar = int(hbar)
                break
            screen.display_msg("04_1_getaehbar", wait=False)
        screen.add_high_bar(hbar)  # Вывод очков для победы

        # Начало игры
        screen.display_msg("05_gamestart")

    def switch_player(self):
        """Меняет игроков местами."""
        self.player, self.second_player = self.second_player, self.player
        Game.screen.anim_playerhl(self)
        Game.screen.display_msg("06_whoturn", self.player.name,
                                delay=data.TIMINGS["DELAY-FST"])

    def check_win(self):
        """Опускает game_flag в случае выйгрыша текущего игрока."""
        if self.player.score_total >= self.high_bar:
            Game.game_flag = False
            Game.screen.display_msg("14_won", self.player.name)
            Game.screen.display_msg("15_gameend")

    def check_combosrow(self, dices):
        """Возвращает True, если среди костей есть >= три одинаковых кости."""
        return any(dices.count(d) >= 3 for d in dices)

    def check_combosrange(self, dices):
        """Возвращает True, если среди костей есть все кости от 1 до 5."""
        return all(d in dices for d in range(1, 6))

    def check_combossingle(self, dices):
        """Возвращает True, если среди костей есть кость 1 или 5."""
        return any(d in dices for d in (1, 5))

    def check_combos(self):
        """Возвращает True, если среди костей есть хотя бы одна комбинация."""
        d = Game.dices
        return any([self.check_combosrow(d), self.check_combosrange(d),
                    self.check_combossingle(d)])

    def add_dices(self):
        """Добавляет недостающие кости (до 6 штук)."""
        Game.dices.extend([1] * (6 - len(Game.dices)))

#
#                            888     d8b
#                            888     Y8P
#                            888
#         8888b.    .d8888b  888888  888   .d88b.   88888b.
#            "88b  d88P"     888     888  d88""88b  888 "88b
#        .d888888  888       888     888  888  888  888  888
#        888  888  Y88b.     Y88b.   888  Y88..88P  888  888
#        "Y888888   "Y8888P   "Y888  888   "Y88P"   888  888

    def action(self):
        """Совершение действия в ход. Возвращает исход действия в числе.

        Отрицательные значения (-1, -2) означают, что ход должен передасться
        другому игроку. Положительные - ход не передается.

        Кости НЕ добавятся в сдедуюищй ход (возвращает False) если:
        0 - игра уже закончена
        1 - игрок совершил действие и продолжает ход (кости еще остались)

        Кости добавляются (возвращает True) если:
        2 - игрок совершил действие и продолжает ход, но кости закончились
        -1 - игрок не может совешить действие т.к. выпавшие кости не приносят
          очков. Ход заканчивается
        -2 - игрок совершил действие и заканчивает ход
        """
        screen = Game.screen
        player = self.player

        # Установка рандомных значений для имеющихся костей и анимация броска
        screen.anim_diceroll(len(Game.dices))
        for i in range(len(Game.dices)):
            Game.dices[i] = random.randint(1, 6)
        temp_dices = Game.dices[:]  # сохрание костей (нужно далее)

        # Выводим на экран выпавшие кости
        screen.display_dices(Game.dices)

        # Проверка, есть ли хоть какие-то кости, приносящие очки.
        # Если нет, ход заканчивается автоматически, и игрок теряет очки.
        if self.check_combos() is False:
            screen.display_msg("07_nocombos")
            player.clear_scoreturn()
            return -1

        # Цикл взятия косей игроком
        while True:
            pick_score = 0
            # ИИ/Человек берет в "руку" какие-то выпавшие кости
            hand = player.get_dicechoose()
            screen.effect_hldices(hand)  # выделение выбранных костей
            # Происходят проверки на комбинации в руке, приносящие очки (поря-
            # док имеет значение!). Кости, приносящие очки, удаляются из руки
            # и из основного списка костей класса Game (но возвращаются из
            # temp_dices, в случае повторного выбора).

            if self.check_combosrange(hand):
                if 6 in hand:
                    pick_score += 1500
                    hand.clear()
                    Game.dices.clear()
                else:
                    pick_score += 750
                    for i in range(1, 6):
                        hand.remove(i)
                        Game.dices.remove(i)

            if self.check_combosrow(hand):
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
                            Game.dices.remove(dice)

            if self.check_combossingle(hand):
                for dice in hand[:]:

                    if dice == 1:
                        pick_score += 100
                        hand.remove(dice)
                        Game.dices.remove(dice)

                    elif dice == 5:
                        pick_score += 50
                        hand.remove(dice)
                        Game.dices.remove(dice)

            # Выводится сообщение, если никакие кости не принесли очков.
            # Цикл тут же начинается сначала.
            if pick_score == 0:
                # Выделение "плохих" костей
                screen.effect_hldices(hand, cp_id=4)
                screen.display_msg("10_1_badallpick", player.name)
                screen.effect_hldices()
                continue
            # Выводится сообщение, если в руке остались кости, которые не при-
            # несли очки (но они используются далее в игре).
            elif len(hand) > 0:
                screen.effect_hldices(hand, cp_id=4)
                screen.display_msg("10_0_badpick")

            # Добавление очков за выбранные кости
            player.add_scorepick(pick_score)
            # Игрок решает как посутпить дальше
            action_choice = player.get_nextaction()
            # Снимается выделение с выбранных костей
            screen.effect_hldices()

            # При отмене выбора, цикл продолжается
            if action_choice == data.KEYCODES["TURN_CANCEL"]:
                Game.dices = temp_dices[:]  # возвращение удаленных костей
                player.clear_scorepick()
            # Если игрок согласен использовать выбранные кости,
            # то они скрываются.
            else:
                removed_dices = tools.exclude_array(temp_dices, Game.dices)
                screen.effect_hldices(removed_dices, cp_id=6)
                break

        # После цикла очки за кости добавляются к очкам за ход.
        # На экран выводится информация о набранных очках.
        player.add_scoreturn()
        screen.display_msg("09_2_scrpick", player.name, pick_score)

        # Если игрок хочет закончить ход и сохнанить набранные очки:
        if action_choice == data.KEYCODES["TURN_END"]:
            # Убираем оставшиеся кости. Новый игрок - чистый стол
            screen.effect_hldices(screen.scr_dices, cp_id=6)
            player.add_scoretotal()
            screen.display_msg("09_1_scrtotl", player.name,
                               player.score_total)
            self.check_win()
            return -2

        elif action_choice == data.KEYCODES["TURN_CONTINUE"]:
            # Если ход продолжается, происходи проверка, остались ли еще кости
            if len(Game.dices) == 0:
                return 2
            else:
                return 1


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
            screen.display_msg("08_0_getpick", wait=False)
            inp = screen.input_str()
            # Проверка, есть ли все выбранные кости среди выпавших костей
            if (inp.isdigit()
                    and all(inp.count(d) <= dices.count(int(d)) for d in inp)):
                return [int(d) for d in inp]
            else:
                screen.display_msg("08_1_errpick",
                                   delay=data.TIMINGS["DELAY-ERR"])

    def get_nextaction(self):
        """Узнает, готов ли игрок рискнуть продолжить ход."""
        screen = Player.screen
        while True:
            screen.display_msg("13_0_actchoose", wait=False, speedup=2)
            inp = screen.input_str()

            if inp in data.KEYCODES.values():
                return inp
            else:
                screen.display_msg("13_1_badans",
                                   delay=data.TIMINGS["DELAY-ERR"])


#  8888888b.    .d88888b.   888888b.     .d88888b.  88888888888
#  888   Y88b  d88P" "Y88b  888  "88b   d88P" "Y88b     888
#  888    888  888     888  888  .88P   888     888     888
#  888   d88P  888     888  8888888K.   888     888     888
#  8888888P"   888     888  888  "Y88b  888     888     888
#  888 T88b    888     888  888    888  888     888     888
#  888  T88b   Y88b. .d88P  888   d88P  Y88b. .d88P     888
#  888   T88b   "Y88888P"   8888888P"    "Y88888P"      888

class AI_meta(Player):
    """Представляет базовый класс ИИ.

    take_*combo* -- взятие роботом определенной комбинации костей

    """

    __type__ = "Robot"

    def __init__(self):
        Player._init_()
        self.claw = []

    def take_range(self, dices):
        """Забирает в claw наибольший диапазон костей."""
        claw = self.claw
        if 6 in dices:
            claw.extend(range(1, 7))
            dices.clear()
        else:
            for d in range(1, 6):
                claw.append(d)
                dices.remove(d)

    def take_row(self, dices):
        """Забирает в claw ряд(ы) костей."""
        claw = self.claw
        for d in dices:
            if dices.count(d) >= 3:
                claw.append(d)
                dices.remove(d)

    def take_single(self, dices, amount=4):
        """Забирает в claw единичные кости, где amount - количество."""
        claw = self.claw
        # По умолчанию amount = 4, т.к. это максимальное число единичных косей
        for i in (1, 5):  # Сначала забираются кости со значением "1"
            for d in dices[:]:
                if amount == 0:
                    break
                if d == i:
                    claw.append(d)
                    dices.remove(d)
                    amount -= 1

    def rowcombo_dice(self, dices):
        """Возвращает значения костей, образующих комбо row"""
        out = []
        for d in dices:
            if dices.count(d) >= 3 and d not in out:
                out.append(d)
        return out


class AI_easy(AI_meta):
    """Представляет глупый ИИ."""

    def get_dicechoose(self):
        gm = Player.gm
        dices = gm.dices[:]
        self.claw = []
        ones, fives = dices.count(1), dices.count(5)

        if gm.check_combosrange(dices):
            if tools.randchance(37):
                self.take_range(dices)
                if ones + fives > 2 and tools.randchance(40):
                    self.take_single(dices)
            elif ones + fives > 2 and tools.randchance(65):
                self.take_single(dices)
            else:
                self.take_single(random.choice([1, 2]))

        elif gm.check_combosrow(dices):
            if len(self.rowcombo_dice(dices)) > 1 and tools.randchance(90):
                self.take_row(dices)
            else:
                row_dice = self.rowcombo_dice(dices)[0]
                if ((row_dice == 1 and fives != 0 and tools.randchance(36))
                   or (row_dice == 5 and ones != 0 and tools.randchance(40))):
                    self.take_single()
                elif row_dice not in (1, 5):
                    if ones + fives > 0 and tools.randchance(40):
                        self.take_single()
                        self.take_row()
                    else:
                        self.take_row()
                else:
                    self.take_row()

        if gm.check_combossingle(dices) and len(self.claw) != 0:
            if len(dices) == ones + fives:
                if tools.randchance(84):
                    self.take_single(dices)
                else:
                    self.take_single(dices,
                                     random.choice(range(1, len(dices))))
            elif ones + fives > 2 and tools.randchance(50):
                self.take_single(dices, 2)
            elif tools.randchance(50):
                self.take_single(dices, 1)

        if len(self.claw) == 0:
            if len(dices) == ones + fives:
                if len(dices) == 1 or tools.randchance(84):
                    self.take_single(dices)
                else:
                    self.take_single(dices,
                                     random.choice(range(1, len(dices))))
            elif ones + fives == 4 and tools.randchance(20):
                self.take_single(dices, 3)
            elif ones + fives > 2 and tools.randchance(39):
                self.take_single(dices, 2)
            else:
                self.take_single(dices, 1)

        return self.claw


class AI_hard(AI_meta):
    """Представляет сложиый ИИ."""

    def get_dicechoose(self):
        """Возвращает выбранные ИИ кости."""
        gm = Player.gm
        dices = gm.dices[:]
        self.claw = []
        singles = dices.count(1) + dices.count(5)

        # Если есть диапазон костей, то забираем его
        if gm.check_combosrange(dices):
            self.take_range(dices)
            # Если остались еще кости, то забираем их
            if gm.check_combossingle(dices):
                self.take_single(dices)

        # Если есть ряд костей, то забрать весь (все) ряд(ы)
        elif gm.check_combosrow(dices):
            self.take_row(dices)
            # Если еще остались единичные кости
            if gm.check_combossingle(dices):
                # Забирам их при условии, что всего косей меньше трех
                # (+ шанс 60%) или с шансом 25%.
                if (len(dices) < 3 and tools.randchance(60)
                        or tools.randchance(25)):
                    self.take_single(dices)

        # Забирам все единичные кости, если остались только они
        elif singles == len(dices):
            self.take_single(dices)

        # Если костей больше трех, то забираем одну с шансом 75% или все
        elif len(dices) > 3:
            if tools.randchance(75) or singles == 1:
                self.take_single(dices, 1)
            else:
                self.take_single(dices)

        # Если кости три или меньше, то забираем все с шансом 75% или одну
        elif len(dices) <= 3:
            if singles > 1 and tools.randchance(75):
                self.take_single(dices)
            else:
                self.take_single(dices, 1)

        delay = (random.uniform(0.7, 1.5) + len(dices) / 10) * -1
        Player.screen.display_msg("11_robthink", delay=delay)
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

        choice = tools.randchance(chance_to_continue)
        if choice is True:
            Player.screen.display_msg("12_0_robturnT")
            return data.KEYCODES["TURN_CONTINUE"]
        else:
            Player.screen.display_msg("12_1_robturnF")
            return data.KEYCODES["TURN_END"]
