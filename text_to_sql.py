
import os
import re
import sqlite3

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# 1. GEMINI CONFIGURATION
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"
DATABASE = "sales.db"


# ==========================================
# 2. TERMINAL COLORS
# ==========================================

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"


# ==========================================
# 3. GET DATABASE SCHEMA
# ==========================================

def get_schema():

    conn = sqlite3.connect(
        f"file:{DATABASE}?mode=ro", uri=True
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    schema = []

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"PRAGMA table_info('{table_name}')"
        )

        columns = cursor.fetchall()

        column_names = [
            column[1] for column in columns
        ]

        schema.append(
            f"{table_name}: {', '.join(column_names)}"
        )

    conn.close()

    return "\n".join(schema)


# ==========================================
# 4. GENERATE SQL USING GEMINI
# ==========================================

def generate_sql(question):

    schema = get_schema()

    prompt = f"""
You are an expert SQLite SQL assistant.

DATABASE SCHEMA:
{schema}

TASK:
Convert the user's English question into a valid SQLite query.

RULES:
1. Generate only SELECT queries.
2. Use only existing tables and columns.
3. Return ONLY SQL.
4. Do not include Markdown.
5. Do not include explanations.
6. Never generate INSERT, UPDATE, DELETE or DROP.
7. Add LIMIT 50 for non-aggregate queries.

USER QUESTION:
{question}
"""

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=prompt,

        config=types.GenerateContentConfig(

            thinking_config=types.ThinkingConfig(
                thinking_level="minimal"
            ),

            max_output_tokens=128
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    sql = response.text.strip()

    # Remove Markdown code fences

    sql = re.sub(
        r"^```(?:sql)?\s*",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()


# ==========================================
# 5. EXECUTE SQL QUERY SAFELY
# ==========================================

def run_query(sql):

    conn = sqlite3.connect(
        f"file:{DATABASE}?mode=ro", uri=True
    )

    allowed_actions = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION,
        getattr(sqlite3, "SQLITE_RECURSIVE", -1)
    }

    def authorize(action, arg1, arg2, database, trigger):

        if action in allowed_actions:
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    conn.set_authorizer(authorize)

    try:

        sql = sql.strip()

        if not re.match(r"^SELECT\b", sql, re.IGNORECASE):
            raise ValueError("Only SELECT queries are allowed.")

        cursor = conn.cursor()

        cursor.execute(sql)

        results = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        return columns, results

    finally:

        conn.close()


# ==========================================
# 6. DISPLAY RESULTS
# ==========================================

def display_results(columns, results):

    if not results:

        print(YELLOW + "No records found." + RESET)

        return

    widths = []

    for index, column in enumerate(columns):

        width = max(
            len(str(column)),
            max(len(str(row[index])) for row in results)
        )

        widths.append(width)

    separator = "+-" + "-+-".join(
        "-" * width for width in widths
    ) + "-+"

    print(GREEN + separator + RESET)

    header = "| " + " | ".join(
        str(column).ljust(widths[index])
        for index, column in enumerate(columns)
    ) + " |"

    print(CYAN + header + RESET)

    print(GREEN + separator + RESET)

    for row in results:

        row_data = "| " + " | ".join(
            str(value).ljust(widths[index])
            for index, value in enumerate(row)
        ) + " |"

        print(row_data)

    print(GREEN + separator + RESET)

    print(
        GREEN +
        f"Total records: {len(results)}" +
        RESET
    )


# ==========================================
# 7. INTERACTIVE CONSOLE
# ==========================================

def main():

    print("\n" + CYAN + "=" * 55 + RESET)

    print(
        CYAN +
        "       GEMINI TEXT-TO-SQL ASSISTANT" +
        RESET
    )

    print(CYAN + "=" * 55 + RESET)

    print("\nWelcome! Ask questions about your sales database.")

    print("\nAVAILABLE COMMANDS:")

    print("schema - View database structure")
    print("help   - View available commands")
    print("quit   - Exit application")
    print("exit   - Exit application")

    while True:

        question = input(
            "\n" + CYAN + "Enter your question: " + RESET
        ).strip()

        if not question:

            print(RED + "Please enter a question." + RESET)

            continue

        # Exit

        if question.lower() in ["quit", "exit"]:

            print(GREEN + "\nThank you! Goodbye!" + RESET)

            break

        # Help

        if question.lower() == "help":

            print("\nAvailable commands:")
            print("schema - View database structure")
            print("quit   - Exit application")

            continue

        # Schema

        if question.lower() == "schema":

            print("\n" + CYAN + "DATABASE SCHEMA:" + RESET)

            try:
                print(get_schema())

            except Exception as error:
                print(RED + f"Error: {error}" + RESET)

            continue

        # Generate SQL

        try:

            print("\nGenerating SQL using Gemini...")

            sql_query = generate_sql(question)

            print("\n" + GREEN + "GENERATED SQL:" + RESET)

            print(sql_query)

            # Execute query

            print("\nExecuting SQL query...")

            result = run_query(sql_query)

            if result is not None:

                columns, rows = result

                print("\n" + GREEN + "QUERY RESULTS:" + RESET)

                display_results(columns, rows)

        except Exception as error:

            print(RED + f"\nError: {error}" + RESET)

            print(YELLOW + "Please try again." + RESET)


# ==========================================
# 8. START APPLICATION
# ==========================================

if __name__ == "__main__":

    main()
