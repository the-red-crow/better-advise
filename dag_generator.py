from typing import List, Dict
from course import Course


class DAGGenerator:
    """
    Generates and manages Directed Acyclic Graph for course prerequisites.
    """
    
    def __init__(self, courses: Dict[str, Course]):
        """
        Initialize a DAGGenerator object.
        
        Args:
            courses (Dict[str, Course]): Dictionary of course codes to Course objects
        """
        self._courses = courses
        self._prerequisite_graph = {}
        self._adjacency_list = {}
    
    def build_prerequisite_dag(self) -> Dict:
        """
        Build the prerequisite DAG from courses.
        
        Returns:
            Dict: The prerequisite DAG structure
        """
        pass
    
    def topological_sort(self) -> List[str]:
        """
        Perform topological sort on the prerequisite graph.
        
        Returns:
            List[str]: List of course codes in topological order
        """
        pass
    
    def find_course_levels(self) -> Dict[str, int]:
        """
        Find the level of each course in the prerequisite hierarchy.
        
        Returns:
            Dict[str, int]: Dictionary mapping course codes to their levels
        """
        pass
    
    def detect_circular_dependencies(self) -> List[str]:
        """
        Detect circular dependencies in the prerequisite graph.
        
        Returns:
            List[str]: List of courses involved in circular dependencies
        """
        pass
    
    def get_courses_without_prerequisites(self) -> List[str]:
        """
        Get courses that have no prerequisites.
        
        Returns:
            List[str]: List of course codes without prerequisites
        """
        pass
