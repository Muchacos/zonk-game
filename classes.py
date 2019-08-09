import random
import tools


class Game:
    '''Представляет основной функционал игры.

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
    printer -- экземпляр класса Printer, использующийся для вывода/получения
               сообщений/информации

    Методы:
    set_settings -- делает то, что указано в названии
    check_win -- проверяет, выйграл ли игрок
    check_action -- проверяет, может ли игрок совершить действие в свой ход
    (check_combosrow,
    check_combosrange,
    check_combossingle) -- проверка разных комбинаций
    add_dices -- добавляет кости
    action -- основной функционал хода

    '''

    game_flag = True
    printer = None
    dices = [1]*6

    def __init__(self):
        pass

    def set_settings(self, player, second_player, high_bar, printer):
        '''Принимает список с настройками и Printer игры, устанавливая их
        в поля экземпляров.'''
        self.player = player
        self.second_player = second_player
        self.high_bar = high_bar
        Game.printer = printer
        Game.printer.print_robothello()
        Game.printer.print_gamestart()

    def switch_player(self):
        self.player, self.second_player = self.second_player, self.player
        Game.printer.print_turnstart()

    def check_win(self):
        '''Сравнивая очки игрока с очками для победы, опускает game_flag в
        случае выйгрыша'''
        if self.player.score_total >= self.high_bar:
            Game.game_flag = False
            Game.printer.print_won()

    def check_combosrow(self, dices):
        '''Возвращает True, если среди костей есть >= 3-х костей с
        одинаковыми значениями'''
        return any(dices.count(d) >= 3 for d in dices)

    def check_combosrange(self, dices):
        '''Возвращает True, если среди костей есть все кости от 1 до 5'''
        return all(d in dices for d in range(1, 6))

    def check_combossingle(self, dices):
        '''Возвращает True, если среди костей есть хотя бы одна кость
        со значением 1 или 5'''
        return any(d in dices for d in (1, 5))

    def check_action(self):
        '''Возвращает True, если среди костей есть хотя бы одна комбинация
        приносящая очки'''
        d = Game.dices
        return any((self.check_combosrow(d), self.check_combosrange(d),
                   self.check_combossingle(d)))

    def add_dices(self):
        '''Добавляет недостающие кости (до 6 штук)'''
        Game.dices.extend([1]*(6 - len(Game.dices)))

    def action(self):
        '''Совершение действия в ход. Возвращает исход действия в числе:

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

        '''

        printer = Game.printer
        player = self.player

        # Проверка не закончена ли игра
        if Game.game_flag is False:
            printer.print_gameend()
            return 0

        # Установка рандомных значений для имеющихся костей
        for i in range(len(Game.dices)):
            Game.dices[i] = random.randint(1, 6)

        # Выводим на экран выпавшие кости
        printer.print_dices(Game.dices)

        # Проверк может ли игрок совершить действие. Если нет, ход заканчива-
        # ется автоматически, и игрок теряет очки.
        if self.check_action() is False:
            printer.print_nodices()
            self.player.clear_scoreturn()
            return -1

        # Инициализация текущих очков за текущее действие
        action_score = 0

        # Цикл, повторяющийся до тех пор, пока игрок не совершит дейстие,
        # приносящее очки.
        while action_score == 0:
            # ИИ/Человек берет в 'руку' какие-то выпавшие кости
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
                        score *= 2**(row_len - 3)
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
                printer.print_nopoints(hand)

        # В конце цикла набранные очки за действие добавляются к очкам за ход.
        # На экран выводится информация о набранных очках.
        player.add_scoreturn(action_score)
        printer.print_scoreearned(action_score)
        printer.print_scoreturn()

        # Проверка, хочет ли игрок закончить ход и сохранить набранные очки
        if player.get_nextaction() is False:
            self.player.add_scoretotal()
            printer.print_scoretotal()
            self.check_win()
            return -2
        # Если ход продолжается, происходи проверка, остались ли еще кости
        elif len(Game.dices) == 0:
            return 2
        else:
            return 1


class Player:
    ''' Представляет родительский класс игрока.

        Поля класса:
        game_mode -- основной функционал игры
        printer -- инструмент для ввода/вывода данных

        Поля экземпляра:
        name -- имя игрока
        score_total -- итоговое число очков
        score_turn -- число очков за ход

    '''

    game_mode = None
    printer = None

    def __init__(self, game_mode, printer, name):
        Player.game_mode = game_mode
        Player.printer = printer
        self.name = name
        self.score_total = 0
        self.score_turn = 0

    def add_scoretotal(self):
        '''Добавляет score_turn к score_total.'''
        self.score_total += self.score_turn
        self.score_turn = 0

    def add_scoreturn(self, score):
        '''Увеличивает score_turn на значение score.'''
        self.score_turn += score

    def clear_scoreturn(self):
        '''Отчищает score_turn (очки за ход)'''
        self.score_turn = 0


class Human(Player):
    """Представляет игрока по ту сторону экрана.

    """

    def get_dicechoose(self):
        '''Возвращает выбранные игроком кости, если те существуют'''
        dices = Player.game_mode.dices
        while True:
            inp = input('> ')
            # Проверка, есть ли все выбранные кости среди выпавших костей
            if (inp.isdigit() and
               all(inp.count(d) <= dices.count(int(d)) for d in inp)):
                return [int(d) for d in inp]
            else:
                Player.printer.print_cannotpick()

    def get_nextaction(self):
        '''Узнает, готов ли игрок рискнуть продолжить ход (y/n)'''
        print('\nContunue?')
        while True:
            inp = input('> ')

            if inp == 'y':
                return True
            elif inp == 'n':
                return False
            else:
                print('Wrong answer')


