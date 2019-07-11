''' Welcome to Zonk game! This is pre-alpha version,
everything you see is just a test. But thanks for bying!'''
import random
from collections import Counter
import re


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
    COMBOS = {'[1, 2, 3, 4, 5, 6]': 1500, '[1, 2, 3, 4, 5]': 750}

    def __init__(self):
        pass

    def set_settings(self, settings, printer):
        self.player = settings['player']
        self.high_bar = settings['high_bar']
        self.printer = printer

    def check_win(self):
        if self.player.score >= self.high_bar:
            Game.game_flag = False
            self.printer._print_won()

    def check_turn(self):
        dices = Game.dices
        flags = [False]*3

        flags[0] = any(dice in (1, 5) for dice in dices)
        flags[1] = Counter(dices).most_common()[0][1] >= 3
        flags[2] = str(dices.sort()) in Game.COMBOS
        return any(flags)

    def add_dices(self):
        Game.dices.extend([1]*(6 - len(Game.dices)))

    def turn(self):
        printer = self.printer
        player = self.player

        if Game.game_flag is False:
            printer._print_gameend()
            return False

        for i in range(len(Game.dices)):
            Game.dices[i] = random.randint(1, 6)

        printer._print_dices(Game.dices)

        if self.check_turn() is False:
            printer._print_nodices()
            self.player.remove_scoreturn()
            return False

        while True:
            hand = printer.get_dicechoose()
            curr_score = 0

            if len(hand) >= 3 and all(dice == hand[0] for dice in hand):
                k = 0
                for dice in hand:
                    if k == 0 and dice == 1:
                        curr_score += 1000
                    elif k == 0:
                        curr_score += dice*100
                    elif k > 3:
                        curr_score *= 2
                    k += 1
                    Game.dices.remove(dice)
                break

            elif len(hand) in range(1, 4) and all(dice in (1, 5) for dice in hand):
                for dice in hand:

                    if dice == 0:
                        printer._print_scoreturn()
                        self.player.add_scoretotal()
                        printer._print_scoretotal()
                        self.check_win()
                        return False

                    elif dice == 1:
                        curr_score += 100
                        Game.dices.remove(dice)

                    elif dice == 5:
                        curr_score += 50
                        Game.dices.remove(dice)
                break

            elif str(hand.sort()) in Game.COMBOS:
                curr_score += COMBOS[hand]
                for dice in hand:
                    Game.dices.remove(dice)
                break

            else:
                curr_score = 0
                printer._print_wrongdice()

        player.add_scoreturn(curr_score)
        printer._print_scoreearned(curr_score)
        printer._print_scoreturn()

        if printer.get_nextturn() is False:
            self.player.add_scoretotal()
            printer._print_scoretotal()
            self.check_win()
            return False
        else:
            return True


class Printer:

    def __init__(self, game_mode):
        self.game_mode = game_mode

    def get_settings(self):
        print('Welcome to the game! What is your name?')
        p = Player(input())
        print('Ok... let me write it down... yep.\nNow, choose a maximum fo points.')
        high_bar = int(input())
        print('Great, we can start!')
        settings = {'player': p, 'high_bar': high_bar}
        return settings

    def get_dicechoose(self):
        dices = self.game_mode.dices
        while True:
            inp = input('> ')
            if inp.isdigit() and all(inp.count(dice) <= dices.count(int(dice)) for dice in inp):
                return [int(dice) for dice in inp]
            else:
                self._print_wrongdice()

    def get_nextturn(self):
        print('\nContunue?')
        while True:
            inp = input('> ')

            if inp == 'n':
                return False
            elif inp == 'y':
                return True
            else:
                print('Wrong answer')

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
        print('No dices to pick!\n')
        print('-------------------------------')

    def _print_wrongdice(self):
        print('You can\'t pick this/those dice(s)!')

    def _print_won(self):
        print('CONGRATS! YOU WON!')

    def _print_gameend(self):
        print('Game alrady end')
