''' Welcome to Zonk game! This is pre-alpha version,
everything you see is just a test. But thanks for bying!'''
import random


class Player:

    def __init__(self, id, name, points=0):
        self.id = id
        self.name = name
        self.points = points

    def sayhi(self):
        print('hi, my name is', self.name)


class Game:
    game_flag = True

    def __init__(self, high_bar, curr_player, pend_player):
        self.high_bar = high_bar
        self.curr_player = curr_player
        self.pend_player = pend_player

    def win_check(self):
        if self.curr_player.points >= self.high_bar:
            Game.game_flag = False
            print('++++++++++++++++++++++++++++++')
            print(self.curr_player.name, 'has won the game!')
            print(self.pend_player.name, ', you suck!')

    def turn(self):
        if Game.game_flag:
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            self.curr_player.points += d1 + d2
            print('Dices: %d %d | Total points: %d' % (d1, d2, self.curr_player.points))
            self.win_check()
            self.curr_player, self.pend_player = self.pend_player, self.curr_player
        else:
            print('The game is ended')
