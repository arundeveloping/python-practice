import os
import pdfplumber

# base content directory
BASE_CONTENT_DIR = r"D:\Gen AI-course\Assignments\Project-2\content"

def process_pdf_folder(folder_path):
    """
    Reads all PDF files in a folder and writes extracted text to output.txt
    """
    try:
        # check if folder exists
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        pdf_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(".pdf")
        ]

        # check if PDFs exist
        if not pdf_files:
            print(f"No PDF files found in: {folder_path}")
            return

        extracted_text = ""

        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            print(f"Reading: {pdf_path}")

            with pdfplumber.open(pdf_path) as pdf:
                for page_no, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
                    else:
                        print(f"No text on page {page_no} in {pdf_file}")

        # output file path
        output_path = os.path.join(folder_path, "output.txt")

        # write output (creates file if missing)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"Output written to: {output_path}\n")

    except FileNotFoundError as e:
        print(f"{e}")

    except PermissionError:
        print(f"Permission denied for folder: {folder_path}")

    except Exception as e:
        print(f"Unexpected error in {folder_path}: {e}")


def main():
    try:
        # check base content folder
        if not os.path.isdir(BASE_CONTENT_DIR):
            raise FileNotFoundError(
                f"Base content folder not found: {BASE_CONTENT_DIR}"
            )

        # traverse sub-folders
        for sub_folder in os.listdir(BASE_CONTENT_DIR):
            sub_folder_path = os.path.join(BASE_CONTENT_DIR, sub_folder)

            if os.path.isdir(sub_folder_path):
                print(f"📂 Processing folder: {sub_folder}")
                process_pdf_folder(sub_folder_path)

    except FileNotFoundError as e:
        print(f"{e}")

    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
