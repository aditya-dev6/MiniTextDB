import json
import os
from enum import Enum

from exceptions.exceptions import (AlreadyExistException, DoesNotExistException, EmptyException, Success)
from helper.helper import (get_table_path, load_table, save_table, get_storage_path)


class ColumnType(Enum):
    Integer = 1
    Decimal = 2
    String = 3


column_template = {}


def create_table(table_name: str) -> Success:
    path = get_table_path(table_name)

    if os.path.exists(path):
        raise AlreadyExistException(f"Table '{table_name}' already exists")

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as file:
        json.dump({}, file, indent=4)

    return Success(f"Table {table_name} created successfully.")


def list_table():
    storage_path = get_storage_path()

    os.makedirs(storage_path, exist_ok=True)

    tables = []

    for file in sorted(os.listdir(storage_path)):
        if file.endswith(".json"):
            tables.append(file[:-5])

    if len(tables) == 0:
        raise EmptyException("No tables found.")

    return tables


def delete_table(table_name: str) -> Success:
    file_path = get_table_path(table_name)

    if not os.path.exists(file_path):
        raise DoesNotExistException(f"Table {table_name} could not be found.")

    os.remove(file_path)

    return Success(f"Table {table_name} deleted successfully")


def insertColumnIntoTable(table_name: str, column_name: str, column_type: ColumnType):
    checkIfTableExists(table_name)

    data = load_table(table_name)

    # Check if column already exists
    for row in data.values():
        if column_name in row:
            raise AlreadyExistException(f"Column '{column_name}' already exists.")

    # Determine default value
    if column_type == ColumnType.String:
        default_value = ""

    elif column_type == ColumnType.Integer:
        default_value = 0

    elif column_type == ColumnType.Decimal:
        default_value = 0.0

    else:
        raise ValueError(f"Invalid column type: {column_type}")

    # Add column to every existing row
    for row in data.values():
        row[column_name] = default_value

    save_table(table_name, data)

    return Success(f"Column {column_name} added successfully.")


def deleteColumnFromTable(table_name: str, column_name: str):
    checkIfTableExists(table_name)

    data = load_table(table_name)

    column_exists = False

    for row in data.values():

        if column_name in row:
            del row[column_name]
            column_exists = True

    if not column_exists:
        raise DoesNotExistException(f"Column '{column_name}' does not exist.")

    save_table(table_name, data)

    return Success(f"Column {column_name} deleted successfully.")


def insertDataIntoTable(table_name: str, row_data: dict):
    checkIfTableExists(table_name)

    data = load_table(table_name)

    # Generate next numeric row ID
    if len(data) == 0:
        row_id = 1
    else:
        row_id = max(int(key) for key in data.keys()) + 1

    # JSON object keys are strings
    data[str(row_id)] = row_data

    save_table(table_name, data)

    return Success(f"Row {row_id} added successfully.")


def select_where(table_name: str, field: str, operator: str, value):
    checkIfTableExists(table_name)

    data = load_table(table_name)

    results = {}

    valid_operators = {"=", ">", ">=", "<", "<="}

    if operator not in valid_operators:
        raise ValueError(f"Invalid operator '{operator}'. "
                         f"Valid operators are: {valid_operators}")

    for row_id, details in data.items():

        if field not in details:
            continue

        field_value = details[field]

        if operator == "=":
            if field_value == value:
                results[row_id] = details

        elif operator == ">":
            if field_value > value:
                results[row_id] = details

        elif operator == ">=":
            if field_value >= value:
                results[row_id] = details

        elif operator == "<":
            if field_value < value:
                results[row_id] = details

        elif operator == "<=":
            if field_value <= value:
                results[row_id] = details

    if len(results) == 0:
        raise EmptyException("No results were found")

    return results


def select_all(table_name: str):
    checkIfTableExists(table_name)

    data = load_table(table_name)

    if len(data) == 0:
        raise EmptyException("No results were found")

    return data


def filtering(table_name: str, field: str):
    checkIfTableExists(table_name)

    data = load_table(table_name)

    filtered_data = []

    for row in data.values():

        if field in row:
            filtered_data.append(row[field])

    if len(filtered_data) == 0:
        raise EmptyException("No results were found")

    return filtered_data


def updateDataInTable(table_name: str, row_id: int, column_name: str, new_value):
    checkIfTableExists(table_name)

    data = load_table(table_name)

    row_id = str(row_id)

    if row_id not in data:
        raise DoesNotExistException(f"Row '{row_id}' does not exist.")

    if column_name not in data[row_id]:
        raise DoesNotExistException(f"Column '{column_name}' does not exist "
                                    f"for row '{row_id}'.")

    data[row_id][column_name] = new_value

    save_table(table_name, data)

    return Success("Data updated successfully.")


def deleteDataFromTable(table_name: str, row_id: int, column_name: str):
    checkIfTableExists(table_name)

    data = load_table(table_name)

    row_id = str(row_id)

    if row_id not in data:
        raise DoesNotExistException(f"Row '{row_id}' does not exist.")

    if column_name not in data[row_id]:
        raise DoesNotExistException(f"Column '{column_name}' does not exist "
                                    f"for row '{row_id}'.")

    del data[row_id][column_name]

    save_table(table_name, data)

    return Success("Data deleted successfully.")


def checkIfTableExists(table_name: str):
    if not os.path.exists(get_table_path(table_name)):
        raise DoesNotExistException(f"Table '{table_name}' does not exist.")

    return True


def execute(operation):
    try:
        result = operation()

        if result is not None:
            print(result)

        return result

    except (AlreadyExistException, DoesNotExistException, EmptyException, ValueError) as e:
        print(e)
        return None
