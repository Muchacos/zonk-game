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
#
class Screen:
    """Представляет игровой экран, отображающий всю графику.

    Поля:
    stdscr -- стандартный экран игры
    scr_dices -- кости, находящийся на экране. Индекс означает позицию по
                 DICES_POSITIONS. Значение "0" означает пустоту, т.е. при
                 отображении "нулевой" кости, ее позиция очистится.
    SH, SW -- досл. screen hight и screen width
    ZONE_*NAME* -- координаты различных зон экрана:
                   [0] и [1] - y и x левого верхнего угла;
                   [2] и [3] - y и x правого нижнего угла;
                   [4] и [5] - длина зоны по y и x
    DICES_POSITIONS -- Позиции костей (верхний левый угол) в зоне для костей

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
        SH, SW = Screen.SH, Screen.SW
        self.scr_dices = [0] * 6
        self.msg_display_settings = data.MSG_DISPLAY_DEFAULT_SETTINGS.copy()
        self.stdscr = curses.initscr()
        stdscr = self.stdscr

        os.system("mode con: cols={0} lines={1}".format(SW, SH))
        stdscr.resize(SH, SW)
        curses.start_color()
        curses.use_default_colors()
        self.init_pairs()
        curses.noecho()
        stdscr.keypad(True)
        curses.curs_set(0)
        stdscr.bkgd(" ", curses.color_pair(1))

    def __del__(self):
        curses.beep()
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

    def init_pairs(self):
        """Инициализация цветовых пар (используемых цветов)."""
        curses.init_pair(1, 15, 16)  # Ярко-белый
        curses.init_pair(2, 16, 16)   # Черный
        curses.init_pair(3, 39, 16)  # Голубой
        curses.init_pair(4, 12, 16)  # Красный
        curses.init_pair(5, 0, 15)  # Ченрый на белом
        curses.init_pair(6, 26, 16)  # Светло-синий
        curses.init_color(256, 0, 153, 306)
        curses.init_color(257, 0, 24, 87)
        curses.init_pair(20, 256, 257)  # Глубокий синий на сверхтемном синем
        curses.init_color(258, 0, 275, 550)
        curses.init_color(259, 4, 40, 138)
        curses.init_pair(21, 258, 259)  # Насыщенный синий на очень темно синем
        curses.init_color(260, 816, 988, 1000)
        curses.init_color(261, 31, 110, 271)
        curses.init_pair(22, 260, 261)  # Барвинок на горечавково-синием
        curses.init_pair(23, 15, 257)  # Ярко-белый на сверхтемном синем
        curses.init_pair(24, 15, 259)  # Ярко-белый на очень темно синем

    #  d8b                                888
    #  Y8P                                888
    #                                     888
    #  888  88888b.   88888b.   888  888  888888
    #  888  888 "88b  888 "88b  888  888  888
    #  888  888  888  888  888  888  888  888
    #  888  888  888  888 d88P  Y88b 888  Y88b.
    #  888  888  888  88888P"    "Y88888   "Y888  88888888
    #                 888
    #                 888
    #                 888
    def input_str(self):
        """Возвращает введенную пользователем строку."""
        stdscr = self.stdscr
        ZONE_INPUT = Screen.ZONE_INPUT
        inp = ""

        stdscr.move(ZONE_INPUT[0], ZONE_INPUT[1])
        curses.curs_set(1)
        curses.flushinp()

        # Пока не запонится поле для ввода
        while len(inp) < ZONE_INPUT[4] * ZONE_INPUT[5] - 1:
            key_id = stdscr.getch()
            key = chr(key_id)

            # Если нажата клавиша цифры или буквы
            if key.isalpha() or key_id in range(32, 65):
                stdscr.addstr(key)
                inp += key
                # Если курсор достиг края, он перемещается на след. строку
                cy, cx = stdscr.getyx()
                if cx == ZONE_INPUT[1] + ZONE_INPUT[5]:
                    stdscr.move(cy + 1, ZONE_INPUT[1])

            # Если нажат Enter
            elif key_id in (10, 13):
                break

            # Если нажат Backspase (и есть что стереть)
            elif key_id == 8 and inp != "":
                cy, cx = stdscr.getyx()
                # Если курсор не находится в начале новой строки, то сотрется
                # символ, находящийся за курсором
                if cx != ZONE_INPUT[1]:
                    dely = cy
                    delx = cx - 1
                # Иначе сотрется символ, находящийся в конце предыдущей строки
                else:
                    dely = cy - 1
                    delx = ZONE_INPUT[1] + ZONE_INPUT[5] - 1
                stdscr.addch(dely, delx, " ")  # удаление = замена на пробел
                stdscr.move(dely, delx)
                inp = inp[:-1]

            # Если нажат Esc
            elif key_id == 27:
                self.clear_zone(ZONE_INPUT)
                inp = ""

        curses.curs_set(0)
        self.clear_zone(ZONE_INPUT)
        return inp

    def input_delayinterrupt(self, delay):
        """Создает задержку, прерываемую нажатием любой кнопки."""
        stdscr = self.stdscr
        curses.flushinp()
        stdscr.timeout(round(delay * 1000))  # перевод в миллесекунды
        key = stdscr.getch()
        stdscr.timeout(-1)

        if key == -1:
            return False
        else:
            return True

    #       888  d8b                      888
    #       888  Y8P                      888
    #       888                           888
    #   .d88888  888  .d8888b   88888b.   888   8888b.   888  888
    #  d88" 888  888  88K       888 "88b  888      "88b  888  888
    #  888  888  888  "Y8888b.  888  888  888  .d888888  888  888
    #  Y88b 888  888       X88  888 d88P  888  888  888  Y88b 888
    #   "Y88888  888   88888P'  88888P"   888  "Y888888   "Y88888  88888888
    #                           888                           888
    #                           888                      Y8b d88P
    #                           888                       "Y88P"
    #
    def display_msg(self, id, *insert, delay=None,
                    wait=None, speedup=None, inner_idx=None):
        """Выводит на экран сообщения из реестра."""
        stdscr = self.stdscr
        ZONE_MSG = Screen.ZONE_MSG
        settings = self.msg_display_settings

        if delay is None:
            delay = settings["delay"]
        if wait is None:
            wait = settings["wait"]
        if speedup is None:
            speedup = settings["speedup"]
        if inner_idx is not None:
            msg = data.MSG_REGISTRY[id][inner_idx]
        else:
            msg = data.MSG_REGISTRY[id]
        if delay < 0:
            can_skip = False
        else:
            can_skip = True

        ch_print_delay = data.TIMINGS["PRINT-CHR"] / speedup

        def printing_with_animation(with_animation):
            y, x_start = ZONE_MSG[0], ZONE_MSG[1] + 1
            insert_idx = 0
            fill = 1  # заполненность текущей строки по x

            self.clear_zone(ZONE_MSG)
            stdscr.move(y, x_start)

            for word in msg.split():
                # Вставка слова из insert с учетов возможных знаков препинания
                if word.startswith("%s"):
                    word = str(insert[insert_idx]) + word[2:]
                    insert_idx += 1
                # Пауза в печати. Не ставится, если печать без анимации
                elif word == "%p":
                    if with_animation:
                        time.sleep(data.TIMINGS["PRINT-PAU"])
                    continue

                # Переход на новую строку по заполненности предыдущей или
                # по спец. символу.
                if fill + len(word) + 1 >= ZONE_MSG[5] or word == "%n":
                    y += 1
                    fill = 1
                    stdscr.move(y, x_start)
                    if word == "%n":
                        continue

                # Печать слова с анимацией или без нее
                if with_animation:
                    result = self.anim_percharword(word, ch_print_delay,
                                                   can_skip)
                    if result == "interrupted":
                        return result
                else:
                    stdscr.addstr(word + " ")
                fill += len(word) + 1  # увеличение заполненности строки
            return "complete"

        result = printing_with_animation(True)
        if result == "interrupted":
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

    def display_msg_seq(self, seq_id, delay=None, wait=None, speedup=None):
        """Выводит на экран последовательность сообщений из реестра."""
        seq_len = len(data.MSG_REGISTRY[seq_id])
        for i in range(seq_len):
            self.display_msg(seq_id, delay=delay, wait=wait,
                             speedup=speedup, inner_idx=i)

    def display_dice(self, position, value, *, cp=0):
        """Выводит на экран кость в указанную позицию."""
        stdscr = self.stdscr
        y, x = Screen.DICES_POSITIONS[position]

        stdscr.attron(curses.color_pair(cp))
        for idx, line in enumerate(data.ASCII_DICES[value]):
            # Печать первой строки с подчеркиваниями посередине, "крыша" кости
            if idx == 0 and value != 0:
                stdscr.addstr(y, x + 1, line[:-2],
                              curses.color_pair(cp) + curses.A_UNDERLINE)
            # Печать последней строки с подчеркиваниями посередине, "дно" кости
            elif idx == 3 and value != 0:
                stdscr.addstr(y + idx, x, line,
                              curses.color_pair(cp) + curses.A_UNDERLINE)
                stdscr.addch(y + 3, x, "│")
                stdscr.addch(y + 3, x + 6, "│")
            else:
                stdscr.addstr(y + idx, x, line)
        stdscr.attroff(curses.color_pair(cp))

    def display_dices(self, dices):
        """Выводит кости на экран."""
        self.scr_dices = [0] * 6
        scr_dices = self.scr_dices

        # Запись переданных костей в scr_dices со случайными позициями
        positions = [i for i in range(6)]
        random.shuffle(positions)
        for i, value in enumerate(dices):
            scr_dices[positions[i]] = value

        for position, value in enumerate(scr_dices):
            self.display_dice(position, value)
        self.stdscr.refresh()

    def display_score(self, player, score_type):
        """Выводит/убирает с экрана очки игрока."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE

        if score_type == "total":
            score = player.score_total
            y = ZONE_SCORE[0] + 3
        elif score_type == "turn":
            score = player.score_turn
            y = ZONE_SCORE[0] + 5
        elif score_type == "pick":
            score = player.score_pick
            y = ZONE_SCORE[0] + 6

        if player.type == "Human":
            x = ZONE_SCORE[1] + 5
        else:
            x = ZONE_SCORE[1] + 14

        if score != 0:
            if score_type == "pick":
                stdscr.addstr(y, x, "+{}".format(score), curses.color_pair(3))
            else:
                stdscr.addstr(y, x, str(score), curses.A_UNDERLINE)
        else:  # Отчищение строки, если очков нет
            if score_type == "pick":
                stdscr.addstr(y, x, "+" + " " * 5)
            else:
                stdscr.addstr(y, x, "_____")
        stdscr.refresh()

    #                      d8b
    #                      Y8P
    #
    #   8888b.   88888b.   888  88888b.d88b.
    #      "88b  888 "88b  888  888 "888 "88b
    #  .d888888  888  888  888  888  888  888
    #  888  888  888  888  888  888  888  888
    #  "Y888888  888  888  888  888  888  888  88888888
    #
    def anim_playerhl(self, game_mode):
        """Проигрывает анимацию бегунка, выделяющего имена игроков."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE
        y = ZONE_SCORE[0] + 1

        # Если текущий игрок - человек, то выделение перемещается справa
        # налево (с робота на человека). В обратном случае, наоборот.
        if game_mode.player.type == "Human":
            name_h = game_mode.player.name
            name_r = game_mode.second_player.name
            for i in range(9 + len(name_r)):
                # Установка x_forward для выделения, x_backward для его снятия
                x_f = ZONE_SCORE[1] + 14 - i
                x_b = ZONE_SCORE[1] + 14 + len(name_r) - i

                # Ограничение, чтобы выделение не заходило за имя человека
                if x_f >= ZONE_SCORE[1] + 5:
                    stdscr.chgat(y, x_f, 1, curses.color_pair(5))
                # Ограничение, чтобы выделение не снималось с имени человека
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
        for k in range(10):
            rand_dices = [random.randint(1, 6) for i in range(num_of_dices)]
            self.display_dices(rand_dices)
            time.sleep(0.1)

    def anim_arrowflick(self, y, x):
        """Проигрывает анимащию мигающей стрелки."""
        stdscr = self.stdscr
        curr_cp, next_cp = 0, 2
        interrupt = False

        while not interrupt:
            stdscr.addstr(y, x, "▼", curses.color_pair(curr_cp))
            interrupt = self.input_delayinterrupt(0.8)
            curr_cp, next_cp = next_cp, curr_cp

        stdscr.addstr(y, x, " ")

    def anim_percharword(self, word, ch_print_delay, can_skip):
        """Посимвольно выводит слово на экран."""
        stdscr = self.stdscr

        curses.flushinp()
        stdscr.timeout(0)
        for alpha in word + " ":
            stdscr.addch(alpha)
            stdscr.refresh()
            # Если игрок нажал кнопку и можно пропустить анимацию
            if stdscr.getch() != -1 and can_skip:
                stdscr.timeout(-1)
                return "interrupted"
            time.sleep(ch_print_delay)
        stdscr.timeout(-1)
        return "complete"

    def anim_ending(self):
        """Сдвигает экран вверх."""
        stdscr = self.stdscr
        stdscr.move(0, 0)
        for i in range(Screen.SH - 1):
            stdscr.deleteln()
            stdscr.refresh()
            time.sleep(0.04)

    #             .d888   .d888                     888
    #            d88P"   d88P"                      888
    #            888     888                        888
    #   .d88b.   888888  888888  .d88b.    .d8888b  888888
    #  d8P  Y8b  888     888    d8P  Y8b  d88P"     888
    #  88888888  888     888    88888888  888       888
    #  Y8b.      888     888    Y8b.      Y88b.     Y88b.
    #   "Y8888   888     888     "Y8888    "Y8888P   "Y888  88888888
    #
    def effect_hldices(self, dices=[], *, cp=3):
        """Выделяет кости."""
        scr_dices = self.scr_dices[:]

        if dices != []:
            for value in dices:
                position = scr_dices.index(value)
                self.display_dice(position, value, cp=cp)
                scr_dices[position] = 0
        else:  # Пустой список dices означает, что нужно снять выделение.
            for position, value in enumerate(scr_dices):
                self.display_dice(position, value)
        self.stdscr.refresh()

    def effect_hlplayers(self, game_mode):
        """Выделяет имя текущего игрока, снимая выделение с предыдущего."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE
        p1, p2 = game_mode.player, game_mode.second_player

        if p1.type == "Human":
            stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 5,
                          p1.name, curses.color_pair(5))
            stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 14,
                          p2.name, curses.color_pair(0))
        elif p1.type == "Robot":
            stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 14,
                          p1.name, curses.color_pair(5))
            stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 5,
                          p2.name, curses.color_pair(0))
        stdscr.refresh()

    #                 888       888
    #                 888       888
    #                 888       888
    #   8888b.    .d88888   .d88888
    #      "88b  d88" 888  d88" 888
    #  .d888888  888  888  888  888
    #  888  888  Y88b 888  Y88b 888
    #  "Y888888   "Y88888   "Y88888  88888888
    #
    def add_players(self, game_mode):
        """Добавляет на экран имена игроков."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE
        name1, name2 = game_mode.player.name, game_mode.second_player.name

        stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 5, name1)
        stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 14, name2)
        self.effect_hlplayers(game_mode)

    def add_high_bar(self, hbar):
        """Добавляет на экран high_bar."""
        ZONE_SCORE = Screen.ZONE_SCORE
        self.stdscr.addstr(ZONE_SCORE[0] + 7, ZONE_SCORE[1] + 9, str(hbar),
                           curses.A_UNDERLINE)

    def add_zonescore(self):
        """Отчищает и отрисовывает зону для очков."""
        stdscr = self.stdscr
        ZONE_SCORE = self.ZONE_SCORE

        self.clear_zone(ZONE_SCORE)
        zone_txt = [" Tot _____    _____ ",
                    " Tur _____    _____ ",
                    "     +        +     ",
                    " Win     _____      "]
        for i, y in enumerate((3, 5, 6, 7)):
            stdscr.addstr(ZONE_SCORE[0] + y, ZONE_SCORE[1], zone_txt[i])
        stdscr.refresh()

    def add_interface(self):
        """Мгновенно добавляет интерфейс на экран."""
        stdscr = self.stdscr
        SH, SW = Screen.SH, Screen.SW
        ZONE_DICES = Screen.ZONE_DICES
        ZONE_INPUT = Screen.ZONE_INPUT
        ZONE_SCORE = Screen.ZONE_SCORE
        ZONE_MSG = Screen.ZONE_MSG

        # Заполнение точками игрового окна
        self.clear_zone((0, 0, SH - 2, SW - 2, SH, SW), "∙", cp=6)

        stdscr.attron(curses.color_pair(1))
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

        self.add_zonescore()
        stdscr.addstr(ZONE_INPUT[0], ZONE_INPUT[1] - 1, ">")
        stdscr.attroff(curses.color_pair(1))
        stdscr.refresh()

    #            888
    #            888
    #            888
    #   .d88b.   888  .d8888b    .d88b.
    #  d8P  Y8b  888  88K       d8P  Y8b
    #  88888888  888  "Y8888b.  88888888
    #  Y8b.      888       X88  Y8b.
    #   "Y8888   888   88888P'   "Y8888
    #
    def clear_zone(self, zone, back=" ", *, cp=0):
        """Отчищает игровую зону."""
        stdscr = self.stdscr
        for y in range(zone[0], zone[2] + 1):
            stdscr.addstr(y, zone[1], back * zone[5], curses.color_pair(cp))
        stdscr.refresh()

    def msg_display_attron(self, *, delay=None, wait=None, speedup=None):
        """Включает атрибуты вывода сообщений."""
        settings = self.msg_display_settings
        if delay is not None:
            settings["delay"] = delay
        if wait is not None:
            settings["wait"] = wait
        if speedup is not None:
            settings["speedup"] = speedup

    def msg_display_attroff(self, *, delay=False, wait=False, speedup=False):
        """Отключает атрибуты вывода сообщений."""
        settings = self.msg_display_settings
        std_settings = data.MSG_DISPLAY_DEFAULT_SETTINGS
        if delay:
            settings["delay"] = std_settings["delay"]
        if wait:
            settings["wait"] = std_settings["wait"]
        if speedup:
            settings["speedup"] = std_settings["speedup"]

    def beep(self):
        """Делает *прлууммм*."""
        curses.beep()
