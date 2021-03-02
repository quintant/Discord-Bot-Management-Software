import curses
import UILayer.uiBlocks as uiBlocks


class ServerMenu: #Sigurjón Ingi
    """ Class for the server menu"""

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
        for server in self.controller.bot.guilds:
            menuItems.append(
                [server,
                f"Name {server.name}",
                f"Members {server.member_count}",
                f"Owner {server.owner}",
                f"Region {server.region}"
                ])

        selected = None
        # while selected != "Back":
        while selected is None:
            self.stdscr.clear()
            uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
            selected = uiBlocks.uiBlocks.selectorBoxColumns(self.stdscr, menuItems)
            if selected != None:
                self.stdscr.clear()
                uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
                sel = uiBlocks.uiBlocks.selectorBox(self.stdscr, [f"View {selected[1]}", "Retry", "Back"])
                if sel == "Back":
                    break
                selected = None

        else:
            return 0
