import curses
import UILayer.uiBlocks as uiBlocks


class MembersMenu: #Sigurjón Ingi
    """ Class for the server menu"""

    def __init__(self, controller, dirStr: str) -> None:
        self.controller = controller
        self.user = controller.user
        self.dirStr = dirStr + "/MembersMenu"
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
                Selection = [f"View {selected[1]}", "Retry", "Back"]
                sel = uiBlocks.uiBlocks.selectorBox(self.stdscr, Selection)
                if sel == Selection[2]:
                    break
                elif sel == Selection[0]:
                    self.selectedServer(selected[0])
                selected = None

        else:
            return 0

    def membersList(self, guild):
        menuItems = []
        for member in guild.members:
            menuItems.append(
                [member,
                f"Name {member.display_name}",
                f"Members {member.name}",
                f"Owner {member.nick}",
                f"Region {member.top_role.name}"
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