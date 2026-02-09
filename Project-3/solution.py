import os
import sys
import pdfplumber

# paths
CONTENT_DIR = r"D:\Gen AI-course\Assignments\Project-1\content"
PDF_NAME = "Chemistry Questions.pdf"
PDF_PATH = os.path.join(CONTENT_DIR, PDF_NAME)
OUTPUT_PATH = os.path.join(CONTENT_DIR, "output.txt")


def read_specific_page(page_number):
    try:
        # Validate folder
        if not os.path.isdir(CONTENT_DIR):
            raise FileNotFoundError(f"Content folder not found: {CONTENT_DIR}")

        # Validate PDF
        if not os.path.isfile(PDF_PATH):
            raise FileNotFoundError(f"PDF file not found: {PDF_PATH}")

        with pdfplumber.open(PDF_PATH) as pdf:
            total_pages = len(pdf.pages)

            if page_number < 1 or page_number > total_pages:
                raise ValueError(
                    f"Invalid page number. PDF has {total_pages} pages."
                )

            page = pdf.pages[page_number - 1]
            text = page.extract_text()

            if not text:
                text = f"No readable text found on page {page_number}"

        # Write output (creates output.txt if missing)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(f"--- Page {page_number} ---\n{text}")

        print(f"Page {page_number} extracted successfully")
        print(f"Output saved to: {OUTPUT_PATH}")

    except FileNotFoundError as e:
        print(f"File error: {e}")

    except PermissionError:
        print("Permission denied while accessing files")

    except ValueError as e:
        print(f"Input error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    # Command-line argument validation
    if len(sys.argv) != 2:
        print("Usage: python project3.py <page_number>")
        return

    try:
        page_number = int(sys.argv[1])
        read_specific_page(page_number)
    except ValueError:
        print("Page number must be an integer")


if __name__ == "__main__":
    main()
