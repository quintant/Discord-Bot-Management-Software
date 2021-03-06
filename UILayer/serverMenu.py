import curses
import UILayer.uiBlocks as uiBlocks


class ServerMenu: #Sigurjón Ingi
    """ Class for the server menu"""

    def __init__(self, controller, dirStr: str) -> None:
        self.controller = controller
        self.user = controller.user
        self.dirStr = dirStr + "/SeverMenu"
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
            if selected != -1:
                self.stdscr.clear()
                uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
                Selection = [f"View {selected[1]}", "Retry", "Back"]
                sel = uiBlocks.uiBlocks.selectorBox(self.stdscr, Selection)
                if sel == Selection[2]:
                    break
                elif sel == Selection[0]:
                    self.selectedServer(selected[0])
                selected = None

        else:
            return 0

    def selectedServer(self, server):
        menuItems = [
            "Members",
            "Details",
            "Back"
        ]
        selected = None
        DIRSTR = f"/{server.name}"
        self.dirStr += DIRSTR
        while selected != "Back":
            self.stdscr.clear()
            uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
            selected = uiBlocks.uiBlocks.selectorBox(self.stdscr, menuItems)
            if selected == "Members":
                self.controller.listMembers(self.dirStr, server)


        self.dirStr = self.dirStr[:-len(DIRSTR)]