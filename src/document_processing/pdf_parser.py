import fitz


class PDFParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        """
        Extract complete text from the PDF.
        """
        document = fitz.open(self.file_path)

        full_text = ""

        for page in document:
            full_text += page.get_text("text") + "\n"

        document.close()

        return full_text

    def get_page_count(self):
        """
        Return total number of pages.
        """
        document = fitz.open(self.file_path)

        page_count = len(document)

        document.close()

        return page_count

    def extract_pages(self):
        """
        Extract text page by page while preserving page numbers.
        """

        document = fitz.open(self.file_path)

        pages = []

        for page_number in range(len(document)):
            page = document[page_number]

            text = page.get_text("text").strip()

            pages.append({
                "page_number": page_number + 1,
                "text": text
            })

        document.close()

        return pages