# We desperately need a frontend, this will do for now
# IF USING AN IDE (PYCHARM OR SIMILAR) MAKE SURE TO ENABLE TERMINAL EMULATION IN RUN CONFIGURATION
import curses
import champ_identifier
import asyncio


########################################################################################################################
#                                                   Main Menu
########################################################################################################################
def print_menu(screen, highlight):
    # Color Pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Get terminal dimensions
    h, w = screen.getmaxyx()

    # Menu options
    menu = ['Rune Page Generator', 'Autopilot', 'Debug', 'Exit']

    # Print Title Text
    screen.clear()
    text = "EZ.GG Alpha v0.0"
    x = w//2 - len(text)//2
    y = h//2 - len(menu)//2
    screen.attron(curses.color_pair(3))
    screen.addstr(y, x, text)
    screen.attron(curses.color_pair(1))

    # Print Menu
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx + 1
        if idx == highlight:
            screen.attron(curses.color_pair(2))
            screen.addstr(y, x, row)
            screen.attron(curses.color_pair(1))
        else:
            screen.addstr(y, x, row)

    # Refresh
    screen.refresh()


########################################################################################################################
#                                                   Rune Generator Menu
########################################################################################################################
def print_rune_generator_menu(screen, text_pass):
    # Color Pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Get terminal dimensions
    h, w = screen.getmaxyx()

    # Print Title Text
    screen.clear()
    text = "EZ.GG Alpha v0.0 - Rune Generator"
    x = w // 2 - len(text) // 2
    y = h // 2
    screen.attron(curses.color_pair(3))
    screen.addstr(y, x, text)
    screen.attron(curses.color_pair(1))

    # Print Text Pass
    x = w // 2 - len(text_pass) // 2
    y = (h // 2) + 1
    screen.addstr(y, x, text_pass)

    # Refresh
    screen.refresh()


########################################################################################################################
#                                                   Driver Function
########################################################################################################################
def main(screen):
    # Color Pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Screen configuration
    curses.curs_set(0)

    # Set color scheme
    screen.attron(curses.color_pair(1))

    # Main Menu Start
    menu_exit = 0
    menu_index = 0
    while menu_exit == 0:
        print_menu(screen, menu_index)
        key = screen.getch()
        if key == curses.KEY_UP and menu_index > 0:
            menu_index -= 1
        elif key == curses.KEY_DOWN and menu_index < 3:
            menu_index += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Rune Generator Menu Start
            if menu_index == 0:
                print_rune_generator_menu(screen, "Waiting for champion lock in...")
                loop = asyncio.get_event_loop()
                loop.run_until_complete(champ_identifier.main())
                runes_menu_exit = 0
                while runes_menu_exit == 0:
                    print_rune_generator_menu(screen, "Runes set! Press ENTER to exit.")
                    key = screen.getch()
                    if key == curses.KEY_ENTER or key in [10, 13]:
                        runes_menu_exit = 1

            elif menu_index == 1:
                # Champselect
                break
            elif menu_index == 2:
                # Debug
                break
            elif menu_index == 3:
                menu_exit = 1


if __name__ == '__main__':
    curses.wrapper(main)
