import curses


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
