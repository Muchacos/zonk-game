from Levels.Part_I import scripts as s


def run(screen):
    s.interface_fade(screen)
    screen.display_msg_seq("uh_first_seq")
    screen.display_msg("empty", delay=-1.5)
    screen.display_msg("uh_try", speedup=0.2)
    screen.display_msg("uh_fortune")
    screen.display_msg("uh_laugh", delay=-1, speedup=0.8)
