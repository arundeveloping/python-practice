import os
import re
import sys
import pdfplumber
import mysql.connector
from mysql.connector import Error

# Paths
CONTENT_DIR = r"D:\Gen AI-course\Assignments\Project-5\content"
PDF_NAME = "Chemistry Questions.pdf"
CONFIG_NAME = "config.txt"

PDF_PATH = os.path.join(CONTENT_DIR, PDF_NAME)
CONFIG_PATH = os.path.join(CONTENT_DIR, CONFIG_NAME)

# DB Config
DB_CONFIG = {
    "host": "",
    "user": "root",
    "password": "root",
    "database": "question_bank"
}


def load_regex_from_config():
    if not os.path.isfile(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("regex="):
                regex = line.split("=", 1)[1].strip()
                if not regex:
                    raise ValueError("Regex value is empty in config file")
                return regex

    raise KeyError("Config file does not contain 'regex' key")


def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if not conn.is_connected():
            raise ConnectionError("Could not connect to database")
        return conn
    except Error as e:
        raise ConnectionError(f"Database connection failed: {e}")


def insert_question(cursor, subject, chapter, question_text, answer_options):
    try:
        sql = """
        INSERT INTO questions (subject_name, chapter_name, question_text, answer_options)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (subject, chapter, question_text, answer_options))
    except Error as e:
        raise RuntimeError(f"Failed to insert question: {e}")


def extract_and_store():
    # Validate folder
    if not os.path.isdir(CONTENT_DIR):
        raise FileNotFoundError(f"Content folder not found: {CONTENT_DIR}")

    # Validate PDF
    if not os.path.isfile(PDF_PATH):
        raise FileNotFoundError(f"PDF file not found: {PDF_PATH}")

    # Load regex
    regex_pattern = load_regex_from_config()
    try:
        compiled_regex = re.compile(regex_pattern, re.MULTILINE | re.DOTALL)
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}")

    # Connect to DB
    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        # Check table exists
        cursor.execute("SHOW TABLES LIKE 'questions'")
        if cursor.fetchone() is None:
            raise RuntimeError("Table 'questions' does not exist in database")

        # Read PDF
        all_text = ""
        with pdfplumber.open(PDF_PATH) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += "\n" + text

        if not all_text.strip():
            print("No readable text found in PDF")
            return

        # Extract questions
        matches = compiled_regex.findall(all_text)

        if not matches:
            print("No questions matched the regex.")
            return

        # Example metadata (you can make this dynamic later)
        subject_name = "Chemistry"
        chapter_name = "Unknown"

        inserted = 0

        for match in matches:
            # If regex has groups, match may be tuple
            if isinstance(match, tuple):
                question_text = match[0]
            else:
                question_text = match

            answer_options = ""  # You can extend regex to capture options too

            insert_question(cursor, subject_name, chapter_name, question_text.strip(), answer_options)
            inserted += 1

        conn.commit()
        print(f"✅ Successfully inserted {inserted} questions into database.")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def main():
    try:
        extract_and_store()
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except ConnectionError as e:
        print(f"Database error: {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")
    except ValueError as e:
        print(f"Configuration/Regex error: {e}")
    except Error as e:
        print(f"MySQL error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
