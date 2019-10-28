import time

import data


def run(screen):
    time.sleep(1)
    screen.anim_paintui()
    time.sleep(1.2)
    screen.display_msg_seq("0_welcome_seq")
    screen.display_msg("0_playername", wait=False)

    long_count = 0
    short_count = 0
    none_count = 0

    for i in range(4):
        name = get_name(screen)

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

    screen.display_msg_seq("0_gameinfo_seq")
    screen.display_msg("0_rules1")
    screen.display_msg("0_rules2", data.PLAYER_NAME)


def get_name(screen):
    name = screen.input_str()
    if len(name) == 0:
        return None
    elif len(name) > 6:
        return "Long"
    elif len(name) < 3:
        return "Short"
    else:
        return name
