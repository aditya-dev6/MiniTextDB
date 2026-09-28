# TextDB — Mini CLI-Based Database

**Course project:** VITyarthi — Build Your Own Project  
**Project type:** Python command-line application  
**Status:** Educational prototype; implemented features are listed below.

## 1. Overview

TextDB is a terminal-based mini database application written in Python. It provides a custom command interface for managing tables and data through commands such as `CREATE TABLE`, `INSERT INTO`, `SELECT`, `UPDATE`, and `DELETE`. The command parser validates user input and dispatches operations to database-engine functions. The engine is responsible for the underlying table and JSON storage behavior.

The project applies Python programming concepts to a practical data-management problem: organizing records, performing basic operations, and preserving data between application runs.

## 2. Problem Statement

Small learning exercises often manipulate data directly in Python variables or isolated JSON files. This can make it difficult to practice the structure of a database system, including command interpretation, table operations, validation, persistence, and separation of responsibilities.

TextDB addresses this learning problem by implementing a compact database-like console where users issue structured commands and receive readable results or errors.

## 3. Objectives

- Build an interactive command-line database prototype in Python.
- Implement a custom command parser using regular expressions and Python literal parsing.
- Provide table-management and record-management operations.
- Separate command-line interaction, parsing, engine operations, and storage responsibilities.
- Practice data structures, file handling, modular programming, and exception handling.
- Document, test, and evaluate the system as an academic project.

## 4. Scope

### Included in the current implementation

- Interactive `TextDB>` console.
- Case-insensitive command dispatch.
- Create, show, and drop tables.
- Add and drop columns.
- Insert dictionary-shaped records.
- Select all records or one column.
- Select records using one comparison condition.
- Update one column for a record selected by numeric `id`.
- Delete a specified column's data for a record selected by numeric `id`.
- Value conversion, result formatting, and user-facing error handling.
- Exit using `EXIT`, `QUIT`, Ctrl+C, or end-of-input.

### Outside the current scope

- Full SQL compatibility.
- Multi-table joins and relational constraints.
- Compound `WHERE` expressions using `AND` / `OR`.
- Transactions, concurrent access, and production-grade recovery.
- Authentication, authorization, and network access.
- Whole-row deletion through the current `DELETE` syntax.
- Performance guarantees for large datasets.

## 5. Target Users

- Students learning Python, data structures, file I/O, and basic database concepts.
- Beginners exploring command parsing and modular application design.
- Instructors or evaluators reviewing a small, self-contained programming project.

## 6. Features and Functional Modules

The project is organized around the following functional modules:

| Module | Responsibility | Current operations |
|---|---|---|
| Command-line interface | Reads commands and displays output | Prompt, `HELP`, `EXIT`, `QUIT` |
| Command parser | Recognizes command syntax, validates arguments, and prepares operations | `CREATE`, `SHOW`, `DROP`, `ADD`, `INSERT`, `SELECT`, `UPDATE`, `DELETE` |
| Table management | Manages table and column definitions | Create/list/drop table; add/drop column |
| Data operations | Performs record-level actions | Insert, select, filter, update, remove column data |
| Storage / engine layer | Executes operations and handles persistence | Functions imported from `src.engine.engine`; storage details are implemented there |
| Output and error handling | Converts results and exceptions into console messages | Formatted results and `Error: ...` messages |

## 7. Input and Output Structure

### Example inputs

```text
CREATE TABLE students
SHOW TABLES
ADD COLUMN students name STRING
ADD COLUMN students age INTEGER
INSERT INTO students VALUES {"name": "Kushagra", "age": 18}
SELECT * FROM students
SELECT name FROM students
SELECT * FROM students WHERE age >= 18
UPDATE students SET age = 19 WHERE id = 1
DELETE FROM students COLUMN age WHERE id = 1
DROP COLUMN students name
DROP TABLE students
```

### Example output

