import os
import pdfplumber

# paths
CONTENT_DIR = r"D:\Gen AI-course\Assignments\Project-1\content"
PDF_NAME = "Chemistry Questions.pdf"
PDF_PATH = os.path.join(CONTENT_DIR, PDF_NAME)
OUTPUT_PATH = os.path.join(CONTENT_DIR, "output.txt")

try:
    #Check if content folder exists
    if not os.path.isdir(CONTENT_DIR):
        raise FileNotFoundError(f"Content folder not found: {CONTENT_DIR}")

    #Check if PDF file exists
    if not os.path.isfile(PDF_PATH):
        raise FileNotFoundError(f"PDF file not found: {PDF_PATH}")

    #Read PDF
    text = ""
    with pdfplumber.open(PDF_PATH) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                print(f"No text found on page {page_no}")

    #Write output (creates file if not present)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)

    print("PDF text extracted successfully")
    print(f"Output saved to: {OUTPUT_PATH}")

except FileNotFoundError as e:
    print(f" File error: {e}")

except PermissionError:
    print("Permission denied while accessing files")

except Exception as e:
    print(f" Unexpected error: {e}")
