"""Этот модуль отвечает за графику игры."""
import curses
import os
import random
import time
from curses import textpad

import data

#   .d8888b.    .d8888b.   8888888b.   8888888888  8888888888  888b    888
#  d88P  Y88b  d88P  Y88b  888   Y88b  888         888         8888b   888
#  Y88b.       888    888  888    888  888         888         88888b  888
#   "Y888b.    888         888   d88P  8888888     8888888     888Y88b 888
#      "Y88b.  888         8888888P"   888         888         888 Y88b888
#        "888  888    888  888 T88b    888         888         888  Y88888
#  Y88b  d88P  Y88b  d88P  888  T88b   888         888         888   Y8888
#   "Y8888P"    "Y8888P"   888   T88b  8888888888  8888888888  888    Y888


class Screen:
    """Представляет игровой экран, отображающий всю графику.

    Поля:
    stdscr -- стандартный экран игры
    scr_dices -- кости, находящийся на экране. Индекс означает позицию по
                 DICES_POSITIONS. Значение "0" означает пустоту, т.е. при
                 отображении "нулевой" кости, ее позиция отчиститься

    Константы:
    SH, SW -- досл. screen hight и screen width
    ZONE_*NAME* -- координаты различных зон экрана:
                   [0] и [1] - y и x левого верхнего угла;
                   [2] и [3] - y и x правого нижнего угла;
                   [4] и [5] - длина зоны по y и x
    DICES_POSITIONS -- Позиции костей (верхний левый угол) в зоне для костей

    Методы:
    Тип input_:
        Функции, связанные с пользовательским вводом
        input_str -- возвращает введенную пользователем строку
        input_delayinterrupt -- создает задержку, которую можно прервать
                                нажатием любой кнопки.
    Тип display_:
        Функции для частого отображения различных данных на экране
        display_msg -- посимвольно выводит на экран сообщения из реестра
        display_dice -- выводит на экран одну кость с параметрами
        display_dices -- выводит на экран игральные кости
        display_score -- выводит/убирает с экрана очки игрока
    Tип anim_:
        Функции, проигрывающие анимации
        animbase_savezone -- возвращает массив с данными по каждому символу
                             в заданной зоне. dis
        anim_ending -- анимация сдвига всего экрана вверх
        anim_diceroll -- анимация броска костей anim
        anim_playerhl -- анимация подсветки текущего игрока
        anim_arrowflick -- анимация мигающей стрелки
        anim_percharword -- анимация посимвольного вывода слова
    Тип effect_:
        Функции, отвечающие за проигрывание эффектов
        effect_hldices -- отвечает за выделение отображаемых костей
        effect_hlplayers -- отвечает за выделеине имен игроков
    Тип add_:
        Функции, добавляющие на экран неизменяемые данные. Обычно используются
        единожды в начале игры.
        add_players -- добавляет на экран имена игроков
        add_high_bar -- добавляет на экран очки, необходимые для победы

    clear_zone -- отчищает указанную игровую зону
    init_pairs -- инициализация цветовых пар (используемых цветов)

    """

    SH, SW = 30, 70
    ZONE_MSG = (5, 7, 7, 61, 3, 55)
    ZONE_DICES = (12, 7, 20, 35, 9, 29)
    ZONE_SCORE = (12, 42, 20, 61, 9, 20)
    ZONE_INPUT = (25, 7, 25, 35, 1, 29)

    DICES_POSITIONS = {
        0: (ZONE_DICES[0], ZONE_DICES[1] + 2),
        1: (ZONE_DICES[0], ZONE_DICES[1] + 11),
        2: (ZONE_DICES[0], ZONE_DICES[1] + 20),
        3: (ZONE_DICES[0] + 4, ZONE_DICES[1] + 2),
        4: (ZONE_DICES[0] + 4, ZONE_DICES[1] + 11),
        5: (ZONE_DICES[0] + 4, ZONE_DICES[1] + 20)
    }

    def __init__(self):
        """Иниц. stdscr, установка параметров теримнала и прорисовка UI."""
        SH, SW = Screen.SH, Screen.SW
        ZONE_DICES = Screen.ZONE_DICES
        ZONE_INPUT = Screen.ZONE_INPUT
        ZONE_MSG = Screen.ZONE_MSG
        ZONE_SCORE = Screen.ZONE_SCORE
        self.scr_dices = [0] * 6  # индекс - позиция, значение - значение :)
        self.stdscr = curses.initscr()
        stdscr = self.stdscr

        # Настройка окна консоли
        os.system("mode con: cols={0} lines={1}".format(SW, SH))
        stdscr.resize(SH, SW)
        curses.start_color()
        curses.use_default_colors()
        self.init_pairs()
        curses.noecho()
        stdscr.keypad(True)
        curses.curs_set(0)

        # Включение ярко-белого цвета для отрисовки
        stdscr.attron(curses.color_pair(1))
        # Заполнение точками игровое окно
        self.clear_zone((0, 0, SH - 2, SW - 2, SH, SW), "∙", 2)

        # Отрисовка игровых зон
        for zone, txt in ([ZONE_DICES, "┤dices├"], [ZONE_SCORE, "┤score├"],
                          [ZONE_INPUT, "┤input├"], [ZONE_MSG, "┤msg├"]):
            uy, lx = zone[0] - 1, zone[1] - 1
            ly, rx = zone[2] + 1, zone[3] + 1
            textpad.rectangle(stdscr, uy, lx, ly, rx)
            stdscr.addstr(uy, lx, "∙")
            stdscr.addstr(uy, rx, "∙")
            stdscr.addstr(ly, lx, "∙")
            stdscr.addstr(ly, rx, "∙")
            stdscr.addstr(uy, rx - len(txt) - 2, txt)
            self.clear_zone(zone)

        # Добавление внутренностей окна Score
        scoretxt1 = " Tot _____    _____ "
        scoretxt2 = " Tur _____    _____ "
        scoretxt3 = "     +        +     "
        scoretxt4 = " Win     _____      "
        stdscr.addstr(ZONE_SCORE[0] + 3, ZONE_SCORE[1], scoretxt1)
        stdscr.addstr(ZONE_SCORE[0] + 5, ZONE_SCORE[1], scoretxt2)
        stdscr.addstr(ZONE_SCORE[0] + 6, ZONE_SCORE[1], scoretxt3)
        stdscr.addstr(ZONE_SCORE[0] + 7, ZONE_SCORE[1], scoretxt4)

        # Добавление стрелки на край окна для ввода
        stdscr.addstr(ZONE_INPUT[0], ZONE_INPUT[1] - 1, ">")

        stdscr.refresh()

    def __del__(self):
        """Завершение работы экрана и возврат стд. параметров терминала."""
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
        os.system("mode con: cols=80 lines=30")

    def init_pairs(self):
        """Установка цветовых пар (используемых цветов)."""
        curses.init_pair(1, 15, 0)  # Ярко-белый
        curses.init_pair(2, 26, 0)  # Светло-синий
        curses.init_pair(3, 39, 0)  # Ярко-голубой
        curses.init_pair(4, 12, 0)  # Красный
        curses.init_pair(5, 0, 15)  # Ченрый на белом
        curses.init_pair(6, 0, 0)   # Черный

