import os
import sys
import re
import pdfplumber

# paths
CONTENT_DIR = r"D:\Gen AI-course\Assignments\Project-4\content"
PDF_NAME = "Chemistry Questions.pdf"
CONFIG_NAME = "config.txt"

PDF_PATH = os.path.join(CONTENT_DIR, PDF_NAME)
CONFIG_PATH = os.path.join(CONTENT_DIR, CONFIG_NAME)
OUTPUT_PATH = os.path.join(CONTENT_DIR, "output.txt")


def load_regex_from_config():
    if not os.path.isfile(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("regex="):
                regex = line.split("=", 1)[1].strip()
                if not regex:
                    raise ValueError("Regex value is empty in config file")
                return regex

    raise KeyError("Config file does not contain 'regex' key")


def read_page_and_extract(page_number):
    try:
        # Validate folder
        if not os.path.isdir(CONTENT_DIR):
            raise FileNotFoundError(f"Content folder not found: {CONTENT_DIR}")

        # Validate PDF
        if not os.path.isfile(PDF_PATH):
            raise FileNotFoundError(f"PDF file not found: {PDF_PATH}")

        # Load regex
        regex_pattern = load_regex_from_config()
        compiled_regex = re.compile(regex_pattern)

        with pdfplumber.open(PDF_PATH) as pdf:
            total_pages = len(pdf.pages)

            if page_number < 1 or page_number > total_pages:
                raise ValueError(
                    f"Invalid page number. PDF has {total_pages} pages."
                )

            page_text = pdf.pages[page_number - 1].extract_text()

            if not page_text:
                matched_text = "No readable text on this page"
            else:
                matches = compiled_regex.findall(page_text)
                matched_text = "\n".join(matches) if matches else "No matches found"

        # Write output (creates file if missing)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(
                f"--- Page {page_number} | Regex Matches ---\n{matched_text}"
            )

        print("Regex-based extraction completed successfully")
        print(f"Output saved to: {OUTPUT_PATH}")

    except FileNotFoundError as e:
        print(f"File error: {e}")

    except PermissionError:
        print("Permission denied while accessing files")

    except (ValueError, KeyError) as e:
        print(f"Configuration error: {e}")

    except re.error as e:
        print(f"Invalid regex pattern: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python project4.py <page_number>")
        return

    try:
        page_number = int(sys.argv[1])
        read_page_and_extract(page_number)
    except ValueError:
        print("Page number must be an integer")


if __name__ == "__main__":
    main()
