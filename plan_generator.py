from typing import List, Dict
from academic_plan import AcademicPlan
from semester import Semester
from course import Course
from dag_generator import DAGGenerator
from prerequisite_checker import PrerequisiteChecker
from excel_parser import ExcelParser
from web_crawler import WebCrawler
from pdf_parser import PDFParser


class PlanGenerator:
    """
    Generates optimal academic plans based on course requirements and constraints.
    """
    
    def __init__(self, dag: DAGGenerator, graduate_parser: ExcelParser, four_year_parser: ExcelParser, prerequisite_checker: PrerequisiteChecker, degreeworks_parser: PDFParser) -> None:
        """
        Initialize a PlanGenerator object.
        """
        self._remaining_courses = []
        self._completed_courses = []
        self._course_catalog = {}
        self._dag = dag
        self._prerequisite_checker = prerequisite_checker
        self._graduate_parser = graduate_parser
        self._four_year_parser = four_year_parser
        self._degreeworks_parser = degreeworks_parser

    def generate_optimal_plan(self) -> AcademicPlan:
        """
        Generate an optimal academic plan.

        Returns:
            AcademicPlan: The generated academic plan
        """
        semesters = []
        self.populate_remaining_courses("Software Dev")
        self.process_degree_works()

        course_schedule = self._four_year_parser.parse_four_year_schedule()

        courses = self.generate_courses(self._remaining_courses)
        self._dag.set_courses(courses)
        self._dag.build_prerequisite_dag()
        courses_topological_sort = self._dag.topological_sort()

        current_semester_index = 0
        semester_names = ["FA", "SP", "SU"]
        current_year = 25

        while self._remaining_courses:
            semester_name = semester_names[current_semester_index % 3]
            semester = Semester(semester_name, current_year, maxHours=15, courses=[])

            # Build the semester code to check availability (e.g., "FA25", "SP25")
            semester_code = semester_name + str(current_year)

            # Try to add courses to this semester based on topological order
            available_courses = [
                course for course in courses_topological_sort
                if course in self._remaining_courses
                and self._prerequisite_checker.check_prerequisites(course, self._completed_courses)
                and semester_code in course_schedule.get(course, [])
            ]

            for course in available_courses:
                course_obj = courses.get(course)
                if semester.getTotalCredits() + course_obj.getHours() <= semester.maxHours:
                    if semester.addCourse(course_obj):
                        self._remaining_courses.remove(course)
                        self._completed_courses.append(course)

            if semester.courses:  # Only add non-empty semesters
                semesters.append(semester)

            current_semester_index += 1
            if current_semester_index % 3 == 0:
                current_year += 1

        # Create and return the academic plan
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

    def populate_remaining_courses(self, degree: str) -> None:
        self._remaining_courses = self._graduate_parser.parse_graduate_study_plan("Software Dev")

    def generate_courses(self, courses: List[Course]) -> Dict[str, Course]:
        return_courses = {}

        for course in courses:
            course_prereq = self._prerequisite_checker.get_missing_prerequisites(course, [])
            new_course = Course(course, "", 3, False, course_prereq)
            return_courses[course] = new_course

        return return_courses

    def process_degree_works(self):
        required_courses = self._degreeworks_parser.parse_degreeworks_pdf()

        for course in self._remaining_courses[:]:
            if course not in required_courses:
                self._remaining_courses.remove(course)
                self._completed_courses.append(course)
