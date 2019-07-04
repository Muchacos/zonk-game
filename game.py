from classes import Player, Game

print('Welcome to the game! First player, what is your name?')
p1 = Player(1, input())
print('And his friend, what is your name?')
p2 = Player(2, input())
print('Ok... let me write it down... yep.\nNow, choose a maximum fo points.')
game_mode = Game(int(input()), p1, p2)
print('Great, we can start!')
print('------------------------------')
print('Rule: to roll a dices, print \'r\'')

while game_mode.game_flag:
    print('------------------------------')
    print(game_mode.curr_player.name, ', your Turn!')
    inp = input()
    while inp != 'r':
        inp = input()
    else:
        game_mode.turn()
