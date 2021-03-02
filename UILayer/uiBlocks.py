"""
Class for creating various UI components including text boxes and
selector boxe
"""
import curses
from curses.textpad import Textbox, rectangle

normal = 1
logo = 2
correct = 3
error = 4
table = 5
# rows, cols = stdscr.getmaxyx()

class uiBlocks:
    def infoText(stdscr: curses.initscr, text: str, y_pos: int, x_pos: int):
        """ for making a Text Box in the system"""
        stdscr.refresh()
        stdscr.addstr(y_pos, x_pos, text, curses.color_pair(normal))
        stdscr.refresh()

    def infoTextRed(stdscr: curses.initscr, text: str, y_pos: int, x_pos: int):
        """ For making the text box RED WOW"""
        stdscr.refresh()
        stdscr.addstr(y_pos, x_pos, text, curses.color_pair(error))
        stdscr.refresh()

    def infoTextGreen(stdscr: curses.initscr, text: str, y_pos: int, x_pos: int):
        """ GREEN text box """
        stdscr.refresh()
        stdscr.addstr(y_pos, x_pos, text, curses.color_pair(correct))
        stdscr.refresh()

    def textField(stdscr: curses.initscr, label: str, y_pos: int = 9):
        """Create an text box for userinput, initialized with stdcr,
        label:str y_pos:int"""
        diff = len(label)
        screen_len = 100 - 3

        stdscr.addstr(y_pos, 1, label)

        editwin = curses.newwin(1, screen_len - diff, y_pos, diff + 2)
        rectangle(stdscr, y_pos - 1, len(label) + 1, y_pos + 1, 2 + screen_len + 1)
        stdscr.refresh()
        box = Textbox(editwin)
        curses.curs_set(1)
        # Let the user edit until Ctrl-G is struck.
        box.edit()

        # Get resulting contents
        message = box.gather()
        curses.curs_set(0)
        return message.strip()

    def selectorBox(stdscr: curses.initscr, items: list, y_pos: int = 9):
        """Creates a box containing a list of items to select from
        initialized with stdscr, items:list, y_pos:int"""

        index = 0
        num_items = len(items)
        bottom_y = y_pos + len(items) * 2
        longest = 0
        for i in items:
            if len(i) > longest:
                longest = len(i)
        bottom_x = 1 + longest + 1
        rectangle(stdscr, y_pos, 0, bottom_y, bottom_x)
        for idx, item in enumerate(items):
            if idx == index:
                # stdscr.addstr(y_pos+1 + idx*2, 1, item, curses.color_pair(logo))
                stdscr.addstr(y_pos + 1 + idx * 2, 1, item, curses.A_REVERSE)
            else:
                stdscr.addstr(y_pos + 1 + idx * 2, 1, item)

        keypress = stdscr.getch()
        while keypress not in [curses.KEY_ENTER, 10, 13]:
            if keypress == curses.KEY_UP:
                if index > 0:
                    index -= 1
            elif keypress == curses.KEY_DOWN:
                if index + 1 < num_items:
                    index += 1

            for idx, item in enumerate(items):
                if idx == index:
                    # stdscr.addstr(y_pos+1 + idx*2, 1, item, curses.color_pair(logo))
                    stdscr.addstr(y_pos + 1 + idx * 2, 1, item, curses.A_REVERSE)
                else:
                    stdscr.addstr(y_pos + 1 + idx * 2, 1, item)
            keypress = stdscr.getch()
        return items[index]

    def selectorBoxColumns(stdscr: curses.initscr, items: list, y_pos: int = 9):
        """
        Creates a box containing a list of items split into columns. Returns items at selected index.
        """
        rows, cols = stdscr.getmaxyx()
        def stringMaker(line: list):
            out = ""
            for item in line[1:]:
                out += "{: <20}".format(item[:20]) + "|"
            return out[:-1]

        index = 0
        offset = 0
        num_items = len(items)
        width = min((len(items[0])-1) * 21, cols-2)
        bottom_y = y_pos + min(rows-10, len(items)*2)
        longest = 0
        for i in items:
            if len(i) > longest:
                longest = len(i)
        bottom_x = 1 + width + 1
        rectangle(stdscr, y_pos, 0, bottom_y, bottom_x)

        for idx in range(min(10, num_items)):
            if idx == index:
                stdscr.addstr(
                    y_pos + 1 + idx * 2,
                    1,
                    stringMaker(items[idx + offset]),
                    curses.A_BLINK | curses.A_REVERSE,
                )
            else:
                stdscr.addstr(
                    y_pos + 1 + idx * 2,
                    1,
                    stringMaker(items[idx + offset]),
                    curses.color_pair(table),
                )
        keypress = stdscr.getch()
        while (keypress) not in [curses.KEY_ENTER, 10, 13, 27]:
            if keypress == curses.KEY_UP:
                if offset >= 0:
                    if index > 0:
                        index -= 1
                    else:
                        if offset > 0:
                            offset -= 1
            elif keypress == curses.KEY_DOWN:
                if index + offset < num_items - 1:
                    if index == 9:
                        offset += 1
                    else:
                        index += 1
            for idx in range(min(10, num_items)):
                if idx == index:
                    stdscr.addstr(
                        y_pos + 1 + idx * 2,
                        1,
                        stringMaker(items[idx + offset]),
                        curses.A_BLINK | curses.A_REVERSE,
                    )
                else:
                    stdscr.addstr(
                        y_pos + 1 + idx * 2,
                        1,
                        stringMaker(items[idx + offset]),
                        curses.color_pair(table),
                    )
            stdscr.refresh()
            keypress = stdscr.getch()
        if keypress == 27:
            return -1
        return items[index + offset]

    def printHeader(stdscr: curses.initscr, dirStr: str):
        """ Prints our amazing Header used everywhere"""
        rows, cols = stdscr.getmaxyx() # 35
        rectangle(stdscr, 0, 0, 8, cols-1)
        LOGO = """
██████╗░██████╗░░██████╗███╗░░░███╗
██╔══██╗██╔══██╗██╔════╝████╗░████║
██████╦╝██║░░██║╚█████╗░██╔████╔██║
██╔══██╗██║░░██║░╚═══██╗██║╚██╔╝██║
██████╦╝██████╔╝██████╔╝██║░╚═╝░██║
╚═════╝░╚═════╝░╚═════╝░╚═╝░░░░░╚═╝"""
        for i, line in enumerate(LOGO.split('\n')):
            stdscr.addstr(
                i,
                (cols - 35) //2,
                line,
                curses.color_pair(logo),
            )
        if len(dirStr) >= cols -2:
            dirStr = ".../" +  dirStr[-cols+6:]
        stdscr.addstr(7, (cols - len(dirStr))//2, dirStr)
        stdscr.refresh()

    def columns(stdscr: curses.initscr, items: list, y_pos: int = 9):
        """ Makes columns for info can we in colums"""
        UIhack = uiBlocks.infoText
        x_offset = 0
        for column in items:

            y_offset = y_pos

            for line in column:
                UIhack(stdscr, line, y_offset, x_offset)
                y_offset += 2
            x_offset += 50

    def inLineSelection(stdscr: curses.initscr, label: str, items: list, y_pos: int = 9):
        """ In line selection so it can selected thing in a list and return it has a str"""
        index = 0
        num_items = len(items)
        bottom_y = y_pos + 1
        longest = len(label) + 1
        for i in items:
            longest += len(i) + 1
        cnt = 1 + len(label)
        bottom_x = 1 + longest + 1

        rectangle(stdscr, y_pos - 1, cnt, bottom_y, bottom_x)
        cnt += 1
        stdscr.addstr(y_pos, 0, label)
        stdscr.refresh()
        for idx, item in enumerate(items):
            if idx == index:
                stdscr.addstr(y_pos, cnt, item, curses.A_REVERSE)
            else:
                stdscr.addstr(y_pos, cnt, item)
            cnt += len(item) + 1

        keypress = stdscr.getch()
        while (keypress) not in [curses.KEY_ENTER, 10, 13]:
            if keypress == curses.KEY_LEFT:
                if index > 0:
                    index -= 1
            elif keypress == curses.KEY_RIGHT:
                if index + 1 < num_items:
                    index += 1
            cnt = 2 + len(label)
            for idx, item in enumerate(items):
                if idx == index:
                    stdscr.addstr(y_pos, cnt, item, curses.A_REVERSE)
                else:
                    stdscr.addstr(y_pos, cnt, item)
                cnt += len(item) + 1
            keypress = stdscr.getch()
        return items[index].strip()

    def dateSelector(stdscr: curses.initscr(), label: str, y_pos: int = 9) -> str:
        """
        DD/MM/YYYY -.- HH:MM
        """
        dMax = 31
        mMax = 12
        sIndex = 0
        hMax = 23
        minMax = 59
        x_offset = len(label) + 1
        bottom_y = y_pos + 1
        bottom_x = x_offset + 16 + 1
        stdscr.addstr(y_pos, 0, label)
        stdscr.refresh()
        rectangle(stdscr, y_pos - 1, x_offset, bottom_y, bottom_x)
        DAY = 1
        MONTH = 1
        YEAR = 2020
        HOUR = 0
        MINUTE = 0
        DATE = f"{DAY:0>2}/{MONTH:0>2}/{YEAR:0>2}-{HOUR:0>2}:{MINUTE:0>2}"
        stdscr.addstr(y_pos, x_offset + 1, f"{DAY:0>2}", curses.A_REVERSE)
        stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
        stdscr.addstr(y_pos, x_offset + 3 + 1, f"{MONTH:0>2}")
        stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
        stdscr.addstr(y_pos, x_offset + 6 + 1, f"{YEAR:0>4}")
        stdscr.addstr(y_pos, x_offset + 1 + 10, "-")
        stdscr.addstr(y_pos, x_offset + 11 + 1, f"{HOUR:0>2}")
        stdscr.addstr(y_pos, x_offset + 1 + 13, ":")
        stdscr.addstr(y_pos, x_offset + 14 + 1, f"{MINUTE:0>2}")

        keypress = stdscr.getch()
        while (keypress) not in [curses.KEY_ENTER, 10, 13]:
            if keypress == curses.KEY_LEFT:
                if sIndex > 0:
                    sIndex -= 1
            elif keypress == curses.KEY_RIGHT:
                if sIndex < 4:
                    sIndex += 1
            elif keypress == curses.KEY_UP:
                if sIndex == 0:  # Day
                    if DAY < dMax:
                        DAY += 1
                elif sIndex == 1:  # Month
                    if MONTH < mMax:
                        MONTH += 1
                elif sIndex == 2:  # Year
                    YEAR += 1
                elif sIndex == 3:  # Hours
                    if HOUR < hMax:
                        HOUR += 1
                elif sIndex == 4:  # Minutes
                    if MINUTE < minMax:
                        MINUTE += 1
            elif keypress == curses.KEY_DOWN:
                if sIndex == 0:  # Day
                    if DAY > 1:
                        DAY -= 1
                elif sIndex == 1:  # Month
                    if MONTH > 1:
                        MONTH -= 1
                elif sIndex == 2:  # Year
                    if YEAR > 2020:
                        YEAR -= 1
                elif sIndex == 3:  # Hours
                    if HOUR > 0:
                        HOUR -= 1
                elif sIndex == 4:  # Minutes
                    if MINUTE > 0:
                        MINUTE -= 1
            if sIndex == 0:
                stdscr.addstr(
                    y_pos, x_offset + 1, f"{DAY:0>2}", curses.A_REVERSE
                )
                stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
                stdscr.addstr(y_pos, x_offset + 3 + 1, f"{MONTH:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
                stdscr.addstr(y_pos, x_offset + 6 + 1, f"{YEAR:0>4}")
                stdscr.addstr(y_pos, x_offset + 1 + 10, "-")
                stdscr.addstr(y_pos, x_offset + 11 + 1, f"{HOUR:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 13, ":")
                stdscr.addstr(y_pos, x_offset + 14 + 1, f"{MINUTE:0>2}")
            elif sIndex == 1:
                stdscr.addstr(y_pos, x_offset + 1, f"{DAY:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
                stdscr.addstr(
                    y_pos, x_offset + 3 + 1, f"{MONTH:0>2}", curses.A_REVERSE
                )
                stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
                stdscr.addstr(y_pos, x_offset + 6 + 1, f"{YEAR:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 10, "-")
                stdscr.addstr(y_pos, x_offset + 11 + 1, f"{HOUR:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 13, ":")
                stdscr.addstr(y_pos, x_offset + 14 + 1, f"{MINUTE:0>2}")
            elif sIndex == 2:
                stdscr.addstr(y_pos, x_offset + 1, f"{DAY:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
                stdscr.addstr(y_pos, x_offset + 3 + 1, f"{MONTH:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
                stdscr.addstr(
                    y_pos, x_offset + 6 + 1, f"{YEAR:0>2}", curses.A_REVERSE
                )
                stdscr.addstr(y_pos, x_offset + 1 + 10, "-")
                stdscr.addstr(y_pos, x_offset + 11 + 1, f"{HOUR:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 13, ":")
                stdscr.addstr(y_pos, x_offset + 14 + 1, f"{MINUTE:0>2}")
            elif sIndex == 3:
                stdscr.addstr(y_pos, x_offset + 1, f"{DAY:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
                stdscr.addstr(y_pos, x_offset + 3 + 1, f"{MONTH:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
                stdscr.addstr(y_pos, x_offset + 6 + 1, f"{YEAR:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 10, "-")
                stdscr.addstr(
                    y_pos, x_offset + 11 + 1, f"{HOUR:0>2}", curses.A_REVERSE
                )
                stdscr.addstr(y_pos, x_offset + 1 + 13, ":")
                stdscr.addstr(y_pos, x_offset + 14 + 1, f"{MINUTE:0>2}")
            else:
                stdscr.addstr(y_pos, x_offset + 1, f"{DAY:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
                stdscr.addstr(y_pos, x_offset + 3 + 1, f"{MONTH:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
                stdscr.addstr(y_pos, x_offset + 6 + 1, f"{YEAR:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 10, "-")
                stdscr.addstr(y_pos, x_offset + 11 + 1, f"{HOUR:0>2}")
                stdscr.addstr(y_pos, x_offset + 1 + 13, ":")
                stdscr.addstr(
                    y_pos, x_offset + 14 + 1, f"{MINUTE:0>2}", curses.A_REVERSE
                )
            DATE = f"{DAY:0>2}/{MONTH:0>2}/{YEAR:0>2}-{HOUR:0>2}:{MINUTE:0>2}"
            keypress = stdscr.getch()
        else:
            return DATE

    def dateSelectorOld(stdscr: curses.initscr(), label: str, y_pos: int = 9) -> str:
        """
        DD/MM/YYYY = 10 char
        """
        sIndex = 0
        dMax = 31
        mMax = 12
        x_offset = len(label) + 1
        bottom_y = y_pos + 1
        bottom_x = x_offset + 10 + 1
        stdscr.addstr(y_pos, 0, label)
        stdscr.refresh()
        rectangle(stdscr, y_pos - 1, x_offset, bottom_y, bottom_x)
        DAY = 1
        MONTH = 1
        YEAR = 2020
        DATE = f"{DAY:0>2}/{MONTH:0>2}/{YEAR:0>2}"
        stdscr.addstr(y_pos, x_offset + 1, f"{DAY: >2}", curses.A_REVERSE)
        stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
        stdscr.addstr(y_pos, x_offset + 3 + 1, f"{MONTH: >2}")
        stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
        stdscr.addstr(y_pos, x_offset + 6 + 1, f"{YEAR: >2}")

        keypress = stdscr.getch()
        while (keypress) not in [curses.KEY_ENTER, 10, 13]:
            if keypress == curses.KEY_LEFT:
                if sIndex > 0:
                    sIndex -= 1
            elif keypress == curses.KEY_RIGHT:
                if sIndex < 2:
                    sIndex += 1
            elif keypress == curses.KEY_UP:
                if sIndex == 0:  # Day
                    if DAY < dMax:
                        DAY += 1
                elif sIndex == 1:  # Month
                    if MONTH < mMax:
                        MONTH += 1
                elif sIndex == 2:  # Year
                    YEAR += 1
            elif keypress == curses.KEY_DOWN:
                if sIndex == 0:  # Day
                    if DAY > 1:
                        DAY -= 1
                elif sIndex == 1:  # Month
                    if MONTH > 1:
                        MONTH -= 1
                elif sIndex == 2:  # Year
                    if YEAR > 2020:
                        YEAR -= 1
            if sIndex == 0:
                stdscr.addstr(
                    y_pos, x_offset + 1, f"{DAY: >2}", curses.A_REVERSE
                )
                stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
                stdscr.addstr(y_pos, x_offset + 3 + 1, f"{MONTH: >2}")
                stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
                stdscr.addstr(y_pos, x_offset + 6 + 1, f"{YEAR: >2}")
            elif sIndex == 1:
                stdscr.addstr(y_pos, x_offset + 1, f"{DAY: >2}")
                stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
                stdscr.addstr(
                    y_pos, x_offset + 3 + 1, f"{MONTH: >2}", curses.A_REVERSE
                )
                stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
                stdscr.addstr(y_pos, x_offset + 6 + 1, f"{YEAR: >2}")
            else:
                stdscr.addstr(y_pos, x_offset + 1, f"{DAY: >2}")
                stdscr.addstr(y_pos, x_offset + 1 + 2, "/")
                stdscr.addstr(y_pos, x_offset + 3 + 1, f"{MONTH: >2}")
                stdscr.addstr(y_pos, x_offset + 1 + 5, "/")
                stdscr.addstr(
                    y_pos, x_offset + 6 + 1, f"{YEAR: >2}", curses.A_REVERSE
                )
            DATE = f"{DAY:0>2}/{MONTH:0>2}/{YEAR:0>2}"
            keypress = stdscr.getch()
        else:
            return DATE
