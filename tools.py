"""Функции этого модуля упрощают работу над игровой механикой."""
import random as r


def randchance(chance):
    """Возвращает True с заданным шансом."""
    if chance >= 100:
        return True
    elif chance <= 0:
        return False

    a = [True for i in range(chance)]
    a.extend([False for i in range(100 - chance)])
    return r.choice(a)
