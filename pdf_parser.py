import os
from typing import List, Dict
from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import re

class PDFParser:
    """
    Parses PDF files to extract course information.
    Give it the name of the pdf on init and call obj.parse_degreeworks_pdf() to recieve a List[str] of all courses needed to be taken.
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
            match = re.search(r'Still needed: \d Credits in (.+)', line)
            second_match = re.search(r'Still needed: \d Class in (.+)', line)
            if match or second_match:
                if match:
                    line = match.group(1)
                if second_match:
                    line = second_match.group(1)
                course_prefix = ""

                for word in line.split(" "):
                    # Matches 4 capital character course prefix
                    if re.match(r'^[A-Z]{4}', word):
                        course_prefix = word
                    # Matches 4 digits or 4 digits Course number with capital 5th character
                    elif re.match(r'^[0-9]{4}[A-Z]?', word):
                        remaining_courses.append(course_prefix + " " + word)

        return remaining_courses
    
    def parse_degreeworks_pdf(self) -> List[str]:
        """
        Parse a DegreeWorks PDF file.
        
        Returns:
            Dict: Dictionary containing parsed PDF data
        """
        self.validate_pdf()
        pages = self.extract_text()
        pages = self.merge_course_requirements(pages.split("\n"))
        remaining_courses = self.extract_remaining_courses(pages)

        return remaining_courses

    def extract_text(self) -> str:
        pages = []
        reader = PdfReader(str(self._file_path))

        pages = ""
        for page in reader.pages:
            pages += page.extract_text(extraction_mode="layout") + "\n"

        pages = self.clean_text(pages)

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

    def clean_text(self, text: str) -> str:
        modified_text = ""
        lines = text.split("\n")
        for line in lines:
            #Replaces multiple spaces into a single one
            line = re.sub(r'[ \t]+', ' ', line)
            line = line.strip()
            if line:
                modified_text += line + "\n"
        return modified_text

    def merge_course_requirements(self, lines) -> List[str]:
        """
        Fixes the issue where each section might span multiple lines.
        """
        merged = []
        buffer = ""

        for line in lines:
            line = line.strip()

            # If line contains "Still needed:", start a new requirement
            if "Still needed:" in line:
                # Save previous buffer if exists
                if buffer:
                    merged.append(buffer)
                buffer = line

            # If buffer exists and line looks like a continuation (starts with "or" or course code)
            elif buffer and (line.startswith("or ")
                             # Matches course prefix and first digit, Ex: PHYS 1
                             or re.match(r'^[A-Z]{4}\s+\d', line)
                             # Matches course number 4 numbers or 4 numbers and a letter, Ex: 1030K 1031
                             or re.match(r'^([0-9]{4} |[0-9]{4}[A-Z] )', line)):
                buffer += " " + line

            # Otherwise, it's a new line (not a continuation)
            else:
                if buffer:
                    merged.append(buffer)
                    buffer = ""

        # Don't forget the last buffer
        if buffer:
            merged.append(buffer)

        return merged

    def sample_output_1(self) -> List[str] :
        """
        From personal degreeworks with chemistry major
        """
        return ['PERS1506', 'RIVR1101', 'RIVR2101', 'ANTH1145', 'ASTR1105', 'ASTR1106', 'ASTR1305', 'ASTR1112',
                'ASTR1112L', 'BIOL1011K', 'BIOL1125', 'BIOL1012K', 'BIOL1215K', 'BIOL1225K', 'CHEM1151', 'CHEM1151L',
                'CHEM1152', 'CHEM1152L', 'CHEM1211', 'CHEM1211L', 'CHEM1212', 'CHEM1212L', 'CHEM1212', 'CPSC1105',
                'CPSC1301', 'CSCI1301K', 'ENVS1105', 'ENVS1105L', 'ENVS1205K', 'ENVS2202', 'GEOL2215', 'GEOL1110',
                'GEOL1121', 'GEOL1121H', 'GEOL1121L', 'GEOL1122', 'GEOL1322', 'GEOL2225', 'PHYS1111', 'PHYS1311',
                'PHYS1112', 'PHYS1312', 'PHYS1125@', 'PHYS1325', 'PHYS2211', 'PHYS2311', 'PHYS2212', 'PHYS2312',
                'PHYS2212K', 'CHEM1211', 'CHEM1211L', 'CHEM1211', 'CHEM1212', 'CHEM1212L', 'CHEM1212', 'PHYS1111',
                'PHYS1311', 'PHYS2211', 'PHYS2311', 'PHYS2211K']

    def sample_output_2(self) -> List[str] :
        """
        From personal degreeworks with CS graduate major. Contains only electives and Exit exam
        """
        return ['CPSC6985', 'CPSC6986', 'CPSC6127', 'CPSC6698', 'CPSC6103', 'CPSC6105', 'CPSC6106', 'CYBR6126', 'CPSC6000']
