import curses
import time

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
                '18_continue': 'Continue turn? (y/n)',
                '19_badans': 'Wrong answer',
                '20_dicechoose': 'Choose the dices'
                }


class Screen:

    ZONE_INPUT = (7, 3)
    ZONE_DICES = (3, None)
    ZONE_MSG = (4, 0)

    def __init__(self):
        self.stdscr = curses.initscr()
        self.sh, self.sw = self.stdscr.getmaxyx()
        # curses.noecho()
        # curses.cbreak()
        # self.stdscr.keypad(True)
        curses.curs_set(0)

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

    def input_str(self):
        stdscr = self.stdscr
        stdscr.addstr(Screen.ZONE_INPUT[0], 0, ' '*self.sw)
        curses.curs_set(1)
        b_str = stdscr.getstr(Screen.ZONE_INPUT[0], Screen.ZONE_INPUT[1])
        curses.curs_set(0)
        stdscr.addstr(Screen.ZONE_INPUT[0], 0, ' '*self.sw)
        stdscr.refresh()
        return b_str.decode('utf-8')

    def display_dices(self, dices):
        stdscr = self.stdscr
        stdscr.addstr(Screen.ZONE_DICES[0], 0, ' '*self.sw)
        for idx, dice in enumerate(dices):
            stdscr.addstr(Screen.ZONE_DICES[0], 5*idx, '[{}]'.format(dice))
        stdscr.refresh()

    def display_msg(self, id, display_time, *data):
        stdscr = self.stdscr
        y, x = Screen.ZONE_MSG[0], Screen.ZONE_MSG[1]
        stdscr.addstr(y, x, ' '*(self.sw - x))
        stdscr.addstr(y, x, MSG_REGISTRY[id] % data)
        stdscr.refresh()
        time.sleep(display_time)

    def display_debug(self, display_time, data='BEEP'):  # ОТЛАДКА
        stdscr = self.stdscr
        stdscr.addstr(12, 0, str(data) + ' '*(self.sw - len(str(data))))
        time.sleep(display_time)
        stdscr.addstr(12, 0, ' '*self.sw)
