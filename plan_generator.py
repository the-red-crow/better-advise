from typing import List
from academic_plan import AcademicPlan
from semester import Semester
from course import Course
from dag_generator import DAGGenerator
from prerequisite_checker import PrerequisiteChecker
from excel_parser import ExcelParser
from web_crawler import WebCrawler


class PlanGenerator:
    """
    Generates optimal academic plans based on course requirements and constraints.
    """
    
    def __init__(self, dag: DAGGenerator, graduate_parser: ExcelParser, four_year_parser: ExcelParser, prerequisite_checker: PrerequisiteChecker) -> None:
        """
        Initialize a PlanGenerator object.
        
        Args:
            remaining_courses (List[str]): List of remaining course codes
            completed_courses (List[str]): List of completed course codes
        """
        self._remaining_courses = []
        self._completed_courses = []
        self._course_catalog = {}
        self._dag = dag
        self._prerequisite_checker = prerequisite_checker
        self._graduate_parser = graduate_parser
        self._four_year_parser = four_year_parser
        self._schedule_constraints = {}

    def generate_optimal_plan(self) -> AcademicPlan:
        """
        Generate an optimal academic plan.

        Returns:
            AcademicPlan: The generated academic plan
        """
        semesters = []
        self.populate_remaining_courses("Software Dev")

        for course in

        topological_sort = self._dag.topological_sort()

        current_semester_index = 0
        semester_names = ["Fall", "Spring", "Summer"]
        current_year = 1

        while self._remaining_courses:
            semester_name = semester_names[current_semester_index % 3]
            semester = Semester(semester_name, current_year, maxHours=15, courses=[])

            # Try to add courses to this semester based on topological order
            available_courses = [
                course for course in topological_sort
                if course in self._remaining_courses
                   and self._prerequisite_checker.check_prerequisites(course, self._completed_courses)
            ]

            for course in available_courses:
                if semester.getTotalCredits() + self._get_course_credits(course) <= semester.maxHours:
                    course_obj = self._create_course_from_code(course)
                    semester.addCourse(course_obj)
                    self._remaining_courses.remove(course)
                    self._completed_courses.add(course)

            if semester.courses:  # Only add non-empty semesters
                semesters.append(semester)

            current_semester_index += 1
            if current_semester_index % 3 == 0:
                current_year += 1

        plan = AcademicPlan([], list(self._completed_courses))
        for semester in semesters:
            plan.add_semester(semester)

        return plan

    def prioritize_courses_by_dag(self) -> List[str]:
        """
        Prioritize courses based on DAG analysis.
        
        Returns:
            List[str]: List of prioritized course codes
        """
        return self._dag.topological_sort()
    
    def assign_courses_to_semesters(self) -> List[Semester]:
        """
        Assign courses to semesters based on constraints.

        Returns:
            List[Semester]: List of semesters with assigned courses
        """
        semesters = []
        topological_sort = self._dag.topological_sort()

        current_semester = 0
        semester_names = ["Fall", "Spring", "Summer"]
        current_year = 1

        for course in topological_sort:
            if course not in self._remaining_courses:
                continue

            # Create new semester if needed
            while current_semester >= len(semesters):
                sem_name = semester_names[current_semester % 3]
                semesters.append(Semester(sem_name, current_year, maxHours=15, courses=[]))
                if (current_semester + 1) % 3 == 0:
                    current_year += 1

            current_sem = semesters[current_semester]
            course_obj = self._create_course_from_code(course)

            # Try to add course to current semester
            if not current_sem.addCourse(course_obj):
                # If it doesn't fit, move to next semester
                current_semester += 1
                while current_semester >= len(semesters):
                    sem_name = semester_names[current_semester % 3]
                    semesters.append(Semester(sem_name, current_year, maxHours=15, courses=[]))
                    if (current_semester + 1) % 3 == 0:
                        current_year += 1
                semesters[current_semester].addCourse(course_obj)

        return semesters
    
    def optimize_credit_distribution(self) -> None:
        """
        Optimize credit distribution across semesters.
        """
        target_credits = 15
        min_credits = 9

        for semester in self._semesters:
            current_credits = semester.getTotalCredits()

            # If semester has too few credits, try to add courses from remaining
            if current_credits < min_credits and self._remaining_courses:
                # Implementation would add courses if space available
                pass

            # If semester exceeds target, try to move courses to next semester
            if current_credits > target_credits:
                # Implementation would move excess courses
                pass
    
    def handle_prerequisite_conflicts(self) -> bool:
        """
        Handle prerequisite conflicts in the plan.

        Returns:
            bool: True if conflicts resolved, False otherwise
        """
        for course in self._remaining_courses:
            prerequisites = self._prerequisite_checker.get_prerequisites(course)

            for prereq in prerequisites:
                if prereq in self._remaining_courses:
                    # Prerequisite needs to be taken before the course
                    # Reorder semesters if needed
                    pass

        return True

    def populate_remaining_courses(self, degree: str) -> None:
        self._remaining_courses = self._graduate_parser.parse_graduate_study_plan("Software Dev")

    def _get_course_credits(self, course_code: str) -> float:
        """Get credit hours for a course."""
        if course_code in self._course_catalog:
            return self._course_catalog[course_code].hours
        return 3  # Default credit hours

    def _create_course_from_code(self, course_code: str) -> Course:
        """Create a Course object from a course code."""
        if course_code not in self._course_catalog:
            from course import Course
            self._course_catalog[course_code] = Course(course_code, course_code, 3)
        return self._course_catalog[course_code]


test = PlanGenerator(DAGGenerator({}), ExcelParser("input/Graduate Study Plans -revised.xlsx"), ExcelParser("input/4-year schedule.xlsx"), PrerequisiteChecker(WebCrawler()))
test.generate_optimal_plan()
pass