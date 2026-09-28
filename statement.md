# TextDB — Project Statement

## 1. Project Title

**TextDB — Mini CLI-Based Database**

## 2. Problem Statement

In beginner programming exercises, data is often stored in temporary variables or manipulated through standalone file operations. This provides limited practice with the broader workflow of a database system: interpreting user commands, validating inputs, managing tables and records, persisting data, and returning meaningful results.

TextDB proposes a small, terminal-based database application in Python. It allows users to issue a defined set of database-like commands through an interactive console. The application parses those commands and delegates operations to an engine that manages table and data operations with JSON-oriented persistence.

## 3. Project Objectives

- Apply Python programming concepts to a practical data-management application.
- Design and implement a custom command interface and parser.
- Support basic table and record operations through terminal commands.
- Practice modular architecture by separating the CLI, parser, engine, and storage responsibilities.
- Use Python data structures, JSON handling, regular expressions, type conversion, and exception handling.
- Document and test the application as a structured academic project.

## 4. Scope

### In Scope

The current project includes an interactive terminal console and parser for these operations:

- Create, list, and drop tables.
- Add and drop columns.
- Insert records supplied as dictionary literals.
- Select all fields or one field.
- Filter records using a single comparison condition.
- Update one field for a record identified by numeric ID.
- Remove a specified column value for a record identified by numeric ID.
- Display help, format results, report errors, and exit the console.

The parser recognizes `INTEGER`/`INT`, `DECIMAL`/`FLOAT`, and `STRING`/`TEXT` column type names. The engine is responsible for the underlying operation and persistence behavior.

### Out of Scope for the Current Version

The current version is not intended to provide full SQL compatibility, multi-table joins, compound query conditions, transactions, concurrent clients, authentication, or production-grade database recovery. Whole-row deletion is also not provided by the currently shown `DELETE` syntax.

## 5. Target Users

- Students learning Python and foundational database concepts.
- Beginners interested in command parsing, data structures, file handling, and modular software design.
- Academic evaluators reviewing a practical programming project.

## 6. High-Level Features

1. **Interactive CLI:** A terminal prompt accepts commands and displays results.
2. **Command parsing:** The parser identifies command keywords, validates syntax, extracts arguments, and converts values.
3. **Table management:** Users can create, list, drop tables, and add or drop columns.
4. **Record operations:** Users can insert, select, filter, update, and remove column data for identified records.
5. **Data handling:** The engine performs operations and uses the project's JSON-oriented storage implementation.
6. **Output and error handling:** Results are formatted for the console, while exceptions are presented as readable error messages.

## 7. High-Level Workflow

User enters command
        |
        v
CLI receives input
        |
        v
Parser identifies and validates syntax
        |
        v
Parser returns an operation
        |
        v
Engine performs the requested action
        |
        v
Storage is read or updated as needed
        |
        v
Result/error is formatted and displayed

## 8. Expected Outcome

The expected outcome is a runnable Python command-line prototype that demonstrates a complete command-to-operation workflow for a small set of database-like tasks. The project also serves as a learning exercise in parsing, modular design, data handling, validation, and testing.
