"""Тут содержатся все классы, составляющие игровую логику."""
import random
import tools


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
    dices -- список, содержащий от 1 до 6 игральных костей (их целочисленные
             значения)

    Поля экземпляров:
    player -- основной игрок (экземпляр класса Player)
    high_bar -- цел. значение очков необходимых для победы
    screen -- экземпляр класса Screen, представляющий экран игры

    Методы:
    check_win -- проверяет, выйграл ли игрок
    check_combos -- проверяет, есть ли хоть одно комбо среди костей
    (check_combosrow,
    check_combosrange,
    check_combossingle) -- проверка разных комбинаций
    add_dices -- добавляет кости
    action -- основной функционал действия

    """

    game_flag = True
    screen = None
    dices = [1]*6

    def __init__(self, screen):
        """Инициализация со вступлением."""
        Game.screen = screen
        screen.display_msg("01_hello", 2)
        screen.display_msg("02_name")
        while True:
            name = screen.input_str()
            if len(name) == 0:
                screen.display_msg("22_dontans", 2)
                name = "Человек"
                break
            elif len(name) <= screen.ZONE_SCORE[5] // 2 - 1:
                screen.display_msg("03_writing", 1)
                break
            else:
                screen.display_msg("25_badname")
        self.player = Human(self, screen, name)
        self.second_player = Robot(self, screen, "zX01")
        screen.display_msg("13_enemy", 2, self.second_player.name)
        screen.display_players(self)
        screen.display_msg("04_00_maxp", 0, self.player.name)
        while True:
            hbar = screen.input_str()
            if hbar.isdigit() and int(hbar) > 100 and int(hbar) < 30000:
                self.high_bar = int(hbar)
                break
            else:
                screen.display_msg("19_badans", 1)
                screen.display_msg("04_00_maxp", 0, self.player.name)
        screen.add_high_bar(hbar)
        screen.display_msg("05_start", 2)

    def switch_player(self):
        """Меняет игроков местами."""
        self.player, self.second_player = self.second_player, self.player
        Game.screen.display_msg("06_whoturn", 1.5, self.player.name)

    def check_win(self):
        """Опускает game_flag в случае выйгрыша текущего игрока."""
        if self.player.score_total >= self.high_bar:
            Game.game_flag = False
            Game.screen.display_msg("16_won", 3, self.player.name)

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
        return any((self.check_combosrow(d), self.check_combosrange(d),
                   self.check_combossingle(d)))

    def add_dices(self):
        """Добавляет недостающие кости (до 6 штук)."""
        Game.dices.extend([1]*(6 - len(Game.dices)))

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

        # Установка рандомных значений для имеющихся костей
        for i in range(len(Game.dices)):
            Game.dices[i] = random.randint(1, 6)

        # Выводим на экран выпавшие кости
        screen.display_dices(Game.dices)

        # Проверк может ли игрок совершить действие. Если нет, ход заканчива-
        # ется автоматически, и игрок теряет очки.
        if self.check_combos() is False:
            screen.display_msg("10_nodice", 3.5)
            player.clear_scoreturn()
            screen.display_score(player, "turn")
            return -1
        elif player.__type__ == "Human":
            screen.display_msg("20_dicechoose")

        # Инициализация текущих очков за текущее действие
        action_score = 0

        # Цикл, повторяющийся до тех пор, пока игрок не совершит дейстие,
        # приносящее очки.
        while action_score == 0:
            # ИИ/Человек берет в "руку" какие-то выпавшие кости
            hand = player.get_dicechoose()
            # Происходят проверки на комбинации в руке, приносящие очки (поря-
            # док имеет значение!). Кости, приносящие очки, удаляются из руки
            # и из основного списка костей класса Game.

            if self.check_combosrange(hand):
                if 6 in hand:
                    action_score += 1500
                    hand.clear()
                    Game.dices.clear()
                else:
                    action_score += 750
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
                            score += dice*100
                        score *= (row_len - 2)
                        action_score += score

                        for i in range(row_len):
                            hand.remove(dice)
                            Game.dices.remove(dice)

            if self.check_combossingle(hand):
                for dice in hand[:]:

                    if dice == 1:
                        action_score += 100
                        hand.remove(dice)
                        Game.dices.remove(dice)

                    elif dice == 5:
                        action_score += 50
                        hand.remove(dice)
                        Game.dices.remove(dice)

            # Выводится сообщение, если в руке остались кости, которые не при-
            # несли очки. Они не удаляются и используются далее в игре.
            if len(hand) > 0:
                screen.display_msg("11_baddice", 3, hand)

        # В конце цикла набранные очки за действие добавляются к очкам за ход.
        # На экран выводится информация о набранных очках.
        player.add_scoreturn(action_score)
        screen.display_score(player, "turn")
        screen.display_msg("09_scoreearn", 1.7, player.name, action_score)

        # Проверка, хочет ли игрок закончить ход и сохранить набранные очки
        if player.get_nextaction() is False:
            player.add_scoretotal()
            screen.display_score(player, "total")
            screen.display_score(player, "turn")
            screen.display_msg("08_scoretot", 2, player.name,
                               player.score_total)
            self.check_win()
            return -2
        # Если ход продолжается, происходи проверка, остались ли еще кости
        elif len(Game.dices) == 0:
            return 2
        else:
            return 1


class Player:
    """Представляет родительский класс игрока.

    Поля класса:
    gm -- основной функционал игры
    screen -- экран с полем для ввода данных

    Поля экземпляра:
    name -- имя игрока
    score_total -- итоговое число очков
    score_turn -- число очков за ход

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

    def add_scoretotal(self):
        """Добавляет score_turn к score_total."""
        self.score_total += self.score_turn
        self.score_turn = 0

    def add_scoreturn(self, score):
        """Увеличивает score_turn на значение score."""
        self.score_turn += score

    def clear_scoreturn(self):
        """Отчищает score_turn (очки за ход)."""
        self.score_turn = 0


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
            inp = screen.input_str()
            # Проверка, есть ли все выбранные кости среди выпавших костей
            if (inp.isdigit() and
               all(inp.count(d) <= dices.count(int(d)) for d in inp)):
                return [int(d) for d in inp]
            else:
                screen.display_msg("12_badpick", 1)
                screen.display_msg("20_dicechoose")

    def get_nextaction(self):
        """Узнает, готов ли игрок рискнуть продолжить ход (1/0)."""
        screen = Player.screen
        screen.display_msg("18_continue")
        while True:
            inp = screen.input_str()

            if inp == "1":  # ДОПИЛИТЬ
                return True
            elif inp == "0":
                return False
            else:
                screen.display_msg("19_badans", 1)
                screen.display_msg("18_continue")


