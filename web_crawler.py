from typing import List, Dict
import requests


class WebCrawler:
    """
    Web crawler for extracting course information from university websites.
    """
    
    def __init__(self, base_url: str):
        """
        Initialize a WebCrawler object.
        
        Args:
            base_url (str): Base URL for the university website
        """
        self._base_url = base_url
        self._session = requests.Session()
    
    def crawl_course_prerequisites(self, course_code: str) -> List[str]:
        """
        Crawl prerequisites for a specific course.
        
        Args:
            course_code (str): The course code to crawl prerequisites for
            
        Returns:
            List[str]: List of prerequisite course codes
        """
        pass
    
    def get_course_description(self, course_code: str) -> str:
        """
        Get course description from the web.
        
        Args:
            course_code (str): The course code to get description for
            
        Returns:
            str: Course description
        """
        pass
    
    def batch_crawl_prerequisites(self, courses: List[str]) -> Dict:
        """
        Crawl prerequisites for multiple courses in batch.
        
        Args:
            courses (List[str]): List of course codes to crawl
            
        Returns:
            Dict: Dictionary mapping course codes to their prerequisites
        """
        pass
    
    def validate_connection(self) -> bool:
        """
        Validate the web connection.
        
        Returns:
            bool: True if connection is valid, False otherwise
        """
        pass
    
    def close_session(self) -> None:
        """
        Close the web session.
        """
        pass
