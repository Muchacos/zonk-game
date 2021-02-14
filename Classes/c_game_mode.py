import data
import tools as t


class GameMode:
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
        GameMode.screen = screen
        GameMode.colorist = colorist
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
        GameMode.screen.anim_playerhl(self)

    def check_win(self):
        """Возвращает True, если игрок выйграл."""
        return self.player.score_total >= self.high_bar

    def restore_dices(self):
        """Добавляет недостающие кости."""
        self.dices.extend([1] * (6 - len(self.dices)))

    def action(self, embed_funcs, event_msgs):
        """Производит основное игровое событие."""
        def run_embed(key, *args, **kwargs):
            return embed_funcs[key](*args, **kwargs)

        def display_event_msg(event_key, *args, **kwargs):
            if event_key in event_msgs.keys():
                scr.display_msg(event_msgs[event_key], *args, **kwargs)

        scr = self.screen
        player = self.player
        colorist = GameMode.colorist
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
