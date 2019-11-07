"""Тут содержатся все классы, составляющие основу игровой логики."""
import curses
import random as r

import data
import tools as t


#   .d8888b.         d8888  888b     d888  8888888888
#  d88P  Y88b       d88888  8888b   d8888  888
#  888    888      d88P888  88888b.d88888  888
#  888            d88P 888  888Y88888P888  8888888
#  888  88888    d88P  888  888 Y888P 888  888
#  888    888   d88P   888  888  Y8P  888  888
#  Y88b  d88P  d8888888888  888   "   888  888
#   "Y8888P88 d88P     888  888       888  8888888888
#
class Game:
    """Представляет основной функционал игры.

    Термины:
    Ход (turn) -- событие, происходящее, пока игрок совершает действия (action)
    Действие (action) -- основное игровое событие
    Очки для победы (high_bar) -- значение, указывающее, сколько итоговых
                                  очков необходимо набрать для победы.

    Поля:
    dices -- список, содержащий от 1 до 6 игральных костей
    player -- текущий игрок
    screen -- экран игры
    high_bar -- значение очков, необходимых для победы
    game_flag -- булевая переменная, указывающаяя может ли продолжаться игра
    second_player -- второй (предыдущий/следующий) игрок

    """

    screen = None
    colorist = None

    def __init__(self, screen, colorist):
        Game.screen = screen
        Game.colorist = colorist
        self.game_flag = True
        self.dices = [1] * 6
        self.temp_dices = []

    def set_settings(self, high_bar, player, enemy):
        """Устанавливает игроков и high_bar."""
        self.player = player
        self.high_bar = high_bar
        self.second_player = enemy

    def switch_player(self):
        """Меняет игроков местами."""
        self.player, self.second_player = self.second_player, self.player
        Game.screen.anim_playerhl(self)

    def check_win(self):
        """Возвращает True, если игрок выйграл."""
        return self.player.score_total >= self.high_bar

    def restore_dices(self):
        """Добавляет недостающие кости."""
        self.dices.extend([1] * (6 - len(self.dices)))

    #                      888     d8b
    #                      888     Y8P
    #                      888
    #   8888b.    .d8888b  888888  888   .d88b.   88888b.
    #      "88b  d88P"     888     888  d88""88b  888 "88b
    #  .d888888  888       888     888  888  888  888  888
    #  888  888  Y88b.     Y88b.   888  Y88..88P  888  888
    #  "Y888888   "Y8888P   "Y888  888   "Y88P"   888  888
    #
    def action(self, embed_funcs, event_msgs):
        """Производит основное игровое событие."""
        def run_embed(key, *args, **kwargs):
            return embed_funcs[key](*args, **kwargs)

        def display_event_msg(event_key, *args, **kwargs):
            if event_key in event_msgs.keys():
                scr.display_msg(event_msgs[event_key], *args, **kwargs)

        scr = self.screen
        player = self.player
        colorist = Game.colorist
        is_human = player.type == "Human"

        run_embed("anim_diceroll", len(self.dices))
        if is_human:
            self.dices = run_embed("get_human_dices", self)
        else:
            self.dices = run_embed("get_robot_dices", self)
        run_embed("display_dices", self.dices)

        if not t.has_anycombo(self.dices):
            display_event_msg("nocombos")
            scr.clear_zone(scr.ZONE_DICES)
            player.clear_scoreturn()
            self.restore_dices()
            self.switch_player()
            return 0

        act_choice = data.KEYCODES["TURN_CANCEL"]
        while act_choice == data.KEYCODES["TURN_CANCEL"]:
            if is_human:
                player.clear_scorepick()  # FIXME: вроде кривовато
                display_event_msg("getpick", wait=False)
            pick = player.get_dicechoose()
            pick_score, pick_bad_dices = t.dices_info(pick).values()
            pick_good_dices = t.exclude_array(pick, pick_bad_dices)

            if pick_score == 0:
                scr.effect_hldices(pick, cp=colorist.red)
                display_event_msg("badallpick", player.name)
                scr.effect_hldices()
                continue

            player.add_scorepick(pick_score)
            scr.effect_hldices(pick_good_dices)
            if pick_bad_dices:
                scr.effect_hldices(pick_bad_dices, cp=colorist.red)
                display_event_msg("badpick")

            if is_human:
                display_event_msg("actchoice", wait=False, speedup=2)
            act_choice = player.get_actchoice()
            if not is_human:  # FIXME: криво сделано
                if act_choice == data.KEYCODES["TURN_END"]:
                    scr.display_msg("a_robturnF")  # FIXME
                else:
                    scr.display_msg("a_robturnT")  # FIXME
            scr.effect_hldices()

        self.dices = t.exclude_array(self.dices, pick_good_dices)
        scr.effect_hldices(pick_good_dices, cp=colorist.none)
        player.add_scoreturn()
        if is_human:
            display_event_msg("h_scrpick", player.name, pick_score)
        else:
            display_event_msg("r_scrpick", player.name, pick_score)

        if act_choice == data.KEYCODES["TURN_END"]:
            player.add_scoretotal()
            if is_human:
                display_event_msg("h_scrtotl", player.name, player.score_total)
            else:
                display_event_msg("r_scrtotl", player.name, player.score_total)
            scr.clear_zone(scr.ZONE_DICES)
            if self.check_win():
                self.game_flag = False
                self.restore_dices()
                return 0
            self.restore_dices()
            self.switch_player()
            display_event_msg("whoturn", self.player.name, delay=1)
        elif len(self.dices) == 0:
            self.restore_dices()