#
#        d8b                                888
#        Y8P                                888
#                                           888
#        888  88888b.   88888b.   888  888  888888
#        888  888 "88b  888 "88b  888  888  888
#        888  888  888  888  888  888  888  888
#        888  888  888  888 d88P  Y88b 888  Y88b.
#        888  888  888  88888P"    "Y88888   "Y888  88888888
#                       888
#                       888
#                       888

    def input_str(self):
        """Получает пользовательский ввод в зоне для ввода и возвращает его."""
        stdscr = self.stdscr
        ZONE_INPUT = Screen.ZONE_INPUT
        inp = ""

        stdscr.move(ZONE_INPUT[0], ZONE_INPUT[1])
        curses.curs_set(1)
        curses.flushinp()  # сброс всех буфферов ввода

        # Пока не запонится поле для ввода
        while len(inp) < ZONE_INPUT[4] * ZONE_INPUT[5] - 1:
            key_id = stdscr.getch()
            key = chr(key_id)

            # Вывод клавиши на экран, если это цифра или буква
            if key.isalpha() or key_id in range(32, 65):
                stdscr.addstr(key)
                inp += key

                cy, cx = stdscr.getyx()  # положение курсора
                # Если курсор достиг края, он перемещается на след. строку
                if cx == ZONE_INPUT[1] + ZONE_INPUT[5]:
                    stdscr.move(cy + 1, ZONE_INPUT[1])

            # Нажат ли Backspase и есть ли возможность что-то стереть
            elif key_id == 8 and inp != "":
                cy, cx = stdscr.getyx()
                # Если курсор находится в начале новой строки, то сотрется
                # символ, находящийся в конце предыдущей
                if cx == ZONE_INPUT[1]:
                    dely = cy - 1
                    delx = ZONE_INPUT[1] + ZONE_INPUT[5] - 1
                # Иначе сотрется символ, находящийся за курсором
                else:
                    dely = cy
                    delx = cx - 1
                stdscr.addch(dely, delx, " ")  # удаление = замена на пробел
                stdscr.move(dely, delx)
                inp = inp[:-1]

            # Если нажат Esc, то удаляется ввод и курсор перемещается в начало
            elif key_id == 27:
                self.clear_zone(ZONE_INPUT)
                inp = ""

            # Если нажат Enter, то ввод заканчивается
            elif key_id in (10, 13):
                break

        curses.curs_set(0)
        self.clear_zone(ZONE_INPUT)
        return inp

    def input_delayinterrupt(self, delay):
        """Создает задержку. Возвращает True, при прерывании её нажатием."""
        stdscr = self.stdscr
        curses.flushinp()
        stdscr.timeout(round(delay * 1000))  # перевод в миллесекунды
        key = stdscr.getch()
        stdscr.timeout(-1)

        if key == -1:
            return False
        else:
            return True

