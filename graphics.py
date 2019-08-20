"""Этот модуль отвечает за графику игры."""
import curses
from curses import textpad
import time
import os

MSG_REGISTRY = {'01_hello': 'Добро пожаловать в игру! %p Я буду вашим ведущим',
                '02_name':  'Как вас зовут?',
                '03_writing': 'Ok... let me write it down... yep.',
                '04_00_maxp': '''Человек, введите максимальное число очков.
                                 %p Победит тот, кто наберет столько же или
                                 больше''',
                '04_01_errint': 'We need a int',
                '04_02_errval': 'Bad idea, do it again',
                '05_start': 'Великолепно! Начинаем игру!',
                '06_whoturn': '%s, твой ход',
                '07_scoreturn': '%s, твои очки за ход: %s',
                '08_scoretot': '%s, всего ты заработал: %s',
                '09_scoreearn': '%s, ты заработал %s очков',
                '10_nodice': 'Нет ни одной комбинации!',
                '11_baddice': 'Некоторые кости не принесли вам очки: %s',
                '12_badpick': 'Вы не можете выбрать эти кости!',
                '13_enemy': """Вас я буду называть Человек. %p А ваш противник -
                               робот по имени %s""",
                '14_robpick': 'Робот взял эти кости: %s',
                '15_00_robturnT': 'Робот решил продолжить ход',
                '15_01_robrurnF': 'Робот решил закончить ход',
                '16_won': 'ПОЗДРАВЛЯЮ, %s!. ТЫ ПОБЕДИЛ!',
                '17_gmend': 'Game was alrady en',
                '18_continue': 'Продолжить ход? (1/0)',  # ДОПИЛИТЬ
                '19_badans': 'Неправильный ответ',
                '20_dicechoose': 'Выберите кости',
                '21_robthink': 'Робот думает',
                '22_dontans': 'Можете не отвечать, если не хотите',
                '23_givname': 'Я буду называть вас \'Человек\'',
                '24_hbar': 'Выберите максимальное число очков'
                }


