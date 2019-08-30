"""Этот модуль отвечает за графику игры."""
import curses
import os
import random
import time
from curses import textpad

MSG_REGISTRY = {
    "01_hello": "Добро пожаловать в игру! %p Я буду вашим ведущим",
    "02_name": "Как вас зовут?",
    "04_00_maxp":
                """%s, теперь введите максимальное число очков. %p Победит тот,
                кто наберет столько же или больше""",
    "04_01_errint": "We need a int",
    "04_02_errval": "Bad idea, do it again",
    "05_start": "Великолепно! Начинаем игру!",
    "06_whoturn": "%s, твой ход",
    "07_scoreturn": "%s, твои очки за ход: %s",
    "08_scoretot": "%s, всего ты заработал: %s",
    "09_scoreearn": "%s, ты заработал %s очков",
    "10_nodice": "Нет ни одной комбинации!",
    "11_baddice": "Некоторые кости не принесли вам очки",
    "12_badpick": "Вы не можете выбрать эти кости!",
    "13_enemy": "Ваш противник - робот по имени %s",
    "14_robpick": "Робот взял эти кости: %s",
    "15_00_robturnT": "Робот решил продолжить ход",
    "15_01_robrurnF": "Робот решил закончить ход",
    "16_won": "ПОЗДРАВЛЯЮ, %s!. ТЫ ПОБЕДИЛ!",
    "17_gmend": "Game was alrady en",
    "18_actchoose": """1 - продолжить ход, 2 - закончить ход,
                    0 - выбрать другие кости""",
    "19_badans": "Неправильный ответ",
    "20_dicechoose": "Выберите кости",
    "21_robthink": "Робот думает",
    "22_dontans":
                """Хорошо, можете не отвечать. %p Тогда я буду
                называть вас 'Человек'""",
    "25_badname": """Простите, но ваше имя не подходит. %p
                  выберете что-то другое""",
    "26_badalldice": "Никакие кости не принесли очков"
}

