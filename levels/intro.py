import data


def run(screen):
    screen.init_zones()
    screen.display_msg("01_hello")

    while True:
        screen.display_msg("02_0_getname", wait=False)
        name = screen.input_str()
        if len(name) == 0:
            screen.display_msg("02_2_stdname")
            name = "Человек"
            break
        elif len(name) <= 6 and len(name) >= 3:
            break
        else:
            screen.display_msg("02_1_badname",
                               delay=data.TIMINGS["DELAY-ERR"])
    data.PLAYER_NAME = name
