"""Функции этого модуля упрощают работу над игровой механикой."""
import random as r

import data


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


def cheat_good_dices(amount_of_dices, *, clear=None):
    """Возвращает хорошие кости (непроигрышные или все, приносящие очки)."""
    if clear is None:
        if chance(r.randint(10, 50)):
            clear = True
        else:
            clear = False

    if clear is True or amount_of_dices == 1:
        possible_dices = data.DICES_CLEAR_COMBOS[amount_of_dices]
        return r.choice(possible_dices)
    else:
        while True:
            result = [r.randint(1, 6) for i in range(amount_of_dices)]
            if (check_combos_any(result) is True and
               result not in data.DICES_CLEAR_COMBOS[amount_of_dices]):
                return result


def cheat_bad_dices(amount_of_dices, loose=True):
    """Возвращает только плохие кости (одна пятерка или абсолютно ничего)."""
    while True:
        result = [r.choice([2, 3, 4, 6]) for i in range(amount_of_dices)]
        if check_combos_any(result) is False:
            if loose is False and len(result) != 1:
                result[0] = 5
            return result
