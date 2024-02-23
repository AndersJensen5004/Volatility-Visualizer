class Exit:
    @classmethod
    def exit_command(cls, TERMINAL_WIDTH: int) -> list:
        row_data = []
        for i in range(0, 5):
            row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))
        row_data.append(("COMMANDS:" + " "*(TERMINAL_WIDTH - 14) +"*"))
        row_data.append(("close - closes terminal" + " "*(TERMINAL_WIDTH - 28) +"*"))
        row_data.append(("exit - return to home (this page)" + " "*(TERMINAL_WIDTH - 38) +"*"))
        row_data.append(("equity <symbol> - loads equity" + " "*(TERMINAL_WIDTH - 35) +"*"))
        for i in range(0, 5):
            row_data.append(("*" + " "*(TERMINAL_WIDTH - 6) +"*"))
        return row_data