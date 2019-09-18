import data


def run(screen):

    def get_name():
        name = screen.input_str()
        if len(name) == 0:
            return None
        elif len(name) > 6:
            return "Long"
        elif len(name) < 3:
            return "Short"
        else:
            return name

    screen.init_zones()
    screen.display_msg("0_welcomeintro")
    screen.display_msg("0_playername", wait=False)

    long_count = 0
    short_count = 0
    none_count = 0

    for i in range(4):
        name = get_name()

        if name not in [None, "Long", "Short"]:
            if long_count == 0 and short_count == 0 and none_count == 0:
                screen.display_msg("0_nicetomeet", name)
            else:
                screen.display_msg("0_oktomeet", name)
            break

        elif i == 3:
            continue

        elif name is None:
            if none_count == 0:
                screen.display_msg("0_naname1")
                screen.display_msg("0_naname1.1", wait=False)
            elif none_count == 1:
                screen.display_msg("0_naname2", wait=False)
            elif none_count == 2:
                screen.display_msg("0_naname3")
                screen.display_msg("0_naname3.1", wait=False)
            none_count += 1

        elif name == "Long":
            if long_count == 0:
                screen.display_msg("0_longname1")
                screen.display_msg("0_longname1.1", wait=False)
            elif long_count == 1:
                screen.display_msg("0_longname2", delay=1.5)
                screen.display_msg("0_longname2.1", wait=False)
            elif long_count == 2:
                screen.display_msg("0_longname3", wait=False)
            long_count += 1

        elif name == "Short":
            if short_count == 0:
                screen.display_msg("0_shortname1", wait=False)
            elif short_count == 1:
                screen.display_msg("0_shortname2", wait=False)
            elif short_count == 2:
                screen.display_msg("0_shortname3", wait=False)
            short_count += 1

    else:
        screen.display_msg("0_enougth", delay=1.5)
        screen.display_msg("0_stdname")

    if name not in [None, "Long", "Short"]:
        data.PLAYER_NAME = name

    screen.display_msg("0_lvlinfo1")
    screen.display_msg("0_lvlinfo2")
    screen.display_msg("0_lvlinfo3")

    screen.display_msg("0_aboutenemies", wait=False)
    input = screen.input_str()
    if input not in ("1", "0"):
        screen.display_msg("0_likeyes")
        input = "1"
    if input == "1":
        screen.display_msg("0_infoenemies1")
        screen.display_msg("0_infoenemies2", data.ROBOT_RANDOM_NAME)
        screen.display_msg("0_infoenemies3")
        screen.display_msg("0_infoenemies4", data.ROBOT_TACTIC_NAME)
        screen.display_msg("0_infoenemies5")
        screen.display_msg("0_infoenemies6", data.ROBOT_CALCULATOR_NAME)
        screen.display_msg("0_infoenemies7")
        screen.display_msg("0_infoenemies8")
        screen.display_msg("0_infoenemies9")
        screen.display_msg("0_infoenemies10")
    else:
        screen.display_msg("0_okno")
