''' Welcome to Zonk game! This is pre-alpha version,
everything you see is just a test. But thanks for bying!'''
import random


class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.score_turn = 0

    def add_scoretotal(self):
        self.score += self.score_turn
        self.score_turn = 0

    def add_scoreturn(self, score):
        self.score_turn += score

    def remove_scoreturn(self):
        self.score_turn = 0


class Game:
    game_flag = True
    dices = [1]*6

    def __init__(self):
        pass

    def set_settings(self, player, high_bar, printer):
        self.player = player
        self.high_bar = high_bar
        self.printer = printer

    def win_check(self):
        if self.player.score >= self.high_bar:
            Game.game_flag = False
            self.printer._print_won()

    def turn(self):
        printer = self.printer

        if Game.game_flag:
            for i in range(len(Game.dices)):
                Game.dices[i] = random.randint(1, 6)

            printer._print_dices(Game.dices)

            if 5 not in Game.dices and 1 not in Game.dices:
                printer._print_nodices()
                self.player.remove_scoreturn()
                return False

            turn_flag = printer.get_turncontinue()
            if not turn_flag:
                printer._print_scoreturn()
                self.player.add_scoretotal()
                printer._print_scoretotal()
                self.win_check()
                return False

            pick = 0

            while True:
                pick = printer.get_dicechoose(Game.dices)

                if Game.dices[pick] == 1:
                    printer._print_scoreearned(100)
                    self.player.add_scoreturn(100)
                    break
                elif Game.dices[pick] == 5:
                    printer._print_scoreearned(50)
                    self.player.add_scoreturn(50)
                    break
                else:
                    printer._print_wrongdice()
            Game.dices.pop(pick)
            printer._print_scoreturn()
            return True

        else:
            printer._print_gameend()
            return False

    def add_dices(self):
        Game.dices.extend([1]*(6 - len(Game.dices)))


class Printer:

    def __init__(self, game_mode):
        self.game_mode = game_mode

    def get_settings(self):
        print('Welcome to the game! What is your name?')
        p = Player(input())
        print('Ok... let me write it down... yep.\nNow, choose a maximum fo points.')
        high_bar = int(input())
        print('Great, we can start!')
        return (p, high_bar)

    def get_dicechoose(self, dices):
        print('\nPick a dice!')
        pick = 0
        while True:
            try:
                val = int(input('dice: '))
                pick = dices.index(val)
            except:
                continue
            else:
                break
        return pick

    def get_turncontinue(self):
        ans = ''
        print('We continue?')

        while ans not in ('y', 'n'):
            ans = input('y/n: ')
        if ans == 'y':
            return True
        elif ans == 'n':
            return False

    def _print_turnstart(self):
        gm = self.game_mode
        print('------------------------------')
        print(gm.player.name, ', your Turn!')

    def _print_dices(self, dices):
        str = ''
        for i in range(len(dices)):
            str += '[%d] ' % dices[i]
        print(str)

    def _print_scoreturn(self):
        print('Turn score:', self.game_mode.player.score_turn)

    def _print_scoretotal(self):
        score = self.game_mode.player.score
        print('Total score:', score)

    def _print_scoreearned(self, score):
        print('You earned %d points!' % score)

    def _print_nodices(self):
        print('No dices to pick!')

    def _print_wrongdice(self):
        print('You can\'t pick this dice')

    def _print_won(self):
        print('CONGRATS! YOU WON!')

    def _print_gameend(self):
        print('Game alrady end')