class Screen:

    SH, SW = 30, 65
    ZONE_DICES = (3, 5, 9, 37, 7, 33)
    ZONE_SCORE = (3, 43, 9, 59, 7, 17)
    ZONE_INPUT = (20, 5, 23, 40, 4, 36)
    ZONE_MSG = (14, 5, 16, 59, 3, 55)

    def __init__(self):
        SH, SW = Screen.SH, Screen.SW
        ZONE_DICES = Screen.ZONE_DICES
        ZONE_INPUT = Screen.ZONE_INPUT
        ZONE_MSG = Screen.ZONE_MSG
        ZONE_SCORE = Screen.ZONE_SCORE
        self.stdscr = curses.initscr()
        stdscr = self.stdscr

        os.system('mode con: cols={0} lines={1}'.format(SW, SH))
        stdscr.resize(SH, SW)
        curses.start_color()
        curses.use_default_colors()
        self.init_pairs()
        curses.noecho()
        # stdscr.keypad(True)   BUG: Нажатие конопи 546
        curses.curs_set(0)

        self.clear_zone((0, 0, SH-2, SW-2, SH, SW), '.', 2)

        stdscr.attron(curses.color_pair(1))
        stdscr.box()
        textpad.rectangle(stdscr,
                          ZONE_DICES[0] - 1, ZONE_DICES[1] - 1,
                          ZONE_DICES[2] + 1, ZONE_DICES[3] + 1)
        textpad.rectangle(stdscr,
                          ZONE_SCORE[0] - 1, ZONE_SCORE[1] - 1,
                          ZONE_SCORE[2] + 1, ZONE_SCORE[3] + 1)
        textpad.rectangle(stdscr,
                          ZONE_INPUT[0] - 1, ZONE_INPUT[1] - 1,
                          ZONE_INPUT[2] + 1, ZONE_INPUT[3] + 1)
        textpad.rectangle(stdscr,
                          ZONE_MSG[0] - 1, ZONE_MSG[1] - 1,
                          ZONE_MSG[2] + 1, ZONE_MSG[3] + 1)
        stdscr.attroff(curses.color_pair(1))

        self.clear_zone(ZONE_DICES)
        self.clear_zone(ZONE_INPUT)
        self.clear_zone(ZONE_SCORE)
        self.clear_zone(ZONE_MSG)

        txt = '/кости/'
        stdscr.addstr(ZONE_DICES[0] - 1, ZONE_DICES[3] - len(txt), txt)
        txt = '/очки/'
        stdscr.addstr(ZONE_SCORE[0] - 1, ZONE_SCORE[3] - len(txt), txt)
        txt = '/ввод/'
        stdscr.addstr(ZONE_INPUT[0] - 1, ZONE_INPUT[3] - len(txt), txt)
        txt = '/сообщения/'
        stdscr.addstr(ZONE_MSG[0] - 1, ZONE_MSG[3] - len(txt), txt)

        stdscr.addstr(ZONE_INPUT[0], ZONE_INPUT[1] - 1, '>')

        for y in range(ZONE_SCORE[0], ZONE_SCORE[2] + 1):
            stdscr.addstr(y, ZONE_SCORE[1] + ZONE_SCORE[5] // 2, '│')
        txt = 'В'
        stdscr.addstr(ZONE_SCORE[0] + 2, ZONE_SCORE[1], ' ' * ZONE_SCORE[5])
        stdscr.addstr(ZONE_SCORE[0] + 2, ZONE_SCORE[1] + ZONE_SCORE[5] // 2 -
                      len(txt) // 2, txt, curses.A_UNDERLINE)
        txt = 'Х'
        stdscr.addstr(ZONE_SCORE[0] + 4, ZONE_SCORE[1], ' ' * ZONE_SCORE[5])
        stdscr.addstr(ZONE_SCORE[0] + 4, ZONE_SCORE[1] + ZONE_SCORE[5] // 2 -
                      len(txt) // 2, txt, curses.A_UNDERLINE)
        txt = 'победа ='
        stdscr.addstr(ZONE_SCORE[0] + ZONE_SCORE[4] - 1, ZONE_SCORE[1] +
                      ZONE_SCORE[5] // 2 - len(txt) + 1, txt)

        stdscr.refresh()

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

    def init_pairs(self):
        curses.init_pair(1, 15, 0)
        curses.init_pair(2, 25, 0)

    def clear_zone(self, zone, back=' ', cp_id=0):
        stdscr = self.stdscr
        for y in range(zone[0], zone[2] + 1):
            stdscr.addstr(y, zone[1], back * zone[5], curses.color_pair(cp_id))
        stdscr.refresh()

    def input_str(self):
        stdscr = self.stdscr
        ZONE_INPUT = Screen.ZONE_INPUT
        inp = ''

        stdscr.move(ZONE_INPUT[0], ZONE_INPUT[1])
        curses.curs_set(1)

        # Пока не запонится поле для ввода
        while len(inp) < ZONE_INPUT[4] * ZONE_INPUT[5] - 1:
            key_id = stdscr.getch()  # BUG: Нажатия работают постоянно
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
            elif key_id == 8 and inp != '':
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
                stdscr.addch(dely, delx, ' ')  # удаление = замена на пробел
                stdscr.move(dely, delx)  # курсор перемещается назад
                inp = inp[:-1]  # уменьшение ввода на удаленный символ

            # Если нажат Esc, то удаляется ввод и курсор перемещается в начало
            elif key_id == 27:
                self.clear_zone(ZONE_INPUT)
                inp = ''

            # Если нажат Enter то ввод заканчивается
            elif key_id in (10, 13):
                break

        curses.curs_set(0)
        self.clear_zone(ZONE_INPUT)
        return inp

    def display_players(self, game_mode):
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE
        name1 = game_mode.player.name
        name2 = game_mode.second_player.name
        stdscr.addstr(ZONE_SCORE[0], ZONE_SCORE[1] + 1, name1)
        stdscr.addstr(ZONE_SCORE[0], ZONE_SCORE[1] + ZONE_SCORE[5] // 2 + 2,
                      name2)
        stdscr.refresh()

    def display_dices(self, dices):
        stdscr = self.stdscr
        ZONE_DICES = Screen.ZONE_DICES

        self.clear_zone(ZONE_DICES)
        string = ('[%d] ' * len(dices) % tuple(dices))[:-1]
        stdscr.addstr(ZONE_DICES[0] + ZONE_DICES[4] // 2,
                      ZONE_DICES[1] + ZONE_DICES[5] // 2 - len(string) // 2,
                      string)
        stdscr.refresh()

    def display_score(self, player, score_type):
        stdscr = self.stdscr
        ZONE_SCORE = Screen.ZONE_SCORE

        if score_type == 'total':
            score = player.score_total
            y = ZONE_SCORE[0] + 2
        elif score_type == 'turn':
            score = player.score_turn
            y = ZONE_SCORE[0] + 4

        if player.__type__ == 'Robot':
            x = ZONE_SCORE[1] + ZONE_SCORE[5] // 2 + 2
        elif player.__type__ == 'Human':
            x = ZONE_SCORE[1] + 1

        if score != 0:
            stdscr.addstr(y, x, str(score))
        else:
            stdscr.addstr(y, x, '     ')
        stdscr.refresh()

    def display_msg(self, id, display_time=0, *data):
        stdscr = self.stdscr
        ZONE_MSG = Screen.ZONE_MSG
        y, x = ZONE_MSG[0], ZONE_MSG[1]
        msg = MSG_REGISTRY[id]
        fill = 0  # заполненность строк по x
        data_idx = 0

        # Отчищение зоны сообщений и перемещение курсора в ее начало
        self.clear_zone(Screen.ZONE_MSG)
        stdscr.move(y, x)

        for word in msg.split():
            # Проверка, не нужно ли вставить данные
            if word.startswith('%s'):                   # Учитываем возможные
                word = str(data[data_idx]) + word[2:]  # знаки препинания.
                data_idx += 1
            elif word == '%p':  # Необходимо ли сделать паузу
                time.sleep(0.3)
                continue

            if fill + len(word) + 1 > ZONE_MSG[5]:  # Переход на новую строку
                stdscr.move(y + 1, x)               # при переполнении преды-
                fill = 0                            # дущей.
            for liter in word + ' ':
                stdscr.addch(liter)  # Ввод слова посимвольно,
                stdscr.refresh()     # со вставкой пробела.
                time.sleep(0.02)
            fill += len(word) + 1

        if display_time != 0:
            time.sleep(display_time)
            self.clear_zone(Screen.ZONE_MSG)

    def add_high_bar(self, hbar):
        """Печатает число очков для победы в зоне для очков."""
        ZONE_SCORE = Screen.ZONE_SCORE
        self.stdscr.addstr(ZONE_SCORE[0] + ZONE_SCORE[4] - 1,
                           ZONE_SCORE[1] + ZONE_SCORE[5] // 2 + 2, str(hbar))

    def ending(self):
        """Проигрывает анимацию сдвига экрана вверх."""
        stdscr = self.stdscr
        stdscr.move(0, 0)
        for i in range(Screen.SH-1):
            stdscr.deleteln()
            stdscr.refresh()
            time.sleep(0.04)


'''
    def display_debug(self, display_time, data='BEEP'):  # ОТЛАДКА
        stdscr = self.stdscr
        stdscr.addstr(12, 0, str(data) + ' '*(Screen.SW - len(str(data))))
        time.sleep(display_time)
        stdscr.addstr(12, 0, ' '*Screen.SW)
'''
