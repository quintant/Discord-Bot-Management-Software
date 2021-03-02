from UILayer.serverMenu import ServerMenu
from UILayer.mainMenu import MainMenu
from UILayer.loginScreen import LoginScreen

import curses


class UIController:  # Sigurjón Ingi
    """
    A class for controlling UI layer
    """

    def __init__(self, bot) -> None:
        from random import randint

        stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        #curses.resize_term(50, 200)  # Y,X
        stdscr.keypad(True)
        normal = 1
        logo = 2
        correct = 3
        error = 4
        table = 5
        # RED THEME
        curses.init_pair(table, 161, 0)
        curses.init_pair(normal, 161, 0)
        curses.init_pair(logo, 161, 0)
        curses.init_pair(correct, curses.COLOR_GREEN, 15)
        curses.init_pair(error, curses.COLOR_WHITE, curses.COLOR_RED )
        stdscr.bkgd(" ", curses.color_pair(normal))
        self.dirStr = "."
        self.stdscr = stdscr
        self.user = -1
        self.bot = bot

    def start(self):
        """
        A function for starting
        """
        screen = LoginScreen(self, self.dirStr)
        ex = screen.show()
        return ex

    def menuMain(self, dirStr):
        """
        A function for the menu
        """
        screen = MainMenu(self, dirStr)
        screen.show()

    def menuServer(self, dirStr):
        screen = ServerMenu(self, dirStr)
        screen.show()

    