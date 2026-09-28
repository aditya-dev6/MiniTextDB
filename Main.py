# ------------------------------------------------------
# COMMAND-LINE INTERFACE
# ------------------------------------------------------
from parser.parser import DatabaseCommandParser


def main():
    parser = DatabaseCommandParser()

    print("======================================")
    print("       TEXT DATABASE CONSOLE")
    print("======================================")
    print("Type EXIT or QUIT to close the database.")
    print("Type HELP to see supported commands.")
    print()

    while True:
        try:
            command = input("TextDB> ").strip()

            if command.upper() in ("EXIT", "QUIT"):
                print("Goodbye!")
                break

            if command.upper() == "HELP":
                print("""
Supported commands:

CREATE TABLE students
SHOW TABLES
DROP TABLE students

ADD COLUMN students name STRING
DROP COLUMN students name

INSERT INTO students VALUES {"name": "Kushagra", "age": 18}

SELECT * FROM students
SELECT name FROM students
SELECT * FROM students WHERE age >= 18

UPDATE students SET age = 19 WHERE id = 1

DELETE FROM students COLUMN age WHERE id = 1

EXIT
""")
                continue

            output = parser.execute_command(command)

            print(output)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == '__main__':
    main()
