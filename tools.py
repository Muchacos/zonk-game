"""Функции этого модуля упрощают создание игровой механики."""
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
    out = base.copy()
    for ex in exclusion:
        out.remove(ex)
    return out


def has_rowcombo(dices):
    """Возвращает True, если среди костей есть >= три одинаковых кости."""
    return any(dices.count(d) >= 3 for d in dices)


def has_rangecombo(dices):
    """Возвращает True, если среди костей есть все кости от 1 до 5."""
    return all(d in dices for d in range(1, 6))


def has_singlecombo(dices):
    """Возвращает True, если среди костей есть кость 1 или 5."""
    return any(d in dices for d in (1, 5))


def has_anycombo(dices):
    """Возвращает True, если среди костей есть хотя бы одна комбинация."""
    return has_singlecombo(dices) or has_rowcombo(dices)


def rand_dices(amount_of_dices):
    """Возвращает случайные кости."""
    return [r.randint(1, 6) for i in range(amount_of_dices)]


def good_dices(n_dices, *, clear=None):
    """Возвращает хорошие кости (непроигрышные или все, приносящие очки)."""
    if clear is None:
        if chance(r.randint(10, 60)):
            clear = True
        else:
            clear = False

    if clear or n_dices == 1:
        dices_list = data.DICES_CLEAR_COMBOS[n_dices]
        return r.choice(dices_list)
    else:
        while True:
            dices = rand_dices(n_dices)
            if (has_anycombo(dices) and
               dices not in data.DICES_CLEAR_COMBOS[n_dices]):
                return dices


def bad_dices(n_dices, *, onefive=False):
    """Возвращает только плохие кости (либо одну пятерку)."""
    while True:
        dices = [r.choice([2, 3, 4, 6]) for i in range(n_dices)]
        if has_anycombo(dices) is False:
            if onefive and n_dices != 1:
                dices[0] = 5
            return dices


def dices_info(dices):
    """Возвращает информацию о переданных костях в соответсвующем словаре."""
    score = 0
    dices = dices.copy()

    if has_rangecombo(dices):
        if 6 in dices:
            score += 1500
            dices.clear()
        else:
            score += 750
            for d in range(1, 6):
                dices.remove(d)

        for dice in dices[:]:
    if has_rowcombo(dices):
            loc_score = 0
            row_len = dices.count(dice)

            if row_len >= 3:
                if dice == 1:
                    loc_score += 1000
                else:
                    loc_score += dice * 100
                loc_score *= (row_len - 2)
                score += loc_score

                for i in range(row_len):
                    dices.remove(dice)

    if has_singlecombo(dices):
        for dice in dices[:]:
            if dice == 1:
                score += 100
                dices.remove(dice)

            elif dice == 5:
                score += 50
                dices.remove(dice)

    return {"score": score, "bad_dices": dices}