class Robot(Player):
    """Представляет ИИ.

    """

    def take_range(self, dices, claw):
        '''Забирает в claw наибольший диапазон костей'''
        if 6 in dices:
            claw.extend(range(1, 7))
            dices.clear()
        else:
            for d in range(1, 6):
                claw.append(d)
                dices.remove(d)

    def take_row(self, dices, claw):
        '''Забирает в claw наибольший(ые) ряд(ы) костей'''
        gm = Player.game_mode
        for d in gm.dices:
            if gm.dices.count(d) >= 3:
                claw.append(d)
                dices.remove(d)

    def take_single(self, dices, claw, amount=4):
        '''Забирает в claw единичные кости. amount - количество (0 = все)'''
        # По умолчанию amount = 4, т.к. это максимальное число единичных косей
        for i in (1, 5):  # Сначала забираются кости со значением '1'
            for d in dices[:]:
                if amount == 0:
                    break
                if d == i:
                    claw.append(d)
                    dices.remove(d)
                    amount -= 1

    def get_dicechoose(self):
        '''Возвращает выбранные ИИ кости'''
        gm = Player.game_mode
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

        # ОТЛАДКА непредвиденного случая
        else:
            print('!НЕПРЕДВИДЕННЫЙ СЛУЧАЙ СБОРА КОСТЕЙ!')
            self.take_single(dices, claw)

        Player.printer.print_robotpick(claw)
        return claw

    def get_nextaction(self):
        '''Узнает, готов ли робот рискнуть продолжить ход'''

        # Возвращает шанс продолжить ход по графику y = -2.5(x-200)^1/2 + 100
        def chance_curve(x):
            if x < 200:
                y = 100
            elif x > 1800:
                y = 0
            else:
                y = round(-2.5*(x-200)**(1/2)+100)
            return y

        dices = Player.game_mode.dices
        chance_to_continue = chance_curve(self.score_turn)
        # После вычисления шанса по формуле, рассматриваются нюансы, увеличива-
        # ющие или уменьшающие риск потерять накопленные очки. Они увеличивают,
        # либо уменьшают шанс продолжить ход:

        # Если текущее кол-во очнов больше кол-ва очков для победы, то
        # продолжать ход и рисковать не имеет смысла.
        if self.score_total + self.score_turn >= Player.game_mode.high_bar:
            chance_to_continue = 0
        elif len(dices) == 0:
            chance_to_continue += 90
        elif len(dices) == 5:
            chance_to_continue += 30
        elif len(dices) < 3:
            chance_to_continue -= 30

        choice = tools.randchance(chance_to_continue)
        Player.printer.print_robotactionchoice(choice)
        print('ШАНС:', chance_to_continue)  # ОТЛАДКА
        return choice


class Printer:
    '''Представляет инструмент для вывода сообщений и получения
        пользовательского ввода.

    Поля экземпляра:
    game_mode -- экземпляр класса Game с основным функционалам игры

    Методы класса:
    input_*something* -- возвращает пользовательский ввод в объекте *something*
    print_*something* -- выводит на экран различные сообщения

    '''

    def __init__(self, game_mode):
        self.game_mode = game_mode

    def input_player(self):
        '''Создает и возвращает игрока'''
        print('Welcome to the game! What is your name?')
        player = Human(self.game_mode, self, name=input('> '))
        print('Ok... let me write it down... yep.')
        return player

    def input_highbar(self):
        '''Получет и выводит число очков для победы'''
        high_bar = 0
        print('Now, choose a maximum fo points.')
        # Проверка на целч. ввод данных
        while True:
            try:
                high_bar = int(input('> '))
            except ValueError:
                print('We need a int')
            else:
                # Проверка, в нужном ли диапазоне очки для победы
                if high_bar < 0 or high_bar > 39999:
                    print('Bad idea, do it again')
                    continue
                else:
                    break
        return high_bar

    def print_gamestart(self):
        print('Great! We can start')

    def print_turnstart(self):
        gm = self.game_mode
        print('------------------------------')
        print('%s\'s turn!' % gm.player.name)

    def print_dices(self, dices):
        for i in range(len(dices)):
            print('[%d] ' % dices[i], end=' ')
        print('\n')

    def print_scoreturn(self):
        player = self.game_mode.player
        print('%s\'s score: %d' % (player.name, player.score_turn))

    def print_scoretotal(self):
        player = self.game_mode.player
        print('%s\'s total score: %d' % (player.name, player.score_total))

    def print_scoreearned(self, score):
        player_name = self.game_mode.player.name
        print('%s was earned %d points!' % (player_name, score))

    def print_nodices(self):
        print('No dices to pick!')

    def print_nopoints(self, dices):
        print('These dices do not give you points:', end=' ')
        for d in dices:
            print('[%s]' % d, end=' ')
        print('\n')

    def print_cannotpick(self):
        print('You cannot pick these dices!')

    def print_robothello(self):
        robot_name = self.game_mode.second_player.name
        print('Your enemy is %s' % robot_name)

    def print_robotpick(self, pick):
        print('Robot was picked: ', end='')
        for d in pick:
            print('[%s]' % d, end=' ')
        print('\n')

    def print_robotactionchoice(self, choice):
        print('Robot choosed to ', end='')
        if choice is True:
            print('continue his turn')
        else:
            print('end his turn')

    def print_won(self):
        player_name = self.game_mode.player.name
        print('CONGRATS, %s!. YOU WON!' % player_name)

    def print_gameend(self):
        print('Game was alrady end')