#
#             888  d8b                      888
#             888  Y8P                      888
#             888                           888
#         .d88888  888  .d8888b   88888b.   888   8888b.   888  888
#        d88" 888  888  88K       888 "88b  888      "88b  888  888
#        888  888  888  "Y8888b.  888  888  888  .d888888  888  888
#        Y88b 888  888       X88  888 d88P  888  888  888  Y88b 888
#         "Y88888  888   88888P'  88888P"   888  "Y888888   "Y88888  88888888
#                                 888                           888
#                                 888                      Y8b d88P
#                                 888                       "Y88P"

    def display_msg(self, id, *insert, delay=0, wait=True, speedup=1):
        """Печатает сообщение из реестра на заданное время, вставляя данные."""
        stdscr = self.stdscr
        ZONE_MSG = Screen.ZONE_MSG
        msg = data.MSG_REGISTRY[id]
        ch_print_delay = data.TIMINGS["PRINT-CHR"] / speedup

        # Если задержка - отрицательное число, то анимацию
        # печати прервать нельзя.
        if delay < 0:
            can_skip = False
        else:
            can_skip = True

        def printing_with_animation(with_animation):
            y, x_start = ZONE_MSG[0], ZONE_MSG[1] + 1
            insert_idx = 0
            fill = 1  # заполненность текущей строки по x

            # Отчищение зоны сообщений и перемещение курсора в ее начало
            self.clear_zone(ZONE_MSG)
            stdscr.move(y, x_start)

            for word in msg.split():
                # Вставка слова из insert с учетов возможных знаков препинания
                if word.startswith("%s"):
                    word = str(insert[insert_idx]) + word[2:]
                    insert_idx += 1
                # Пауза в печати. Не ставится, если печать без анимации
                elif word == "%p":
                    if with_animation is True:
                        time.sleep(data.TIMINGS["PRINT-PAU"])
                    continue

                # Переход на новую строку по заполненности предыдущей
                # или по спец. символу.
                if fill + len(word) + 1 >= ZONE_MSG[5] or word == "%n":
                    y += 1
                    fill = 1
                    stdscr.move(y, x_start)
                    if word == "%n":
                        continue

                # Печать слова с анимацией или без нее
                if with_animation is True:
                    result = self.anim_percharword(word, ch_print_delay,
                                                   can_skip)
                    if result != 0:
                        return -1
                else:
                    stdscr.addstr(word + " ")
                fill += len(word) + 1  # увеличение заполненности строки

            return 0

        # Печать с анимацией. Если она была прервана, то печать без анимации
        result = printing_with_animation(True)
        if result != 0:
            printing_with_animation(False)

        # Если необходимо ждать, пока игрок прочитает сообщение, то после
        # небольшой задержки появляетя мигающий курсор, ожидающий нажатия.
        if wait and delay == 0:
            if self.input_delayinterrupt(1) is False:
                curs_y, curs_x = stdscr.getyx()
                self.anim_arrowflick(curs_y, curs_x)
        # Если задержка - положительное число, то ее можно прервать нажатием
        # клавиши. Если отрицательное - прервать ее нельзя.
        elif delay > 0:
            self.input_delayinterrupt(delay)
        else:
            time.sleep(abs(delay))

    def display_dice(self, position, value, cp_id=0):
        """Отображает кость со значением value в координатах y и x."""
        stdscr = self.stdscr
        y, x = Screen.DICES_POSITIONS[position]
        stdscr.attron(curses.color_pair(cp_id))  # включение цвета печати

        # Построковая печать костей
        for idx, line in enumerate(data.ASCII_DICES[value]):
            # Печать первой строки с подчеркиваниями посередине, "крыша" кости
            if idx == 0 and value != 0:
                stdscr.addstr(y, x + 1, line[:-2],
                              curses.color_pair(cp_id) + curses.A_UNDERLINE)
            # Печать последней строки с подчеркиваниями посередине, "дно" кости
            elif idx == 3 and value != 0:
                stdscr.addstr(y + idx, x, line,
                              curses.color_pair(cp_id) + curses.A_UNDERLINE)
                stdscr.addch(y + 3, x, "│")
                stdscr.addch(y + 3, x + 6, "│")
            # Печать остальных строк
            else:
                stdscr.addstr(y + idx, x, line)

        stdscr.attroff(curses.color_pair(cp_id))  # отключение цвета печати

    def display_dices(self, dices):
        """Выводит на экран кости из списка dices в случайные позиции."""
        self.scr_dices = [0] * 6
        scr_dices = self.scr_dices

        # Зопись костей в scr_dices со случайными позициями
        positions = [i for i in range(6)]
        random.shuffle(positions)
        for i, value in enumerate(dices):
            scr_dices[positions[i]] = value

        # Отображение всех костей из scr_dices. "Нулевые" значения отчищают
        # свои позиции. Так отчищение зоны происходит автоматически.
        for position, value in enumerate(scr_dices):
            self.display_dice(position, value)
        self.stdscr.refresh()

    def display_score(self, player, score_type):
        """Печатает очки игоков (по типу) в зоне для очков."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE

        # Определение строки (для каждой свой тип очков)
        if score_type == "total":
            score = player.score_total
            y = ZONE_SCORE[0] + 3
        elif score_type == "turn":
            score = player.score_turn
            y = ZONE_SCORE[0] + 5
        elif score_type == "pick":
            score = player.score_pick
            y = ZONE_SCORE[0] + 6

        # Определение столбца (для каждого свой игрок)
        if player.__type__ == "Human":
            x = ZONE_SCORE[1] + 5
        else:
            x = ZONE_SCORE[1] + 14

        if score != 0:
            if score_type == "pick":
                stdscr.addstr(y, x, "+{}".format(score), curses.color_pair(3))
            else:
                stdscr.addstr(y, x, str(score), curses.A_UNDERLINE)
        else:
            # Отчищение строки, если очков нет
            if score_type == "pick":
                stdscr.addstr(y, x, "+" + " " * 5)
            else:
                stdscr.addstr(y, x, "_____")
        stdscr.refresh()

#
#                            d8b
#                            Y8P
#
#         8888b.   88888b.   888  88888b.d88b.
#            "88b  888 "88b  888  888 "888 "88b
#        .d888888  888  888  888  888  888  888
#        888  888  888  888  888  888  888  888
#        "Y888888  888  888  888  888  888  888  88888888

    def anim_playerhl(self, game_mode):
        """Плавно перемещает выделение с предыдущего на текущего игрока."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE
        y = ZONE_SCORE[0] + 1

        # Если текущий игрок - человек, то выделение перемещается справо
        # налево (с робота на человека). В обратном случае, наоборот.
        if game_mode.player.__type__ == "Human":
            name_h = game_mode.player.name
            name_r = game_mode.second_player.name
            for i in range(9 + len(name_r)):
                # Установка x_forward для выделения,  x_backward для его снятия
                x_f = ZONE_SCORE[1] + 14 - i
                x_b = ZONE_SCORE[1] + 14 + len(name_r) - i

                # Ограничение, чтобы выделение не заходило за имя человека
                if x_f >= ZONE_SCORE[1] + 5:
                    stdscr.chgat(y, x_f, 1, curses.color_pair(5))
                # Ограничение, чтобы выделения не снималось с имени человека
                if x_b >= ZONE_SCORE[1] + 5 + len(name_h):
                    stdscr.chgat(y, x_b, 1, curses.color_pair(0))

                stdscr.refresh()
                time.sleep(0.03)
        else:
            name_h = game_mode.second_player.name
            name_r = game_mode.player.name
            for i in range(9 + len(name_r)):
                x_f = ZONE_SCORE[1] + 5 + len(name_h) + i
                x_b = ZONE_SCORE[1] + 5 + i

                if x_f < ZONE_SCORE[1] + 14 + len(name_r):
                    stdscr.chgat(y, x_f, 1, curses.color_pair(5))
                if x_b < ZONE_SCORE[1] + 14:
                    stdscr.chgat(y, x_b, 1, curses.color_pair(0))

                stdscr.refresh()
                time.sleep(0.03)

    def anim_diceroll(self, num_of_dices):
        """Проигрывает анимацию броска костей."""
        rand_dices = []
        # Случайный выбор переданного кол-во костей и их показ на доли секунд
        for k in range(10):
            rand_dices = [random.randint(1, 6) for i in range(num_of_dices)]
            self.display_dices(rand_dices)
            time.sleep(0.1)

    def anim_arrowflick(self, y, x):
        """Создает мигающую стрелку и убирет её по нажатию."""
        stdscr = self.stdscr
        curr_cp, next_cp = 0, 6
        interrupt = False

        while interrupt is False:
            stdscr.addstr(y, x, "▼", curses.color_pair(curr_cp))
            interrupt = self.input_delayinterrupt(0.8)
            curr_cp, next_cp = next_cp, curr_cp

        stdscr.addstr(y, x, " ")

    def anim_percharword(self, word, ch_print_delay, can_skip):
        """Посимвольно печатает слово. Возвращает 0 в случае успеха."""
        stdscr = self.stdscr

        curses.flushinp()
        stdscr.timeout(0)

        for alpha in word + " ":
            stdscr.addch(alpha)
            stdscr.refresh()

            if stdscr.getch() != -1 and can_skip:
                stdscr.timeout(-1)
                return -1
            time.sleep(ch_print_delay)

        stdscr.timeout(-1)
        return 0

    def anim_ending(self):
        """Сдвигает экран вверх."""
        stdscr = self.stdscr
        stdscr.move(0, 0)
        for i in range(Screen.SH - 1):
            stdscr.deleteln()
            stdscr.refresh()
            time.sleep(0.04)

