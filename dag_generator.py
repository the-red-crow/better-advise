from typing import List, Dict
from course import Course


class DAGGenerator:
    """
    Generates and manages Directed Acyclic Graph for course prerequisites.
    """
    
    def __init__(self, courses: Dict[str, Course] = {}):
        """
        Initialize a DAGGenerator object.
        
        Args:
            courses (Dict[str, Course]): Dictionary of course codes to Course objects
        """
        self._courses = courses
        self._prerequisite_graph = {}
        self._adjacency_list = {}
    
    def build_prerequisite_dag(self) -> Dict:
        for course in self._courses.values():
            self._prerequisite_graph[course.code] = course.prerequisites
            for prereq in course.prerequisites:
                if prereq not in self._adjacency_list:
                    self._adjacency_list[prereq] = []
                self._adjacency_list[prereq].append(course.code)
        
    
    def topological_sort(self) -> List[str]:
        tsList: List[str] = []
        visited: Dict[str, bool] = {}
        def dfs(course_code: str):
            visited[course_code] = True
            for neighbor in self._prerequisite_graph.get(course_code, []):
                if not visited.get(neighbor, False):
                    dfs(neighbor)
            tsList.append(course_code)
        for course_code in self._courses.keys():
            if not visited.get(course_code, False):
                dfs(course_code)
        return tsList[::-1]
    
    def find_course_levels(self) -> Dict[str, int]:
        levels: Dict[str, int] = {}
        def dfs(course_code: str) -> int:
            if course_code in levels:
                return levels[course_code]
            if not self._prerequisite_graph.get(course_code):
                levels[course_code] = 0
                return 0
            max_level = 0
            for prereq in self._prerequisite_graph[course_code]:
                prereq_level = dfs(prereq)
                max_level = max(max_level, prereq_level + 1)
            levels[course_code] = max_level
            return max_level
        for course_code in self._courses.keys():
            dfs(course_code)
        return levels
    
    def detect_circular_dependencies(self) -> List[str]:
        def dfs(course_code: str, visited: Dict[str, bool], rec_stack: Dict[str, bool]) -> bool:
            visited[course_code] = True
            rec_stack[course_code] = True
            for neighbor in self._prerequisite_graph.get(course_code, []):
                if not visited.get(neighbor, False):
                    if dfs(neighbor, visited, rec_stack):
                        return True
                elif rec_stack.get(neighbor, False):
                    return True
            rec_stack[course_code] = False
            return False
        visited: Dict[str, bool] = {}
        rec_stack: Dict[str, bool] = {}
        circular_courses: List[str] = []
        for course_code in self._courses.keys():
            if not visited.get(course_code, False):
                if dfs(course_code, visited, rec_stack):
                    circular_courses.append(course_code)
        return circular_courses
    
    def get_courses_without_prerequisites(self) -> List[str]:
        no_prereq_courses: List[str] = []
        for course_code, course in self._courses.items():
            if not course.prerequisites:
                no_prereq_courses.append(course_code)
        return no_prereq_courses

    def set_courses(self, courses: Dict[str, Course]):
        self._courses = courses
