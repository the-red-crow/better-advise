from typing import Dict


class ExcelParser:
    """
    Parses Excel files to extract course schedule information.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize an ExcelParser object.
        
        Args:
            file_path (str): Path to the Excel file to parse
        """
        self._file_path = file_path
    
    def parse_graduate_study_plan(self) -> Dict:
        """
        Parse a graduate study plan Excel file.
        
        Returns:
            Dict: Dictionary containing parsed graduate study plan data
        """
        pass
    
    def parse_four_year_schedule(self) -> Dict:
        """
        Parse a four-year schedule Excel file.
        
        Returns:
            Dict: Dictionary containing parsed four-year schedule data
        """
        pass
    
    def get_course_schedule_info(self) -> Dict:
        """
        Get course schedule information from Excel file.
        
        Returns:
            Dict: Dictionary containing course schedule information
        """
        pass
    
    def validate_excel_format(self) -> bool:
        """
        Validate the Excel file format.
        
        Returns:
            bool: True if valid format, False otherwise
        """
        pass
