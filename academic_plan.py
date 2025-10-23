from typing import List, Dict
from semester import Semester


class AcademicPlan:
    """
    Represents an academic plan with semesters and course management.
    """
    
    def __init__(self, remaining_courses: List[str], completed_courses: List[str]):
        """
        Initialize an AcademicPlan object.
        
        Args:
            remaining_courses (List[str]): List of remaining course codes
            completed_courses (List[str]): List of completed course codes
        """
        self._remaining_courses = remaining_courses
        self._completed_courses = completed_courses
        self._semesters = []
        self._total_semesters = 0
    
    def add_semester(self, semester: Semester) -> None:
        """
        Add a semester to the academic plan.
        
        Args:
            semester (Semester): The semester to add
        """
        pass
    
    def get_semester(self, index: int) -> Semester:
        """
        Get a semester by index.
        
        Args:
            index (int): The index of the semester
            
        Returns:
            Semester: The semester at the given index
        """
        pass
    
    def validate_plan(self) -> bool:
        """
        Validate the academic plan for correctness.
        
        Returns:
            bool: True if valid, False otherwise
        """
        pass
    
    def get_plan_summary(self) -> Dict:
        """
        Get a summary of the academic plan.
        
        Returns:
            Dict: Dictionary containing plan summary information
        """
        pass
