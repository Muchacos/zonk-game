import curses
from curses import textpad
import time
import os

MSG_REGISTRY = {'01_hello': 'Welcome to the game!',
                '02_name':  'What is your name?',
                '03_writing': 'Ok... let me write it down... yep.',
                '04_00_maxp': 'Now, choose a maximum fo points.',
                '04_01_errint': 'We need a int',
                '04_02_errval': 'Bad idea, do it again',
                '05_start': 'Great! We can start',
                '06_whoturn': '%s\'s turn',
                '07_scoreturn': '%s\'s score: %s',
                '08_scoretot': '%s\'s total score: %s',
                '09_scoreearn': '%s was earned %s points',
                '10_nodice': 'No dices to pick!',
                '11_baddice': 'Some dices do not give you points: %s',
                '12_badpick': 'You cannot pick these dices!',
                '13_enemy': 'Your enemy is %s',
                '14_robpick': 'Robot was picked: %s',
                '15_00_robturnT': 'Robot choosed to continue his turn',
                '15_01_robrurnF': 'Robot choosed to end his turn',
                '16_won': 'CONGRATS, %s!. YOU WON!',
                '17_gmend': 'Game was alrady end',
                '18_continue': 'Continue turn? (1/0)',  # ДОПИЛИТЬ
                '19_badans': 'Wrong answer',
                '20_dicechoose': 'Choose the dices',
                '21_robthink': 'Robot is thinking'
                }


class Screen:

    SH, SW = 30, 65
    ZONE_DICES = (3, 5, 9, 37, 7, 33)
    ZONE_SCORE = (3, 43, 9, 59, 7, 17)
    ZONE_INPUT = (20, 5, 20, 19, 1, 15)
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

        txt = '/dices/'
        stdscr.addstr(ZONE_DICES[0] - 1, ZONE_DICES[3] - len(txt), txt)
        txt = '/score/'
        stdscr.addstr(ZONE_SCORE[0] - 1, ZONE_SCORE[3] - len(txt), txt)
        txt = '/input/'
        stdscr.addstr(ZONE_INPUT[0] - 1, ZONE_INPUT[3] - len(txt), txt)
        txt = '/messages/'
        stdscr.addstr(ZONE_MSG[0] - 1, ZONE_MSG[3] - len(txt), txt)

        stdscr.addstr(ZONE_INPUT[0], ZONE_INPUT[1] - 1, '>')

        for y in range(ZONE_SCORE[0], ZONE_SCORE[2] + 1):
            stdscr.addstr(y, ZONE_SCORE[1] + ZONE_SCORE[5] // 2, '|')
        txt = 'В'
        stdscr.addstr(ZONE_SCORE[0] + 2, ZONE_SCORE[1], ' ' * ZONE_SCORE[5])
        stdscr.addstr(ZONE_SCORE[0] + 2, ZONE_SCORE[1] + ZONE_SCORE[5] // 2 -
                      len(txt) // 2, txt, curses.A_UNDERLINE)
        txt = 'Х'
        stdscr.addstr(ZONE_SCORE[0] + 4, ZONE_SCORE[1], ' ' * ZONE_SCORE[5])
        stdscr.addstr(ZONE_SCORE[0] + 4, ZONE_SCORE[1] + ZONE_SCORE[5] // 2 -
                      len(txt) // 2, txt, curses.A_UNDERLINE)

        stdscr.refresh()

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

    def init_pairs(self):
        curses.init_pair(1, 15, 0)
        curses.init_pair(2, 25, 0)

    def clear_zone(self, coord, back=' ', cp_id=0):
        stdscr = self.stdscr
        for y in range(coord[0], coord[2] + 1):
            stdscr.addstr(y, coord[1], back * coord[5],
                          curses.color_pair(cp_id))
        stdscr.refresh()

    def input_str(self):
        stdscr = self.stdscr
        ZONE_INPUT = Screen.ZONE_INPUT
        inp = ''

        stdscr.move(ZONE_INPUT[0], ZONE_INPUT[1])
        curses.curs_set(1)

        while len(inp) < ZONE_INPUT[5]:
            key = stdscr.getch()  # BUG: Нажатия работают постоянно
            if key in range(48, 58):
                stdscr.addstr(chr(key))
                inp += chr(key)
            elif key == 8 and inp != '':
                cy, cx = stdscr.getyx()
                stdscr.addch(cy, cx - 1, ' ')
                stdscr.move(cy, cx - 1)
                inp = inp[:-1]
            elif key == 10 and inp != '':
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
        y, x = Screen.ZONE_MSG[0], Screen.ZONE_MSG[1]
        self.clear_zone(Screen.ZONE_MSG)
        stdscr.addstr(y, x, MSG_REGISTRY[id] % data)
        stdscr.refresh()
        if display_time != 0:
            time.sleep(display_time)
            self.clear_zone(Screen.ZONE_MSG)
            return 0
        return 0

    def ending(self):
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