class Robot(Player):
    """Представляет ИИ.

    Методы:
    take_*dicecombo* -- взятие роботом определенной комбинации костей
    get_dicechoose -- интеллектуальный выбор роботом выпавших костей
    get_nextaction -- интеллектуальный выбор роботом прололжать ход или нет

    """

    __type__ = "Robot"

    def take_range(self, dices, claw):
        """Забирает в claw наибольший диапазон костей."""
        if 6 in dices:
            claw.extend(range(1, 7))
            dices.clear()
        else:
            for d in range(1, 6):
                claw.append(d)
                dices.remove(d)

    def take_row(self, dices, claw):
        """Забирает в claw ряд(ы) костей."""
        gm = Player.gm
        for d in gm.dices:
            if gm.dices.count(d) >= 3:
                claw.append(d)
                dices.remove(d)

    def take_single(self, dices, claw, amount=4):
        """Забирает в claw единичные кости, где amount - количество."""
        # По умолчанию amount = 4, т.к. это максимальное число единичных косей
        for i in (1, 5):  # Сначала забираются кости со значением "1"
            for d in dices[:]:
                if amount == 0:
                    break
                if d == i:
                    claw.append(d)
                    dices.remove(d)
                    amount -= 1

    def get_dicechoose(self):
        """Возвращает выбранные ИИ кости."""
        gm = Player.gm
        dices = gm.dices[:]
        claw = []
        singles = dices.count(1) + dices.count(5)  # кол-во единичных костей

        # Если есть диапазон костей, то забираем его
        if gm.check_combosrange(dices):
            self.take_range(dices, claw)
            # Если остались еще кости, то забираем их
            if gm.check_combossingle(dices):
                self.take_single(dices, claw)

        # Если есть ряд костей, то забрать весь (все) ряд(ы)
        elif gm.check_combosrow(dices):
            self.take_row(dices, claw)
            # Если еще остались единичные кости
            if gm.check_combossingle(dices):
                # Забирам их при условии, что всего косей меньше трех
                # (+ шанс 60%) или с шансом 25%.
                if (len(dices) < 3 and tools.randchance(60) or
                   tools.randchance(25)):
                    self.take_single(dices, claw)

        # Забирам все единичные кости, если остались только они
        elif singles == len(dices):
            self.take_single(dices, claw)

        # Если костей больше трех, то забираем одну с шансом 75% или все
        elif len(dices) > 3:
            if tools.randchance(75) or singles == 1:
                self.take_single(dices, claw, 1)
            else:
                self.take_single(dices, claw)

        # Если кости три или меньше, то забираем все с шансом 75% или одну
        elif len(dices) <= 3:
            if singles > 1 and tools.randchance(75):
                self.take_single(dices, claw)
            else:
                self.take_single(dices, claw, 1)

        delay = random.randint(1, 3) * -1
        Player.screen.display_msg("21_robthink", delay)
        Player.screen.display_msg("14_robpick", 2, claw)
        return claw

    def get_nextaction(self):
        """Узнает, готов ли робот рискнуть продолжить ход."""
        # Возвращает шанс продолжить ход по графику y = -2.5(x-200)^1/2 + 100
        def chance_curve(x):
            if x < 200:
                y = 100
            elif x > 1800:
                y = 0
            else:
                y = round(-2.5*(x-200)**(1/2)+100)
            return y

        dices = Player.gm.dices
        chance_to_continue = chance_curve(self.score_turn)
        # После вычисления шанса по формуле, рассматриваются нюансы, увеличива-
        # ющие или уменьшающие риск потерять накопленные очки. Они увеличивают,
        # либо уменьшают шанс продолжить ход:

        # Если текущее кол-во очнов больше кол-ва очков для победы, то
        # продолжать ход и рисковать не имеет смысла.
        if self.score_total + self.score_turn >= Player.gm.high_bar:
            chance_to_continue = 0
        elif len(dices) == 0:
            chance_to_continue += 90
        elif len(dices) == 5:
            chance_to_continue += 30
        elif len(dices) < 3:
            chance_to_continue -= 30

        choice = tools.randchance(chance_to_continue)
        if choice is True:
            Player.screen.display_msg("15_00_robturnT", 2)
        else:
            Player.screen.display_msg("15_01_robrurnF", 2)
        return choice