```text
TextDB> CREATE TABLE students
Command executed successfully.

TextDB> SELECT * FROM students
1. ...

TextDB> EXIT
Goodbye!
```

Empty results are reported as `No results were found.` where applicable.

## 8. Technologies and Tools

- **Python 3**
- **JSON** for structured data representation and persistence, as implemented by the engine
- **`ast`** — `ast.literal_eval()` for interpreting literal values and insert dictionaries
- **`json`** — JSON serialization for formatted output and storage support
- **`re`** — regular-expression-based command recognition
- **Git and GitHub** — recommended for version control and repository submission
- **`unittest`** — recommended standard-library framework for automated tests

## 9. Architecture
                 User
                  |
                  v
          Command-line interface
                  |
                  v
       DatabaseCommandParser
       - dispatch, validate and convert command
                  |
                  v
         Parsed operation
          (callable)
                  |
                  v
       Engine functions
       src.engine.engine
                  |
                  v
        Table / data logic
                  |
                  v
          JSON persistence
                  |
                  v
        Result or exception
                  |
                  v
       Output formatting / CLI

### Component responsibilities

- **CLI (`main`)**: starts the console, reads input, handles help and exit commands, and prints results.
- **`DatabaseCommandParser`**: maps command keywords to parser methods and coordinates parsing and execution.
- **Parser helpers**: convert values, map column type names, and format returned data.
- **Engine (`src.engine.engine`)**: implements the database operations called by the parser.
- **Storage**: persists data according to the engine's implementation.

The parser returns a callable for each recognized operation. `execute_command()` invokes it, formats the result, and catches exceptions to return readable error messages.

## 10. Workflow

1. The user enters a command at the `TextDB>` prompt.
2. The CLI handles `HELP`, `EXIT`, and `QUIT` directly; other input is sent to the parser.
3. The parser trims the command and identifies its first keyword.
4. The matching parser method validates syntax and extracts table names, fields, operators, and values.
5. The parser returns an operation callable that invokes the relevant engine function.
6. The engine performs the requested operation and interacts with storage as needed.
7. The parser formats the result or returns a readable error.
8. The CLI displays the response and waits for the next command.

## 11. Command Reference

Commands are case-insensitive. Identifiers must begin with a letter or underscore and may then contain letters, digits, or underscores.

| Command | Syntax |
|---|---|
| Create table | `CREATE TABLE table_name` |
| List tables | `SHOW TABLES` |
| Drop table | `DROP TABLE table_name` |
| Add column | `ADD COLUMN table_name column_name type` |
| Drop column | `DROP COLUMN table_name column_name` |
| Insert record | `INSERT INTO table_name VALUES {"field": value}` |
| Select all fields | `SELECT * FROM table_name` |
| Select one field | `SELECT column_name FROM table_name` |
| Filter records | `SELECT * FROM table_name WHERE field operator value` |
| Update a field | `UPDATE table_name SET column = value WHERE id = number` |
| Remove a field value | `DELETE FROM table_name COLUMN column_name WHERE id = number` |
| Help | `HELP` |
| Exit | `EXIT` or `QUIT` |

### Accepted column type names

| Names accepted by parser | Engine enum |
|---|---|
| `INTEGER`, `INT` | `ColumnType.Integer` |
| `DECIMAL`, `FLOAT` | `ColumnType.Decimal` |
| `STRING`, `TEXT` | `ColumnType.String` |

### `SELECT` comparison operators

The parser recognizes `=`, `>`, `<`, `>=`, and `<=` in a single-condition `WHERE` clause.

### Value handling

The parser attempts `ast.literal_eval()` first. It also recognizes lowercase `true`, `false`, and `null`; otherwise, an unparsed value is retained as a string. Insert data must be expressed as a valid Python dictionary literal.

## 12. Installation and Execution

### Prerequisites

- Python 3 installed.
- The project source code, including `src.engine.engine` and the functions/classes imported by the parser.