#
#                   .d888   .d888                     888
#                  d88P"   d88P"                      888
#                  888     888                        888
#         .d88b.   888888  888888  .d88b.    .d8888b  888888
#        d8P  Y8b  888     888    d8P  Y8b  d88P"     888
#        88888888  888     888    88888888  888       888
#        Y8b.      888     888    Y8b.      Y88b.     Y88b.
#         "Y8888   888     888     "Y8888    "Y8888P   "Y888  88888888

    def effect_hldices(self, dices=[], *, cp_id=3):
        """Выделяет или снимает выделение с костей."""
        scr_dices = self.scr_dices[:]
        # Пустой массив dices означает, что нужно снять выделение.
        # Непустой - выделение создать.
        if dices != []:
            for value in dices:
                position = scr_dices.index(value)
                self.display_dice(position, value, cp_id)
                scr_dices[position] = 0
        else:
            for position, value in enumerate(scr_dices):
                self.display_dice(position, value)
        self.stdscr.refresh()

    def effect_hlplayers(self, game_mode):
        """Выделяет имя текущего игрока."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE
        p1, p2 = game_mode.player, game_mode.second_player

        if p1.__type__ == "Human":
            stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 5,
                          p1.name, curses.color_pair(5))
            stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 14,
                          p2.name, curses.color_pair(0))
        elif p1.__type__ == "Robot":
            stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 14,
                          p1.name, curses.color_pair(5))
            stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 5,
                          p2.name, curses.color_pair(0))
        stdscr.refresh()

#
#                       888       888
#                       888       888
#                       888       888
#         8888b.    .d88888   .d88888
#            "88b  d88" 888  d88" 888
#        .d888888  888  888  888  888
#        888  888  Y88b 888  Y88b 888
#        "Y888888   "Y88888   "Y88888  88888888

    def add_players(self, game_mode):
        """Печатает на экране имена игроков в зоне для очков."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE
        name1, name2 = game_mode.player.name, game_mode.second_player.name

        stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 5, name1)
        stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 14, name2)

        self.effect_hlplayers(game_mode)

    def add_high_bar(self, hbar):
        """Печатает число очков для победы в зоне для очков."""
        ZONE_SCORE = Screen.ZONE_SCORE
        self.stdscr.addstr(ZONE_SCORE[0] + 7, ZONE_SCORE[1] + 9, str(hbar),
                           curses.A_UNDERLINE)

#
#                  888
#                  888
#                  888
#         .d88b.   888  .d8888b    .d88b.
#        d8P  Y8b  888  88K       d8P  Y8b
#        88888888  888  "Y8888b.  88888888
#        Y8b.      888       X88  Y8b.
#         "Y8888   888   88888P'   "Y8888

    def clear_zone(self, zone, back=" ", cp_id=0):
        """Принимает конст. ZONE_*, задний фон, цвет, и отчищает эту зону."""
        stdscr = self.stdscr
        for y in range(zone[0], zone[2] + 1):
            stdscr.addstr(y, zone[1], back * zone[5], curses.color_pair(cp_id))
        stdscr.refresh()