#   .d8888b.   .d8888b.  888    .d8888b.  8888888b.  88888  .d8888b.  888888888
#  d88P  Y88b d88P""Y88b 888   d88P""Y88b 888   Y88b  888  d88P  Y88b    888
#  888    888 888    888 888   888    888 888    888  888  Y88b.         888
#  888        888    888 888   888    888 888   d88P  888   "Y888b.      888
#  888        888    888 888   888    888 8888888P"   888      "Y88b.    888
#  888    888 888    888 888   888    888 888 T88b    888        "888    888
#  Y88b  d88P Y88b..d88P 888   Y88b..d88P 888  T88b   888  Y88b  d88P    888
#   "Y8888P"   "Y8888P"  888888 "Y8888P"  888   T88b 88888  "Y8888P"     888
#
class Colorist:
    """Представляет менеджера, отвечающего за работу с цветами.

    Поля:
    *PALETTE_NAME* -- цветовая палитра с индексами цветовых пар, где:
                      [0] - белый, [1] - пустота, [2] - голубой, [3] - красный;
                      [4] - фон, [5] - светлая тень, [6] - темная тень,
                      [7] - светлая граница.

    screen -- экземпляр соответсвующего класса
    current_palette -- текущая цветовая палитра
    *pairname* -- индекс цветовой пары, представляющей на данный момент
                  указанный цвет. Проще говоря, ссылки на пары в палитре.
    """

    FAST_SPRINT = (20, 21, 22, 23, 24, 25, 26, 27)
    FIRST_LEVEL = (1, 2, 3, 4, 30, 31, 32, 1)

    def __init__(self, screen):
        Colorist.screen = screen
        curses.start_color()
        curses.use_default_colors()
        self.init_colors()
        self.init_pairs()
        self.change_palette(self.FAST_SPRINT)

    def change_palette(self, palette):
        """Изменяет текущую палитру вместе с ссылками на ее цвета"""
        self.current_palette = palette
        self.white = palette[0]
        self.none = palette[1]
        self.blue = palette[2]
        self.red = palette[3]
        self.bkgd = palette[4]
        self.bkgd_ltshadow = palette[5]
        self.bkgd_dkshadow = palette[6]
        self.bkgd_ltborder = palette[7]
        Colorist.screen.stdscr.bkgdset(" ", curses.color_pair(self.white))

    def convert_color(self, *channels):
        """Конвертирует цвет из формата 0-255 в формат 0-1000."""
        return [round(ch / 255 * 1000 + 0.5) for ch in channels]

    def init_color(self, id, r, g, b):
        """Создает цвет, переводя его в формат, пригодный для curses."""
        converted_color = self.convert_color(r, g, b)
        curses.init_color(id, *converted_color)

    def init_fade_colors(self, id_start, k, c0_id, c1_id):
        """Создает k промежуточных цветов между цветами c0 и c1."""
        c0 = curses.color_content(c0_id)
        c1 = curses.color_content(c1_id)
        for i in range(1, k + 1):
            new_color = []
            for ch in range(3):  # channel
                new_ch = round(i / (k + 1) * (c1[ch] - c0[ch])) + c0[ch]
                new_color.append(new_ch)
            curses.init_color(id_start + i - 1, *new_color)

    def init_fade_pairs(self, id_start, fore0, fore1, back0, back1):
        """Создает цветовые пары, объединяя диапазоны fore0-1 и back0-1."""
        if fore0 == fore1:
            k = (back1 - back0 + 1)
            fore_ids = [fore0] * k
        else:
            k = (fore1 - fore0 + 1)
            fore_ids = range(fore0, fore1 + 1)
        if back0 == back1:
            back_ids = [back0] * k
        else:
            back_ids = range(back0, back1 + 1)

        for i in range(k):
            curses.init_pair(id_start + i, fore_ids[i], back_ids[i])

    def init_colors(self):
        """Создание используемых цветов."""
        self.init_color(16, 0, 0, 0)  # черный
        self.init_color(3, 51, 204, 255)  # ярко-голубой (выделение)

        # быстрый забег
        self.init_color(30, 165, 202, 246)  # точки фона
        self.init_color(31, 0, 70, 140)  # точки светлой тени
        self.init_color(32, 0, 39, 78)  # точки темной тени
        self.init_color(33, 8, 28, 69)  # фон
        self.init_color(34, 1, 10, 35)  # фон светлой тени
        self.init_color(35, 0, 6, 21)  # фон зоны (темной тени)

        # первый уровень
        self.init_color(40, 0, 108, 217)  # точки фона
        self.init_color(41, 0, 70, 140)  # точки светлой тени
        self.init_color(42, 0, 39, 78)  # точки темной тени

        # промежуточные цвета перехода к первому уровню
        self.init_fade_colors(70, 3, 30, 40)  # точки фона
        self.init_fade_colors(73, 3, 31, 41)  # точки светлой тени
        self.init_fade_colors(76, 3, 32, 42)  # точки темной тени
        self.init_fade_colors(79, 3, 33, 16)  # фон
        self.init_fade_colors(82, 3, 34, 16)  # фон светлой тени
        self.init_fade_colors(85, 3, 35, 16)  # фон зоны (темной тени)

    def init_pairs(self):
        """Создание цветовых пар."""
        # стандартные цвета \ первый уровень
        curses.init_pair(1, 15, 16)  # белый
        curses.init_pair(2, 16, 16)  # пустота
        curses.init_pair(3, 39, 16)  # голубой
        curses.init_pair(4, 12, 16)  # красный
        curses.init_pair(5, 16, 15)  # ченрый на белом
        curses.init_pair(204, 201, 15)  # ярко-фиолетовый (цвет для ошибок)

        # быстрый забег
        curses.init_pair(20, 15, 35)  # белый
        curses.init_pair(21, 35, 35)  # пустота
        curses.init_pair(22, 3, 35)   # голубой
        curses.init_pair(23, 12, 35)  # красный

        curses.init_pair(24, 30, 33)  # фон
        curses.init_pair(25, 31, 34)  # светлая тень
        curses.init_pair(26, 32, 35)  # темная тень
        curses.init_pair(27, 15, 34)  # светлая граница

        # первый уровень (интерфейс)
        curses.init_pair(30, 40, 16)  # фон
        curses.init_pair(31, 41, 16)  # светлая тень
        curses.init_pair(32, 42, 16)  # темная тень

        # переход к первому уровню
        self.init_fade_pairs(40, 15, 15, 85, 87)  # белый
        self.init_fade_pairs(43, 70, 72, 79, 81)  # фон
        self.init_fade_pairs(46, 73, 75, 82, 84)  # светлая тень
        self.init_fade_pairs(49, 76, 78, 85, 87)  # темная тень


