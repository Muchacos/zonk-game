class PlayerMeta:
    """Представляет родительский класс игрока.

    Методы подклассов:
    get_dicechoose -- получает ввод от игрока с выбранными костями
    get_actchoice -- получает ввод от игрока с информацией, хочет ли он
                     продолжить/закончить ход или выбрать другие кости

    """

    gm = None
    screen = None

    def __init__(self, game_mode, screen, name):
        PlayerMeta.gm = game_mode
        PlayerMeta.screen = screen
        self.name = name
        self.score_total = 0
        self.score_turn = 0
        self.score_pick = 0

    def add_scoretotal(self):
        self.score_total += self.score_turn
        self.score_turn = 0
        PlayerMeta.screen.display_score(self, "turn")  # удаление очков с экрана
        PlayerMeta.screen.display_score(self, "total")

    def add_scoreturn(self):
        self.score_turn += self.score_pick
        self.score_pick = 0
        PlayerMeta.screen.display_score(self, "pick")  # удаление очков с экрана
        PlayerMeta.screen.display_score(self, "turn")

    def add_scorepick(self, score):
        self.score_pick += score
        PlayerMeta.screen.display_score(self, "pick")

    def clear_scoreturn(self):
        self.score_turn = 0
        PlayerMeta.screen.display_score(self, "turn")

    def clear_scorepick(self):
        self.score_pick = 0
        PlayerMeta.screen.display_score(self, "pick")
