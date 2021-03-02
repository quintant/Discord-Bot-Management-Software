import curses
import UILayer.uiBlocks as uiBlocks


class MainMenu: #Sigurjón Ingi
    """ Class for the main menu"""

    def __init__(self, controller, dirStr: str) -> None:
        self.controller = controller
        self.user = controller.user
        self.dirStr = dirStr + "/MainMenu"
        self.stdscr = controller.stdscr
        self.stdscr.clear()
        uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)

    def show(self):
        """ shows the main menu"""
        menuItems = []
        menuItems.append("Server list")
        menuItems.append("Bot info")
        menuItems.append("Log Out")
        selected = None
        while selected != "Log Out":
            self.stdscr.clear()
            uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
            selected = uiBlocks.uiBlocks.selectorBox(self.stdscr, menuItems)
            if selected == "Server list":
                self.controller.menuServer(self.dirStr)

        else:
            return 0