#  8888888b.   888             d8888  Y88b   d88P  8888888888  8888888b.
#  888   Y88b  888            d88888   Y88b d88P   888         888   Y88b
#  888    888  888           d88P888    Y88o88P    888         888    888
#  888   d88P  888          d88P 888     Y888P     8888888     888   d88P
#  8888888P"   888         d88P  888      888      888         8888888P"
#  888         888        d88P   888      888      888         888 T88b
#  888         888       d8888888888      888      888         888  T88b
#  888         88888888 d88P     888      888      8888888888  888   T88b
#
class Player:
    """Представляет родительский класс игрока.

    Методы подклассов:
    get_dicechoose -- получает ввод от игрока с выбранными костями
    get_actchoice -- получает ввод от игрока с информацией, хочет ли он
                     продолжить/закончить ход или выбрать другие кости

    """

    gm = None
    screen = None

    def __init__(self, game_mode, screen, name):
        Player.gm = game_mode
        Player.screen = screen
        self.name = name
        self.score_total = 0
        self.score_turn = 0
        self.score_pick = 0

    def add_scoretotal(self):
        self.score_total += self.score_turn
        self.score_turn = 0
        Player.screen.display_score(self, "turn")  # удаление очков с экрана
        Player.screen.display_score(self, "total")

    def add_scoreturn(self):
        self.score_turn += self.score_pick
        self.score_pick = 0
        Player.screen.display_score(self, "pick")  # удаление очков с экрана
        Player.screen.display_score(self, "turn")

    def add_scorepick(self, score):
        self.score_pick += score
        Player.screen.display_score(self, "pick")

    def clear_scoreturn(self):
        self.score_turn = 0
        Player.screen.display_score(self, "turn")

    def clear_scorepick(self):
        self.score_pick = 0
        Player.screen.display_score(self, "pick")


