import random as r


def randchance(chance):
    '''Возвращает True с определенным шансом'''
    a = [True for i in range(chance)]
    a.extend([False for i in range(100 - chance)])
    return r.choice(a)
