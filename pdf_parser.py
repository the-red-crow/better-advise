from typing import List, Dict


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
        self._file_path = file_path
    
    def extract_remaining_courses(self) -> List[str]:
        """
        Extract remaining courses from the PDF.
        
        Returns:
            List[str]: List of remaining course codes
        """
        pass
    
    def parse_degreeworks_pdf(self) -> Dict:
        """
        Parse a DegreeWorks PDF file.
        
        Returns:
            Dict: Dictionary containing parsed PDF data
        """
        pass
    
    def validate_pdf(self) -> bool:
        """
        Validate the PDF file format and content.
        
        Returns:
            bool: True if valid, False otherwise
        """
        pass
