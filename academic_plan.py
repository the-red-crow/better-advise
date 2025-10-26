from typing import List, Dict
from semester import Semester
from course import Course
from web_crawler import WebCrawler
from prerequisite_checker import PrerequisiteChecker


class AcademicPlan:
    """
    Represents an academic plan with semesters and course management.
    """

    def __init__(self, remaining_courses: List[str], completed_courses: List[str]):
        self._remaining_courses = set(remaining_courses)
        self._completed_courses = set(completed_courses)
        self._semesters: List[Semester] = []
        self._total_semesters = 0
        self._last_errors: List[str] = []

    def add_semester(self, semester: Semester) -> None:
        """Add a semester to the academic plan."""
        self._semesters.append(semester)
        self._total_semesters = len(self._semesters)

    def get_semester(self, index: int) -> Semester:
        """Get a semester by index."""
        if 0 <= index < len(self._semesters):
            return self._semesters[index]
        raise IndexError(f"Semester index {index} out of range")

    def validate_plan(self) -> bool:
        """
        Validate the academic plan:
          - No duplicate course codes across semesters
          - All remaining courses are scheduled
          - Completed courses are not re-scheduled
          - No semester exceeds maxHours
        """
        errors = []
        scheduled_codes = []
        prereq_errors = []
        wc = WebCrawler()
        pc = PrerequisiteChecker(wc)
        for sem in self._semesters:
            # check credit hours
            if sem.getTotalCredits() > sem.maxHours:
                errors.append(
                    f"{sem.name} {sem.year} exceeds max hours ({sem.getTotalCredits()} > {sem.maxHours})"
                )

            # collect codes
            for c in sem.courses:
                scheduled_codes.append(c.code)

            prereq_errors += pc.validate_semester_plan(sem)
            
        # check duplicates
        if len(scheduled_codes) != len(set(scheduled_codes)):
            errors.append("Duplicate course(s) found across semesters")

        # check remaining
        if not self._remaining_courses.issubset(set(scheduled_codes)):
            errors.append("Some remaining courses are not scheduled")

        # check completed
        overlap = self._completed_courses.intersection(set(scheduled_codes))
        if overlap:
            errors.append(f"Completed courses scheduled again: {list(overlap)}")
        
        if prereq_errors:
            errors.append(f"Prerequisites need to be taken before some courses.")

        self._last_errors = errors
        return len(errors) == 0

    def get_plan_summary(self) -> Dict:
        """Get a summary of the academic plan."""
        scheduled_codes = [c.code for s in self._semesters for c in s.courses]
        total_hours = sum(s.getTotalCredits() for s in self._semesters)

        return {
            "total_semesters": self._total_semesters,
            "total_hours": total_hours,
            "completed_courses": list(self._completed_courses),
            "remaining_courses": list(self._remaining_courses),
            "scheduled_courses": scheduled_codes,
            "is_valid": self.validate_plan(),
            "errors": self._last_errors,
        }
