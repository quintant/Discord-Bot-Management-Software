import UILayer.uiBlocks as uiBlocks
from UILayer.inputChecker import InputChecker
from UILayer.prompts import Prompts

class EmployeeMenu:  # Þorgils
    '''class Encapsulates menu employee menu'''

    def __init__(self, controller, dirStr: str) -> None:
        self.controller = controller
        self.user = controller.user
        self.dirStr = dirStr + "/EmployeeMenu"
        self.stdscr = controller.stdscr
        self.stdscr.clear()
        self.inputChecker = InputChecker(controller, "Employee")
        self.prompts = Prompts(self.controller)
        uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)

    def showMain(self):
        '''
            Show employee menu
        '''
        menuItems = []
        menuItems.append("Employee Search")
        SEARCH = 0
        menuItems.append("Add New Employee")
        ADD = 1
        menuItems.append("List All Employees")
        LIST = 2
        menuItems.append("Back")
        BACK = 3
        selected = None
        while selected != menuItems[BACK]:
            self.stdscr.clear()
            uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
            selected = uiBlocks.uiBlocks.selectorBox(self.stdscr, menuItems)
            if selected == menuItems[SEARCH]:
                self.showSearch()

            elif selected == menuItems[ADD]:
                self.showAddEmployee()

            elif selected == menuItems[LIST]:
                employeeList = self.controller.getAllEmployees()
                if not employeeList:
                    self.prompts.notFound(self.dirStr)
                    continue
                else:
                    self.showEmployeeList(employeeList)
        else:
            return 0

    def showSearch(self):
        '''
        Enter search menu, return user input, also allow user toretry or quit
        '''
        _dir = "/Search"
        self.dirStr += _dir
        SEARCH_LABEL = "Name or SSN "

        menuItems = []
        menuItems.append("Search")
        SEARCH = 0
        menuItems.append("Retry")
        RETRY = 1
        menuItems.append("Back")
        BACK = 2

        selected = None

        while selected != menuItems[BACK]:
            self.stdscr.clear()
            uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
            itemToSearch = uiBlocks.uiBlocks.textField(self.stdscr, SEARCH_LABEL)
            selected = uiBlocks.uiBlocks.selectorBox(self.stdscr, menuItems,
                                                     13)
            if selected == menuItems[SEARCH]:
                employees = self.controller.searchEmployeeList(itemToSearch)
                if not employees:
                    self.prompts.notFound(self.dirStr)
                    continue
                else:
                    self.showEmployeeList(employees)
            elif selected == menuItems[RETRY]:
                continue

        self.dirStr = self.dirStr[0:-len(_dir)]

    def showAddEmployee(self):
        """ Show adding a new instance of employee with the neccesery info"""
        _dir = "/AddEmployee"
        self.dirStr += _dir #13 char
        self.stdscr.clear()
        uiBlocks.uiBlocks.printHeader(self.stdscr,self.dirStr)
        emLabels = [
            "Name",
            "SSN",
            "Address",
            "Home Phone",
            "Mobile Phone",
            "Email",
            "Location",
            "Position",
        ]
        menuItems = []
        menuItems.append("Create")
        CREATE = 0
        menuItems.append("Retry")
        RETRY = 1
        menuItems.append("Cancel")
        CANCEL = 2
        selected = None

        while selected != menuItems[CANCEL]:
            goBack = False
            employeeinfo = []
            offset = 10
            for label in emLabels:
                if label == "Position":
                    text = uiBlocks.uiBlocks.inLineSelection(self.stdscr,
                                                             "Position",
                                                             ["Admin", "Office",
                                                              "Airport"],
                                                             offset)

                elif label == "Location":
                    destList = self.controller.getAllDestinations()
                    if not destList:
                        uiBlocks.uiBlocks.infoText(self.stdscr, "No locations have been added, defaulting to Reykjavik",
                                                   offset, 105)
                        text = "Reykjavik"
                    else:
                        airportList = [dest.airportName for dest in destList]
                        text = uiBlocks.uiBlocks.inLineSelection(
                            self.stdscr, label, airportList, offset)
                else:
                    while True:
                        # Check if user input is good, on first text field
                        # allow user to press enter and get a back key
                        text = uiBlocks.uiBlocks.textField(self.stdscr, label,
                                                           offset)
                        if label == emLabels[0] and not text:
                            # If this is the first text field and user adds an
                            # enters nothing a selection box will pop up asking
                            # user to either go back or retry his input
                            if self.prompts.noInput(offset):
                                goBack = True
                                break
                            else:
                                self.stdscr.clear()
                                uiBlocks.uiBlocks.printHeader(self.stdscr,
                                                              self.dirStr)
                        else:
                            inputCheck = self.inputChecker.checkInput(text, label)

                            if inputCheck is True:
                                idCheck = self.inputChecker.idChecker(text,
                                                                 "employee")
                                if idCheck is True:
                                    break
                                else:
                                    uiBlocks.uiBlocks.infoText(self.stdscr,
                                                               idCheck,
                                                               offset, 105)
                            else:
                                uiBlocks.uiBlocks.infoText(self.stdscr,
                                                           inputCheck,
                                                           offset, 105)
                    if goBack:
                        break

                offset += 3
                employeeinfo.append(text.strip())
            if goBack:
                break
            selected = uiBlocks.uiBlocks.selectorBox(self.stdscr, menuItems, offset)
            if selected == menuItems[CREATE]:
                self.controller.createEmployee(*employeeinfo)
                selected = menuItems[CANCEL]
            elif selected == menuItems[RETRY]:
                continue

        self.dirStr = self.dirStr[0:-len(_dir)]

    def showEmployeeInfo(self, employee):
        """
        This function shows info on specific employee and show availible options on him.
        """
        _dir = "/EmployeeInfo"
        self.dirStr += _dir #14 char
        self.stdscr.clear()
        uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)

        menuItems = []
        menuItems.append("Update Employee")
        UPDATE = 0
        menuItems.append("Remove Employee")
        REMOVE = 1
        menuItems.append("Back")
        BACK = 2
        selected = None

        offset = 20

        while selected != menuItems[BACK]:
            self.stdscr.clear()
            uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
            # first column
            col1 = [
                f"Name: {employee.name}",
                f"Address: {employee.homeAddress}",
                f"Email: {employee.email}"
            ]
            # Second column
            col2 = [
                f"SSN: {employee.idNumber}",
                f"Home phone: {employee.homePhone}",
                f"Location: {employee.geoLocation}"
            ]
            # 3rd column
            col3 = [
                f"Position: {employee.employeeType}",
                f"Mobile phone: {employee.mobilePhone}",
            ]
            uiBlocks.uiBlocks.columns(self.stdscr, [col1, col2,col3], y_pos=10)

            selected = uiBlocks.uiBlocks.selectorBox(self.stdscr, menuItems, offset)
            if selected ==  menuItems[UPDATE]:
                self.showUpdateEmployee(employee)
                employee = self.controller.getEmployee(employee.idNumber)
            elif selected == menuItems[REMOVE]:
                removeCheck = self.prompts.removeCheck(employee.name,
                                                       "Employee",
                                                       self.dirStr)
                if removeCheck:
                    self.controller.removeEmployee(employee)
                    return True
        self.dirStr = self.dirStr[0:-len(_dir)]

    def showEmployeeList(self, employeeList: list):
        """ Shows a list of all employees that we have"""
        def stringMaker(line: list):
            out = ""
            for item in line:
                out += "{: <20}".format(item[:20])+"|"
            return out[:-1]
        _dir = "/ListEmployees"
        self.dirStr += _dir #14 char
        self.stdscr.clear()
        uiBlocks.uiBlocks.printHeader(self.stdscr,self.dirStr)
        menuItems = []
        menuItems.append("View Selected")
        VIEW = 0
        menuItems.append("Select Another")
        SELECTANOTHER = 1
        menuItems.append("Back")
        BACK = 2
        selected = None
        items = []
        if employeeList:
            for item in employeeList:
                items.append([item, item.name, item.idNumber, item.geoLocation, item.employeeType])

            while selected != menuItems[BACK]:
                self.stdscr.clear()
                uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
                titles = ["Name", "Employee SSN", "Location", "Employee type"]
                TITLE = stringMaker(titles)
                uiBlocks.uiBlocks.infoText(self.stdscr, TITLE, y_pos=10, x_pos=1)
                selectedItem = uiBlocks.uiBlocks.selectorBoxColumns(self.stdscr, items, y_pos=11)[0]
                selected = uiBlocks.uiBlocks.selectorBox(self.stdscr, menuItems, 42)
                if selected == menuItems[SELECTANOTHER]:
                    pass
                elif selected == menuItems[VIEW]:
                    removeCheck = self.showEmployeeInfo(selectedItem)
                    if removeCheck:
                        selected = menuItems[BACK]
        self.dirStr = self.dirStr[0:-len(_dir)]

    def showUpdateEmployee(self, Employee):
        """ Showing how to update info on employee """
        _dir = "/Update Employee"
        self.dirStr += _dir #16 char
        self.stdscr.clear()
        uiBlocks.uiBlocks.printHeader(self.stdscr,self.dirStr)

        menuItems = []
        menuItems.append("Address")
        ADDRESS = 0
        menuItems.append("Home Phone")
        HOME = 1
        menuItems.append("Mobile Phone")
        MOBILE = 2
        menuItems.append("Email")
        EMAIL = 3
        menuItems.append("Location")
        LOCATION = 4
        menuItems.append("Position")
        POSITION = 5
        menuItems.append("Back")
        BACK = 6
        selected = None
        textF = uiBlocks.uiBlocks.textField
        while selected != menuItems[BACK]:
            self.stdscr.clear()
            uiBlocks.uiBlocks.printHeader(self.stdscr, self.dirStr)
            offset = 10
            uiBlocks.uiBlocks.infoText(self.stdscr,"What to Update",offset,0)
            offset += 2
            selected = uiBlocks.uiBlocks.selectorBox(self.stdscr,menuItems,offset)
            offset = 35
            if selected == menuItems[ADDRESS]:
                while True:
                    address = textF(self.stdscr,"Address",offset)
                    inputCheck = self.inputChecker.checkInput(address, "Address")
                    if inputCheck is True:
                        Employee.homeAddress = address
                        self.controller.updateEmployee(Employee)
                        break
                    else:
                        uiBlocks.uiBlocks.infoText(self.stdscr, inputCheck,
                                                   offset, 105)
            elif selected == menuItems[HOME]:
                while True:
                    phone = textF(self.stdscr,"Home Phone",offset)
                    inputCheck = self.inputChecker.checkInput(phone,
                                                              "Home Phone")
                    if inputCheck is True:
                        Employee.homePhone = phone
                        self.controller.updateEmployee(Employee)
                        break
                    else:
                        uiBlocks.uiBlocks.infoText(self.stdscr, inputCheck,
                                                   offset, 105)
            elif selected == menuItems[MOBILE]:
                while True:
                    mobilePhone = textF(self.stdscr, "Mobile Phone", offset)
                    inputCheck = self.inputChecker.checkInput(mobilePhone,
                                                              "Mobile Phone")
                    if inputCheck is True:
                        Employee.mobilePhone = mobilePhone
                        self.controller.updateEmployee(Employee)
                        break
                    else:
                        uiBlocks.uiBlocks.infoText(self.stdscr, inputCheck,
                                                   offset, 105)
            elif selected == menuItems[EMAIL]:
                while True:
                    email = textF(self.stdscr,"Email",offset)
                    inputCheck = self.inputChecker.checkInput(email, "Email")
                    if inputCheck is True:
                        Employee.email = email
                        self.controller.updateEmployee(Employee)
                        break
                    else:
                        uiBlocks.uiBlocks.infoText(self.stdscr, inputCheck,
                                                   offset, 105)

            elif selected == menuItems[LOCATION]:
                # If no locations are in our database this throws a TypeError
                # This catches it displays error text
                try:
                    destList = self.controller.getAllDestinations()
                    airportList = [dest.airportName for dest in destList]
                    text = uiBlocks.uiBlocks.inLineSelection(self.stdscr,
                                                            "Locations",
                                                            airportList,
                                                            offset)
                    Employee.geoLocation = text
                    self.controller.updateEmployee(Employee)
                except TypeError:
                    uiBlocks.uiBlocks.infoText(self.stdscr, """
                                                            There are no locations in our database
                                                            Therefore you cannot change employees
                                                            location. Please add destinations through
                                                            our destination menu
                                                            Press anykey to continue
                                                            """, offset, 0)
                    self.stdscr.getch()

            elif selected == menuItems[POSITION]:
                position = uiBlocks.uiBlocks.inLineSelection(self.stdscr,
                                                             "Position",
                                                             ["Admin",
                                                              "Office",
                                                              "Airport"],
                                                             offset)
                Employee.employeeType = position
                self.controller.updateEmployee(Employee)

        self.dirStr = self.dirStr[0:-len(_dir)]
