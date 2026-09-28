import ast
import json
import re

from engine.engine import (ColumnType, create_table, list_table, delete_table, insertColumnIntoTable,
                               deleteColumnFromTable, insertDataIntoTable, select_where, select_all, filtering,
                               updateDataInTable, deleteDataFromTable, )


class DatabaseCommandParser:

    def __init__(self):
        self.commands = {"CREATE": self.parse_create, "SHOW": self.parse_show, "DROP": self.parse_drop,
                         "ADD": self.parse_add, "INSERT": self.parse_insert, "SELECT": self.parse_select,
                         "UPDATE": self.parse_update, "DELETE": self.parse_delete, "EXIT": self.parse_exit,
                         "QUIT": self.parse_exit, }

    # --------------------------------------------------
    # Utility functions
    # --------------------------------------------------

    # So that other classes can directly access this
    def findValue(self, value):

        value = value.strip()

        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            loweredValue = value.lower()

            if loweredValue == "true":
                return True

            if loweredValue == "false":
                return False

            if loweredValue == "null":
                return None

            return value

    def columnType(self, type_name):

        types = {"INTEGER": ColumnType.Integer, "INT": ColumnType.Integer, "DECIMAL": ColumnType.Decimal,
                 "FLOAT": ColumnType.Decimal, "STRING": ColumnType.String, "TEXT": ColumnType.String, }

        type_name = type_name.upper()

        if type_name not in types:
            raise ValueError(f"Invalid column type '{type_name}'. "
                             f"Use INTEGER, DECIMAL, or STRING.")

        return types[type_name]

    def outputFormat(self, result):

        if result is None:
            return ""

        if isinstance(result, list):
            if not result:
                return "No results were found."

            return "\n".join(f"{index}. {item}" for index, item in enumerate(result, start=1))

        if isinstance(result, dict):
            if not result:
                return "No results were found."

            lines = []

            for row_id, row_data in result.items():
                lines.append(f"ID: {row_id} | "
                             f"{json.dumps(row_data, ensure_ascii=False)}")

            return "\n".join(lines)

        return str(result)

    # --------------------------------------------------
    # CREATE TABLE
    # --------------------------------------------------

    def parse_create(self, command):
        pattern = r"^CREATE\s+TABLE\s+([A-Za-z_][A-Za-z0-9_]*)$"

        match = re.match(pattern, command, re.IGNORECASE)

        if not match:
            raise ValueError("Syntax: CREATE TABLE table_name")

        table_name = match.group(1)

        return lambda: create_table(table_name)

    # --------------------------------------------------
    # SHOW TABLES
    # --------------------------------------------------

    def parse_show(self, command):
        if not re.fullmatch(r"SHOW\s+TABLES", command, re.IGNORECASE):
            raise ValueError("Syntax: SHOW TABLES")

        return list_table

    # --------------------------------------------------
    # DROP TABLE / DROP COLUMN
    # --------------------------------------------------

    def parse_drop(self, command):
        table_match = re.fullmatch(r"DROP\s+TABLE\s+([A-Za-z_][A-Za-z0-9_]*)", command, re.IGNORECASE, )

        if table_match:
            table_name = table_match.group(1)

            return lambda: delete_table(table_name)

        column_match = re.fullmatch(r"DROP\s+COLUMN\s+([A-Za-z_][A-Za-z0-9_]*)"
                                    r"\s+([A-Za-z_][A-Za-z0-9_]*)", command, re.IGNORECASE, )

        if column_match:
            table_name = column_match.group(1)
            column_name = column_match.group(2)

            return lambda: deleteColumnFromTable(table_name, column_name)

        raise ValueError("Syntax:\n"
                         "DROP TABLE table_name\n"
                         "DROP COLUMN table_name column_name")

    # --------------------------------------------------
    # ADD COLUMN
    # --------------------------------------------------

    def parse_add(self, command):
        pattern = (
            r"^ADD\s+COLUMN\s+"
            r"([A-Za-z_][A-Za-z0-9_]*)\s+"
            r"([A-Za-z_][A-Za-z0-9_]*)\s+"
            r"([A-Za-z_][A-Za-z0-9_]*)$"
        )
        match = re.match(pattern, command, re.IGNORECASE)

        if not match:
            raise ValueError("Syntax: ADD COLUMN table_name column_name type")

        table_name = match.group(1)
        column_name = match.group(2)
        type_name = match.group(3)

        column_type = self.columnType(type_name)

        return lambda: insertColumnIntoTable(table_name, column_name, column_type)

    # --------------------------------------------------
    # INSERT INTO
    # --------------------------------------------------

    def parse_insert(self, command):
        pattern = (r"^INSERT\s+INTO\s+"
                   r"([A-Za-z_][A-Za-z0-9_]*)\s+"
                   r"VALUES\s+(.+)$")

        match = re.match(pattern, command, re.IGNORECASE)

        if not match:
            raise ValueError('Syntax: INSERT INTO table_name VALUES '
                             '{"column": value}')

        table_name = match.group(1)
        values_text = match.group(2).strip()

        try:
            row_data = ast.literal_eval(values_text)
        except (ValueError, SyntaxError):
            raise ValueError("Invalid row data. Use a valid Python dictionary.")

        if not isinstance(row_data, dict):
            raise ValueError("VALUES must contain a dictionary.")

        return lambda: insertDataIntoTable(table_name, row_data)

    # --------------------------------------------------
    # SELECT
    # --------------------------------------------------

    def parse_select(self, command):
        # SELECT * FROM table
        all_match = re.fullmatch(r"SELECT\s+\*\s+FROM\s+"
                                 r"([A-Za-z_][A-Za-z0-9_]*)", command, re.IGNORECASE, )

        if all_match:
            table_name = all_match.group(1)

            return lambda: select_all(table_name)

        # SELECT column FROM table
        column_match = re.fullmatch(r"SELECT\s+([A-Za-z_][A-Za-z0-9_]*)\s+FROM\s+"
                                    r"([A-Za-z_][A-Za-z0-9_]*)", command, re.IGNORECASE, )

        if column_match:
            field = column_match.group(1)
            table_name = column_match.group(2)

            return lambda: filtering(table_name, field)

        # SELECT * FROM table WHERE field operator value
        # matches regex of the following pattern
        where_match = re.fullmatch(r"SELECT\s+\*\s+FROM\s+"
                                   r"([A-Za-z_][A-Za-z0-9_]*)\s+"
                                   r"WHERE\s+"
                                   r"([A-Za-z_][A-Za-z0-9_]*)\s+"
                                   r"(>=|<=|=|>|<)\s+(.+)", command, re.IGNORECASE, )

        if where_match:
            table_name = where_match.group(1)
            field = where_match.group(2)
            operator = where_match.group(3)
            value = self.findValue(where_match.group(4))

            return lambda: select_where(table_name, field, operator, value)

        raise ValueError("Syntax:\n"
                         "SELECT * FROM table_name\n"
                         "SELECT column FROM table_name\n"
                         "SELECT * FROM table_name WHERE field >= value")

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    def parse_update(self, command):
        pattern = (r"^UPDATE\s+"
                   r"([A-Za-z_][A-Za-z0-9_]*)\s+"
                   r"SET\s+"
                   r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s+"
                   r"WHERE\s+id\s*=\s*(\d+)$")

        match = re.match(pattern, command, re.IGNORECASE)

        if not match:
            raise ValueError("Syntax: UPDATE table SET column = value WHERE id = 1")

        table_name = match.group(1)
        column_name = match.group(2)
        new_value = self.findValue(match.group(3))
        row_id = int(match.group(4))

        return lambda: updateDataInTable(table_name, row_id, column_name, new_value)

    # --------------------------------------------------
    # DELETE COLUMN DATA
    # --------------------------------------------------

    def parse_delete(self, command):
        pattern = (r"^DELETE\s+FROM\s+"
                   r"([A-Za-z_][A-Za-z0-9_]*)\s+"
                   r"COLUMN\s+"
                   r"([A-Za-z_][A-Za-z0-9_]*)\s+"
                   r"WHERE\s+id\s*=\s*(\d+)$")

        match = re.match(pattern, command, re.IGNORECASE)

        if not match:
            raise ValueError("Syntax: DELETE FROM table COLUMN column WHERE id = 1")

        table_name = match.group(1)
        column_name = match.group(2)
        row_id = int(match.group(3))

        return lambda: deleteDataFromTable(table_name, row_id, column_name)

    # --------------------------------------------------
    # EXIT
    # --------------------------------------------------
    def parse_exit(self, command):
        return lambda: "EXIT"

    # --------------------------------------------------
    # MAIN PARSER
    # --------------------------------------------------

    def parse(self, command):
        command = command.strip()

        if not command:
            raise ValueError("Command cannot be empty.")

        first_word = command.split(maxsplit=1)[0].upper()

        if first_word not in self.commands:
            raise ValueError(f"Unknown command '{first_word}'.")

        return self.commands[first_word](command)

    # --------------------------------------------------
    # EXECUTION + OUTPUT
    # --------------------------------------------------
    def execute_command(self, command):
        try:
            operation = self.parse(command)
            result = operation()

            if result == "EXIT":
                return "EXIT"

            output = self.outputFormat(result)

            if output:
                return output

            return "Command executed successfully."

        except Exception as error:
            return f"Error: {error}"
