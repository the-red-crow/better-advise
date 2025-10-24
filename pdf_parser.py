import os
from typing import List, Dict
from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PdfReadError


class PDFParser:
    """
    Parses PDF files to extract course information.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize a PDFParser object.
        
        Args:
            file_path (str): Path to the PDF file to parse
        """
        self._file_path = Path(file_path)
    
    def extract_remaining_courses(self, text: List[str]) -> List[str]:
        """
        Extract remaining courses from the PDF.
        
        Returns:
            List[str]: List of remaining course codes
        """
        remaining_courses = []
        for line in text:
            pass

        return remaining_courses
    
    def parse_degreeworks_pdf(self) -> List:
        """
        Parse a DegreeWorks PDF file.
        
        Returns:
            Dict: Dictionary containing parsed PDF data
        """
        self.validate_pdf()
        pages = self.extract_text()
        remaining_courses = self.extract_remaining_courses(pages)

    def extract_text(self) -> Dict:
        pages = []
        reader = PdfReader(str(self._file_path))

        for page in reader.pages:
            pages.append(page.extract_text())

        return pages

    def is_valid_pdf(self) -> bool:
        if not self._file_path.exists() or not self._file_path.is_file():
            return False

        try:
            reader = PdfReader(str(self._file_path))
        except PdfReadError:
            return False
        except Exception:
            return False

        pages = getattr(reader, "pages", None)
        if pages is None or len(pages) == 0:
            return False

        # Successfully opened and has pages — consider valid (text extraction may fail for image-only PDFs)
        return True

    def validate_pdf(self):
        """
        Validate the PDF file format and content.
        
        Returns:
            Raises error
        """
        if not self.is_valid_pdf():
            raise PdfReadError


# Test code
# test = PDFParser("input/cs.pdf")
test = PDFParser("input/chem.pdf")
test.parse_degreeworks_pdf()