#  888    888  888     888  888b     d888         d8888  888b    888
#  888    888  888     888  8888b   d8888        d88888  8888b   888
#  888    888  888     888  88888b.d88888       d88P888  88888b  888
#  8888888888  888     888  888Y88888P888      d88P 888  888Y88b 888
#  888    888  888     888  888 Y888P 888     d88P  888  888 Y88b888
#  888    888  888     888  888  Y8P  888    d88P   888  888  Y88888
#  888    888  Y88b. .d88P  888   "   888   d8888888888  888   Y8888
#  888    888   "Y88888P"   888       888  d88P     888  888    Y888
#
class Human(Player):
    """Представляет игрока по ту сторону экрана."""

    type = "Human"

    def get_dicechoose(self):
        dices = Player.gm.dices
        screen = Player.screen
        while True:
            inp = screen.input_str()
            # Проверка, есть ли все выбранные кости среди выпавших костей
            if (inp.isdigit() and
               all(inp.count(d) <= dices.count(int(d)) for d in inp)):
                return [int(d) for d in inp]
            else:
                pass  # FIXME: нужно сделать вывод сообщения об ошибке

    def get_actchoice(self):
        screen = Player.screen
        while True:
            inp = screen.input_str()
            if inp in data.KEYCODES.values():
                return inp
            else:
                pass  # FIXME: нужно сделать вывод сообщения об ошибке