### Run the application

From the repository root, run the file containing `main()` (for example, `main.py`):
- python Main.py

On systems where Python is invoked as `python3`:
- python3 Main.py

The program displays the TextDB banner and opens the interactive prompt.
> Ensure the engine module is available at the import path used by the parser. The engine's data directory and persistence configuration should be checked in `src/engine/engine.py`.

## 13. Testing

Testing should cover both successful operations and invalid input. If tests are added using `unittest`, run them from the repository root:

python -m unittest discover -s tests -v

Suggested test cases:

| Area | Test |
|---|---|
| Parser | Recognizes each supported command |
| Parser | Rejects empty, unknown, and malformed commands |
| Value conversion | Handles integers, decimals, quoted strings, booleans, and null |
| Table management | Creates, lists, drops, and rejects duplicate/missing tables as appropriate |
| Columns | Adds and drops columns; validates type names |
| Insert | Accepts dictionary input and rejects non-dictionary input |
| Select | Returns all data, a selected column, and matching filtered records |
| Update | Updates the requested field for the specified ID |
| Delete | Removes the specified column data for the specified ID |
| Persistence | Data remains available after restarting, if supported by the engine |
| Error handling | Engine and parsing errors produce understandable messages |

Tests should use a temporary data directory or isolated test database where possible, so test runs do not modify real project data.

## 14. Non-Functional Requirements

The following are project targets to evaluate, not claims of measured performance or production certification.

| Requirement | Target / approach |
|---|---|
| Usability | Provide a consistent prompt, command examples, help text, and readable responses. |
| Reliability | Validate command syntax and handle expected failures without crashing the interactive session. |
| Maintainability | Keep CLI, parser, engine, and storage responsibilities separated into modules. |
| Error handling | Return understandable errors for invalid commands and operation failures; avoid silent failure. |
| Performance | Keep operations responsive for small educational datasets; measure execution time before making quantitative claims. |
| Resource efficiency | Use the Python standard library and avoid unnecessary services or dependencies. |
| Data integrity | Validate values in the engine and use safe persistence practices; further safeguards are future work if not yet implemented. |
| Portability | Use Python 3 and standard-library functionality where possible, with platform-independent paths in storage code. |

## 15. Design Decisions and Rationale

- **Terminal interface:** keeps the project focused on programming, data processing, and database concepts rather than GUI development.
- **Custom command syntax:** provides a practical reason to learn parsing, regular expressions, and validation.
- **JSON-oriented storage:** makes the data human-readable and easy to inspect during development.
- **Engine function separation:** lets the parser translate commands without embedding all data operations in the CLI.
- **Standard-library-first approach:** reduces setup complexity and makes the core implementation easier to run and study.

## 16. Known Limitations

- The parser uses regular expressions and is not a full SQL parser.
- `SELECT ... WHERE` supports one comparison condition only.
- `UPDATE` changes one field and identifies the record using a numeric `id`.
- The current `DELETE` command removes a column value for a record; it does not delete the whole record.
- The insert syntax requires a dictionary literal.
- `HELP` is implemented in the CLI loop, not in the parser's command map.
- Storage guarantees, schema enforcement, ID behavior, and recovery depend on the engine implementation and should be verified there.
- No concurrency, authentication, transaction system, or query optimizer is included in the described implementation.

## 17. Future Enhancements

- Support multiple selected columns, sorting, limits
- Add a separate whole-record deletion command.
- Implement schema constraints
- Improve storage safety
- Add structured logging and automated test coverage.

## 19. References

- Python documentation: https://docs.python.org/3/
- Python `ast` module: https://docs.python.org/3/library/ast.html
- Python `json` module: https://docs.python.org/3/library/json.html
- Python `re` module: https://docs.python.org/3/library/re.html
- Python `unittest` module: https://docs.python.org/3/library/unittest.html
- Git documentation: https://git-scm.com/doc
