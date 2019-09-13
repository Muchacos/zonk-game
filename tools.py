"""Функции этого модуля упрощают работу над игровой механикой."""
import random as r



def chance(chance):
    """Возвращает True с заданным шансом."""
    if chance >= 100:
        return True
    elif chance <= 0:
        return False

    a = [True for i in range(chance)]
    a.extend([False for i in range(100 - chance)])
    return r.choice(a)


def exclude_array(base, exclusion):
    """Возвращает массив base, исключая из него массив exclusion."""
    out = base[:]
    for ex in exclusion:
        out.remove(ex)
    return out


def check_combos_row(dices):
    """Возвращает True, если среди костей есть >= три одинаковых кости."""
    return any(dices.count(d) >= 3 for d in dices)


def check_combos_range(dices):
    """Возвращает True, если среди костей есть все кости от 1 до 5."""
    return all(d in dices for d in range(1, 6))


def check_combos_single(dices):
    """Возвращает True, если среди костей есть кость 1 или 5."""
    return any(d in dices for d in (1, 5))


def check_combos_any(dices):
    """Возвращает True, если среди костей есть хотя бы одна комбинация."""
    return any([check_combos_row(dices), check_combos_single(dices)])

