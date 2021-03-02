import curses
import UILayer.uiBlocks as uiBlocks


class LoginScreen: # Sigurjón Ingi
    """ Class for the login screen where it all starts"""
    
    def __init__(self, controller, dirStr: str) -> None:
        self.controller = controller
        self.dirStr = dirStr
        self.stdscr = controller.stdscr
        self.stdscr.clear()
        uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)

    def show(self):
        """ Shows the begining of the system"""
        menuItems = ["BOT", "USER", "Quit"]
        selected = None
        while selected != "Quit":
            self.stdscr.clear()
            uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
            selected = uiBlocks.uiBlocks.selectorBox(self.stdscr, menuItems)
            if selected == "BOT":
                self.controller.user = 0
                self.controller.menuMain(self.dirStr)
            elif selected == "USER":
                self.controller.user = 0
                self.controller.menuMain(self.dirStr)
        else:
            return 0