#  8888888b.    .d88888b.   888888b.     .d88888b.  88888888888
#  888   Y88b  d88P" "Y88b  888  "88b   d88P" "Y88b     888
#  888    888  888     888  888  .88P   888     888     888
#  888   d88P  888     888  8888888K.   888     888     888
#  8888888P"   888     888  888  "Y88b  888     888     888
#  888 T88b    888     888  888    888  888     888     888
#  888  T88b   Y88b. .d88P  888   d88P  Y88b. .d88P     888
#  888   T88b   "Y88888P"   8888888P"    "Y88888P"      888
#
class RobotMeta(Player):
    """Представляет базовый класс Роботов.

    Поля:
    claw -- клешня робота, в которой он хранит выбранные кости
    dices_for_pick -- копия списка с выпавшими костями. Ее использование
                      освобождает от передачи списка dices как аргумента в
                      функции take_*
    thinking -- булевая переменная, определяющая, будет ли робот думать,
                задерживая свой ход

    """

    type = "Robot"

    def __init__(self, game_mode, screen, name, thinking=False):
        Player.__init__(self, game_mode, screen, name)
        self.claw = []
        self.dices_for_pick = []
        self.thinking = thinking

    def take_range(self):
        """Забирает в claw наибольший диапазон костей."""
        claw = self.claw
        dices = self.dices_for_pick
        if 6 in dices:
            claw.extend(range(1, 7))
            dices.clear()
        else:
            for d in range(1, 6):
                claw.append(d)
                dices.remove(d)

    def take_row(self):
        """Забирает в claw ряд(ы) костей."""
        claw = self.claw
        dices = self.dices_for_pick[:]
        for d in dices:
            if dices.count(d) >= 3:
                claw.append(d)
                self.dices_for_pick.remove(d)

    def take_single(self, amount=4):
        """Забирает в claw единичные кости, где amount - количество."""
        claw = self.claw
        dices = self.dices_for_pick
        # По умолчанию amount = 4, т.к. это максимальное число единичных косей
        for i in (1, 5):  # Сначала забираются кости со значением "1"
            for d in dices[:]:
                if amount == 0:
                    break
                if d == i:
                    claw.append(d)
                    dices.remove(d)
                    amount -= 1

    def rowcombo_dice(self):
        """Возвращает значение костей, образующих комбо 'row'."""
        dices = self.dices_for_pick
        out = []
        for d in dices:
            if dices.count(d) >= 3 and d not in out:
                out.append(d)
        return out


class RobotRandom(RobotMeta):
    """Представляет робота, полагающегося на случайность."""

    def get_dicechoose(self):
        gm = Player.gm
        self.claw = []
        self.dices_for_pick = gm.dices[:]
        dices = self.dices_for_pick
        ones, fives = dices.count(1), dices.count(5)

        if t.has_rangecombo(dices):
            if t.chance(37):
                self.take_range()
                if ones + fives > 2 and t.chance(40):
                    self.take_single()
            elif ones + fives > 2 and t.chance(65):
                self.take_single()
            else:
                self.take_single(r.choice([1, 2]))

        elif t.has_rowcombo(dices):
            # Если костей два ряда, то забираем оба с шансом 90%
            if len(self.rowcombo_dice()) > 1 and t.chance(90):
                self.take_row()
            else:
                row_dice = self.rowcombo_dice()[0]
                # Вместо ряда забираем единичные кости, если ряд состоит из них
                if ((row_dice == 1 and fives != 0 and t.chance(36))
                   or (row_dice == 5 and ones != 0 and t.chance(40))):
                    self.take_single(2)
                elif row_dice not in (1, 5):
                    self.take_row()
                    # Забираем ещи и единичные с шансом 40%
                    if ones + fives > 0 and t.chance(40):
                        self.take_single()
                else:
                    self.take_row()

        # Если остались единичные и мы брали кости
        if t.has_singlecombo(dices) and len(self.claw) != 0:
            # Если все оставшиеся кости - единичные
            if len(dices) == ones + fives:
                if t.chance(84):  # То берем их все с шансом 84%
                    self.take_single()
                else:  # Либо забираем их случайное количество (но не все)
                    self.take_single(r.choice(range(1, len(dices))))
            elif ones + fives > 2 and t.chance(50):
                self.take_single(2)
            elif t.chance(50):
                self.take_single(1)

        if len(self.claw) == 0:
            if len(dices) == ones + fives:
                if len(dices) == 1 or t.chance(84):
                    self.take_single()
                else:
                    self.take_single(r.choice(range(1, len(dices))))
            # Забираем 3/2/1/все единичные кости по условиям
            elif ones + fives == 4 and t.chance(73):
                self.take_single(3)
            elif ones + fives > 2 and t.chance(52):
                self.take_single(2)
            elif t.chance(31):
                self.take_single(1)
            else:
                self.take_single()

        if self.thinking is True:
            delay = (r.uniform(0.7, 1.5) + len(dices) / 10) * -1
            Player.screen.display_msg("a_robthink", delay=delay)
        return self.claw

    def get_actchoice(self):
        gm = Player.gm
        dices = gm.dices
        n_dices = len(dices)
        chance_to_continue = 0

        if n_dices == 0:
            chance_to_continue = 93
        elif n_dices in (4, 5):
            chance_to_continue = r.randint(70, 90)
        elif n_dices == 3:
            chance_to_continue = r.randint(60, 70)
        elif n_dices == 2:
            chance_to_continue = r.randint(20, 50)
        else:
            chance_to_continue = r.randint(10, 30)

        scores = self.score_pick + self.score_turn + self.score_total
        if scores >= gm.high_bar:
            chance_to_continue = r.randint(1, 10)
        elif scores >= gm.second_player.score_total:
            chance_to_continue += r.randint(9, 24)

        turn_score = self.score_pick + self.score_turn
        if turn_score >= r.randint(700, 1000):
            chance_to_continue -= r.randint(21, 39)
        elif turn_score >= r.randint(300, 600):
            chance_to_continue -= r.randint(15, 21)
        else:
            chance_to_continue += r.randint(10, 40)

        choice = t.chance(chance_to_continue)
        if choice is True:
            return data.KEYCODES["TURN_CONTINUE"]
        else:
            return data.KEYCODES["TURN_END"]


