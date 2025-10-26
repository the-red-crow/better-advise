from typing import List, Dict
from web_crawler import WebCrawler
from semester import Semester


class PrerequisiteChecker:
    """
    Checks course prerequisites and validates semester plans.
    """
    
    def __init__(self, web_crawler: WebCrawler):
        """
        Initialize a PrerequisiteChecker object.
        
        Args:
            web_crawler (WebCrawler): WebCrawler instance for fetching course data
        """
        self._course_catalog = {}
        self._web_crawler = web_crawler
    
    def check_prerequisites(self, course: str, completed: List[str]) -> bool:
        """
        Check if prerequisites are met for a course.
        """
        prereqs = self._web_crawler.crawl_course_prerequisites(course)
        remaining = [x for x in prereqs if x not in completed] 
        if remaining == [''] or not remaining:
            return True
        else:
            return False
    
    def get_missing_prerequisites(self, course: str, completed: List[str]) -> List[str]:
        """
        Get missing prerequisites for a course.
        """
        prereqs = self._web_crawler.crawl_course_prerequisites(course)
        return [x for x in prereqs if x not in completed]
    
    def validate_semester_plan(self, semester: Semester, completed: List[str]) -> List[str]:
        """
        Validate a semester plan for prerequisite issues.
        
        Args:
            semester (Semester): Semester to validate
            completed (List[str]): List of completed course codes
            
        Returns:
            List[str]: List of prerequisite issues found
        """
        remaining = []
        for course in semester.courses:
            prereqleft = [x for x in course.prereq if x not in completed]
            remaining += prereqleft
        if remaining:
            return remaining
        else:
            return []
    
    def update_course_catalog(self, course_data: Dict) -> None:
        """
        Update the course catalog with new course data.
        
        Args:
            course_data (Dict): Dictionary containing course data
        """
        pass