DICES = {
    0: ["       ", "       ", "       ", "       "],
    1: ["       ", "│     │", "│  ●  │", "│     │"],
    2: ["       ", "│    ●│", "│     │", "│●    │"],
    3: ["       ", "│●    │", "│  ●  │", "│    ●│"],
    4: ["       ", "│●   ●│", "│     │", "│●   ●│"],
    5: ["       ", "│●   ●│", "│  ●  │", "│●   ●│"],
    6: ["       ", "│●   ●│", "│●   ●│", "│●   ●│"]
}


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
    init_pairs -- пнициализация цветовых пар
    clear_zone -- отчищает указанную игровую зону
    input_str -- возвращает пользовательский ввод
    display_players -- выводит на экран имена игроков
    display_dices -- выводит на экран игральные кости
    display_score -- выводит на экран заработанные очки
    display_msg -- выводит на экран сообщения из реестра
    add_high_bar -- выводит на экран число очков для победы
    ending -- показывает анимацию исчезания окна

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
        self.scr_dices = [0] * 6  # индекс - позиция, значение "0" - пусто
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

        stdscr.attron(curses.color_pair(1))

        self.clear_zone((0, 0, SH - 2, SW - 2, SH, SW), "∙", 2)

        for zone, txt in ([ZONE_DICES, "┤кости├"], [ZONE_SCORE, "┤очки├"],
                          [ZONE_INPUT, "┤ввод├"], [ZONE_MSG, "┤сообщения├"]):
            uy, lx = zone[0] - 1, zone[1] - 1
            ly, rx = zone[2] + 1, zone[3] + 1
            textpad.rectangle(stdscr, uy, lx, ly, rx)
            stdscr.addstr(uy, lx, "∙")
            stdscr.addstr(uy, rx, "∙")
            stdscr.addstr(ly, lx, "∙")
            stdscr.addstr(ly, rx, "∙")
            stdscr.addstr(uy, rx - len(txt) - 2, txt)
            self.clear_zone(zone)

        stdscr.addstr(ZONE_SCORE[0] + 3, ZONE_SCORE[1] + 1,
                      "Общ _____    _____")
        stdscr.addstr(ZONE_SCORE[0] + 5, ZONE_SCORE[1] + 1,
                      "Ход _____    _____")
        stdscr.addstr(ZONE_SCORE[0] + 7, ZONE_SCORE[1] + 1, "Поб     _____")
        stdscr.addstr(ZONE_INPUT[0], ZONE_INPUT[1] - 1, ">")

        stdscr.refresh()

    def __del__(self):
        """Завершение работы экрана и возврат стд. параметров терминала."""
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

    def init_pairs(self):
        """Установка цветовых пар (используемых цветов)."""
        curses.init_pair(1, 15, 0)
        curses.init_pair(2, 26, 0)
        curses.init_pair(3, 39, 0)
        curses.init_pair(4, 12, 0)

    def input_str(self):
        """Получает пользовательский ввод в зоне для ввода и возвращает его."""
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

            # Если нажат Enter то ввод заканчивается
            elif key_id in (10, 13):
                break

        curses.curs_set(0)
        self.clear_zone(ZONE_INPUT)
        return inp

    def display_msg(self, id, delay=0, *data):
        """Выводит сообщение из реестра на заданное время, вставляя данные."""
        stdscr = self.stdscr
        ZONE_MSG = Screen.ZONE_MSG
        y, x = ZONE_MSG[0], ZONE_MSG[1] + 1
        msg = MSG_REGISTRY[id]
        fill = 1  # заполненность текущей строки по x
        data_idx = 0

        # Отчищение зоны сообщений и перемещение курсора в ее начало
        self.clear_zone(ZONE_MSG)
        stdscr.move(y, x)

        for word in msg.split():
            # Вставка данных по спец символу
            if word.startswith("%s"):                  # Учет возможных
                word = str(data[data_idx]) + word[2:]  # знаков препинания.
                data_idx += 1
            # Пауза во вводе по спец символу
            elif word == "%p":
                time.sleep(0.4)
                continue

            # Переход на новую строку при переполнении предыдущей
            if fill + len(word) + 1 > ZONE_MSG[5]:
                stdscr.move(y + 1, x)
                fill = 1

            # Посимвольный ввод слова
            for alpha in word + " ":
                stdscr.addch(alpha)
                stdscr.refresh()
                time.sleep(0.02)
            fill += len(word) + 1

        # Если задержка - положительное число, то ее можно прервать нажатием
        # клавиши. Если отрицательное - прервать ее нельзя.
        if delay > 0:
            curses.flushinp()
            stdscr.timeout(round(delay * 1000))
            stdscr.getch()
            stdscr.timeout(-1)
        else:
            time.sleep(abs(delay))

    def display_dices(self, dices):
        """Выводит на экран кости из списка dices."""
        self.scr_dices = [0] * 6
        scr_dices = self.scr_dices

        # Зопись костей в scr_dices со случайными позициями
        positions = [i for i in range(6)]
        random.shuffle(positions)
        for i, value in enumerate(dices):
            scr_dices[positions[i]] = value

        # Отображение всех костей из scr_dices. "Нулевые" значения отчищают
        # свои позиции.
        for position, value in enumerate(scr_dices):
            self.display_dice(position, value)
        self.stdscr.refresh()

    def display_dice(self, position, value, cp_id=-1):
        """Отображает кость со значением value в координатах y и x."""
        stdscr = self.stdscr
        y, x = Screen.DICES_POSITIONS[position]
        stdscr.attron(curses.color_pair(cp_id))  # Включение цвета печати

        # Построковая печать костей
        for idx, line in enumerate(DICES[value]):
            # Печать первой строки с подчеркиваниями посередине, "крыша" кости
            if idx == 0 and value != 0:
                stdscr.addstr(y, x + 1, line[:-2],
                              curses.color_pair(cp_id) + curses.A_UNDERLINE)
            # Печать последней строки с подчеркиваниями посередине,"дно" кости
            elif idx == 3 and value != 0:
                stdscr.addstr(y + idx, x, line,
                              curses.color_pair(cp_id) + curses.A_UNDERLINE)
                stdscr.addch(y + 3, x, "│")
                stdscr.addch(y + 3, x + 6, "│")
            # Печать остальных строк
            else:
                stdscr.addstr(y + idx, x, line)

        stdscr.attroff(curses.color_pair(cp_id))  # Отключение цвета печати

    def display_players(self, game_mode):
        """Печатает на экране имена игроков в зоне для очков."""
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE
        n1 = game_mode.player.name
        n2 = game_mode.second_player.name
        stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 5, n1)
        stdscr.addstr(ZONE_SCORE[0] + 1, ZONE_SCORE[1] + 14, n2)
        stdscr.refresh()

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

        # Определение столбца (для каждого свой игрок)
        if player.__type__ == "Robot":
            x = ZONE_SCORE[1] + 14
        elif player.__type__ == "Human":
            x = ZONE_SCORE[1] + 5

        if score != 0:
            stdscr.addstr(y, x, str(score), curses.A_UNDERLINE)
        else:
            stdscr.addstr(y, x, "_____")  # отчищение строки, если очков нет
        stdscr.refresh()

    def display_pick_score(self, score=0):
        """Отображает очки, которые приносят выбранные кости"""
        stdscr = self.stdscr
        ZONE_DICES = Screen.ZONE_DICES
        stdscr.addstr(ZONE_DICES[0] + ZONE_DICES[4] - 1,
                      ZONE_DICES[1], " " * ZONE_DICES[5])
        stdscr.addstr(ZONE_DICES[0] + ZONE_DICES[4] - 1,
                      ZONE_DICES[1] + 2, "= {}".format(score))

    def clear_zone(self, zone, back=" ", cp_id=0):
        """Принимает конст. ZONE_*, задний фон, цвет, и отчищает эту зону."""
        stdscr = self.stdscr
        for y in range(zone[0], zone[2] + 1):
            stdscr.addstr(y, zone[1], back * zone[5], curses.color_pair(cp_id))
        stdscr.refresh()

    def add_high_bar(self, hbar):
        """Печатает число очков для победы в зоне для очков."""
        ZONE_SCORE = Screen.ZONE_SCORE
        self.stdscr.addstr(ZONE_SCORE[0] + 7, ZONE_SCORE[1] + 9, str(hbar),
                           curses.A_UNDERLINE)

    def dices_highlightion(self, dices=[], *, cp_id=3):
        """Выделяет или снимает выделение с костей"""
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

    def ending(self):
        """Проигрывает анимацию сдвига экрана вверх."""
        stdscr = self.stdscr
        stdscr.move(0, 0)
        for i in range(Screen.SH - 1):
            stdscr.deleteln()
            stdscr.refresh()
            time.sleep(0.04)