class RobotTactic(RobotMeta):
    """Представляет робота-тактика."""

    def get_dicechoose(self):
        gm = Player.gm
        self.dices_for_pick = gm.dices[:]
        self.claw = []
        dices = self.dices_for_pick
        singles = dices.count(1) + dices.count(5)

        if t.has_rangecombo(dices):
            self.take_range()
            if t.has_singlecombo(dices):
                self.take_single()

        elif t.has_rowcombo(dices):
            self.take_row()
            if t.has_singlecombo(dices) and t.chance(25):
                self.take_single()

        # Забирам все единичные кости, если остались только они
        elif singles == len(dices):
            self.take_single()

        # Если костей больше трех, то забираем одну с шансом 75% или все
        elif len(dices) > 3:
            if t.chance(75) or singles == 1:
                self.take_single(1)
            else:
                self.take_single()

        # Если кости три или меньше, то забираем все с шансом 75% или одну
        elif len(dices) <= 3:
            if singles > 1 and t.chance(75):
                self.take_single()
            else:
                self.take_single(1)

        # Забираем единичные кости, если таковые остались и принесут победу
        possible_points = t.dices_info(dices)["score"]
        if (t.has_singlecombo(dices) and possible_points +
           self.score_turn + self.score_total >= gm.high_bar):
            self.take_single()

        if self.thinking is True:
            delay = (r.uniform(0.7, 1.5) + len(dices) / 10) * -1
            Player.screen.display_msg("a_robthink", delay=delay)
        return self.claw

    def get_actchoice(self):
        def chance_curve(x):
            """Возвращает шанс продолжить ход, вычисляемый функцией 'y'."""
            # x - кол-во очков, y - шанс
            if x < 200:
                y = 100
            elif x > 1800:
                y = 0
            else:
                y = round(-2.5 * (x - 200)**(1 / 2) + 100)
            return y

        dices = Player.gm.dices
        n_dices = len(dices)
        chance_to_continue = chance_curve(self.score_turn)

        # Нюансы, увеличивающие или уменьшающие шанс продолжить ход
        if (self.score_total + self.score_turn
           + self.score_pick >= Player.gm.high_bar):
            chance_to_continue = 0
        elif n_dices == 0:
            chance_to_continue += 90
        elif n_dices == 5:
            chance_to_continue += 30
        elif n_dices < 3:
            chance_to_continue -= 30

        choice = t.chance(chance_to_continue)
        if choice is True:
            return data.KEYCODES["TURN_CONTINUE"]
        else:
            return data.KEYCODES["TURN_END"]
