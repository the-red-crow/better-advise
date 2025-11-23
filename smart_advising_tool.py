# smart_advising_tool.py
from typing import List, Dict, Optional
import os

from config_manager import ConfigManager
from pdf_parser import PDFParser
from excel_parser import ExcelParser
from excel_exporter import ExcelExporter
from web_crawler import WebCrawler
from prerequisite_checker import PrerequisiteChecker
from dag_generator import DAGGenerator
from plan_generator import PlanGenerator

from semester import Semester
from course import Course
from academic_plan import AcademicPlan


class SmartAdvisingTool:
    """
    Orchestrates the academic advising workflow:
    - Loads configuration
    - Parses inputs (PDF + Excel)
    - Generates a simple course plan
    - Exports to Excel
    """

    def __init__(self, config_file: str = "config.toml"):
        self._config_manager: Optional[ConfigManager] = None
        self._pdf_parser: Optional[PDFParser] = None
        self._excel_parser_gsp: Optional[ExcelParser] = None
        self._excel_parser_4yr: Optional[ExcelParser] = None
        self._excel_exporter: Optional[ExcelExporter] = None

        self._remaining_courses: List[str] = []
        self._completed_courses: List[str] = []
        self._term_hints: Dict[str, List[str]] = {}

        self._output_path: Optional[str] = None
        self._config_file = config_file

    # ---------------------------
    # Initialization
    # ---------------------------
    def initialize_components(self) -> None:
        print("[SmartAdvisingTool] Initializing components...")

        self._config_manager = ConfigManager(self._config_file)
        paths = self._config_manager.get_input_paths()

        # Parsers
        self._pdf_parser = PDFParser(paths.get("degree_pdf_path"))
        self._excel_parser_gsp = ExcelParser(paths.get("graduate_study_plan_path"))
        self._excel_parser_4yr = ExcelParser(paths.get("four_year_schedule_path"))
       

        # Optional: Web crawler + prereq checker (don’t fail run if network/HTML changes)
        catalog_url = self._config_manager.get_setting("course_catalog_url") or "https://catalog.columbusstate.edu/course-descriptions/"
        try:
            self._web_crawler = WebCrawler(catalog_url)
            self._prerequisite_checker = PrerequisiteChecker(self._web_crawler)
        except Exception as e:
            print("[SmartAdvisingTool] Crawler unavailable:", e)
            self._web_crawler = None
            self._prerequisite_checker = None

        self._dag_generator = DAGGenerator()  # start empty; PlanGenerator.set_courses will fill

        # Output
        out_dir = self._config_manager.get_setting("output_directory") or "outputs"
        out_file = self._config_manager.get_setting("output_excel_filename") or "recommended_class_plan.xlsx"
        os.makedirs(out_dir, exist_ok=True)
        self._output_path = os.path.join(out_dir, out_file)

        self._excel_exporter = ExcelExporter(self._output_path)

        # Data caches
        self._remaining_courses = []
        self._completed_courses = []
        self._term_hints = {}

        print("[SmartAdvisingTool] Components initialized.")


    # ---------------------------
    # Input processing
    # ---------------------------
    def process_inputs(self) -> bool:
        print("[SmartAdvisingTool] Processing inputs...")
        try:
            # Parse remaining courses from DegreeWorks PDF
            remaining_from_pdf = []
            if self._pdf_parser and self._pdf_parser.is_valid_pdf():
                remaining_from_pdf = self._pdf_parser.parse_degreeworks_pdf()
                print(f"[SmartAdvisingTool] PDFParser found {len(remaining_from_pdf)} remaining courses")

            # Parse graduate study plan
            remaining_from_gsp = []
            if self._excel_parser_gsp and self._excel_parser_gsp.validate_excel_format():
                remaining_from_gsp = self._excel_parser_gsp.parse_graduate_study_plan()
                print(f"[SmartAdvisingTool] Graduate Study Plan courses: {len(remaining_from_gsp)}")

            # Parse four-year schedule for term hints
            term_hints = {}
            if self._excel_parser_4yr and self._excel_parser_4yr.validate_excel_format():
                term_hints = self._excel_parser_4yr.parse_four_year_schedule()
                print(f"[SmartAdvisingTool] Four-Year Schedule terms: {len(term_hints)}")

            # Merge results
            self._remaining_courses = list(dict.fromkeys(remaining_from_pdf + remaining_from_gsp))
            self._completed_courses = []
            self._term_hints = term_hints

            print(f"[SmartAdvisingTool] Remaining: {len(self._remaining_courses)} | Completed: {len(self._completed_courses)}")
            return True
        except Exception as e:
            print("[SmartAdvisingTool] Error while processing inputs:", e)
            return False

    # ---------------------------
    # Plan generation
    # ---------------------------
    
    def _build_naive_plan(self) -> AcademicPlan:
        """
        Simple, safe, prereq-aware plan:
        - Each course assumed 3 credits.
        - Fill terms (Fall → Spring → Summer → …) respecting max hours.
        - If prereq checker is available, only schedule courses whose prereqs are met
        by previously scheduled terms (acts as 'completed').
        - Stops if no progress is possible to avoid infinite loops.
        """
        max_hours = self._config_manager.get_setting("max_semester_hours") or 15
        HOURS_PER_COURSE = 3

        # Working sets
        remaining = list(self._remaining_courses)  # list of codes
        placed: List[str] = []                     # codes already scheduled (become “completed” for next terms)
        completed_seed = set(self._completed_courses or [])
        plan = AcademicPlan(remaining_courses=self._remaining_courses, completed_courses=self._completed_courses)

        # Term generator (keeps it simple)
        year = 2025
        term_cycle = ["Fall", "Spring", "Summer"]
        term_idx = 0

        def new_semester():
            nonlocal term_idx, year
            name = term_cycle[term_idx]
            sem = Semester(name, year, max_hours)   # no *courses initially
            if not isinstance(sem.courses, list):
                sem.courses = list(sem.courses)
            # advance pointer for next time
            term_idx = (term_idx + 1) % len(term_cycle)
            if term_idx == 1:  # Fall -> Spring rolls year forward
                year += 1
            return sem

        # Plan building loop: keep creating semesters until all courses placed or stuck
        safety_counter = 0
        while remaining and safety_counter < 100:  # guardrail against infinite loops
            safety_counter += 1

            sem = new_semester()
            term_load = 0
            made_progress_this_term = False

            # Use current “completed” pool = original completed + anything placed in prior semesters
            completed_now = completed_seed.union(placed)

            # Greedy pass: try to place courses whose prereqs are satisfied and hours fit
            still_pending: List[str] = []
            for code in remaining:
                # Skip already counted
                if code in placed:
                    continue

                # Check prereqs if checker is available
                if self._use_prereqs and self._prerequisite_checker:
                    try:
                        ok = self._prerequisite_checker.check_prerequisites(code, list(completed_now))
                    except Exception:
                        ok = True  # degrade gracefully
                else:
                    ok = True

                if not ok:
                    still_pending.append(code)
                    continue

                # Hours fit?
                if term_load + HOURS_PER_COURSE > max_hours:
                    still_pending.append(code)
                    continue

                # Add to this semester (as a placeholder Course object)
                c = Course(
                    code=code,
                    name=code,
                    desc=f"Auto-generated placeholder for {code}",
                    hours=HOURS_PER_COURSE,
                    courseTaken=False,
                    letterGrade="",
                    semestersoffered=["Fall", "Spring", "Summer"],
                )
                sem.courses.append(c)
                term_load += HOURS_PER_COURSE
                placed.append(code)
                made_progress_this_term = True

            # If we scheduled anything, add the semester to the plan
            if sem.courses:
                plan.add_semester(sem)

            remaining = [c for c in remaining if c not in placed]

            # If we didn’t place anything in this term and nothing fits (or prereqs block all),
            # break to avoid endless spinning.
            if not made_progress_this_term:
                break

        # Optionally: if anything remains unscheduled, dump them into an “Extra” semester
        # (useful for visibility)
        if remaining:
            extra = Semester("Extra", year, max_hours)
            if not isinstance(extra.courses, list):
                extra.courses = list(extra.courses)
            for code in remaining:
                extra.courses.append(
                    Course(code, code, f"Unscheduled (prereqs/credits)", HOURS_PER_COURSE, False, "", ["Fall","Spring","Summer"])
                )
            plan.add_semester(extra)

        _ = plan.validate_plan()  # harmless check
        return plan


    def generate_course_plan(self) -> str:
        print("[SmartAdvisingTool] Generating course plan...")
        if not self._excel_exporter or not getattr(self._excel_exporter, "_output_path", None):
            raise RuntimeError("Output path not initialized. Check initialize_components().")

        # Prefer the real generator if all parts are ready; otherwise keep your naive fallback
        use_real = all([
            self._dag_generator,
            self._prerequisite_checker,
            self._excel_parser_gsp,
            self._excel_parser_4yr,
            self._pdf_parser,
        ])

        if use_real:
            gen = PlanGenerator(
                dag=self._dag_generator,
                graduate_parser=self._excel_parser_gsp,
                four_year_parser=self._excel_parser_4yr,
                prerequisite_checker=self._prerequisite_checker,
                degreeworks_parser=self._pdf_parser,
                max_hours_per_term=self._config_manager.get_setting("max_semester_hours") or 9,
                start_year_two_digit=25,
            )
            plan = gen.generate_optimal_plan()
        else:
            print("[SmartAdvisingTool] Falling back to naive plan generator.")
            plan = self._build_naive_plan()

        if not self._excel_exporter.export_academic_plan(plan):
            raise RuntimeError("Failed to export academic plan to Excel.")
        print(f"[SmartAdvisingTool] Plan exported: {self._excel_exporter._output_path}")
        return self._excel_exporter._output_path

    # ---------------------------
    # Run + Cleanup
    # ---------------------------
    def run(self) -> bool:
        print("[SmartAdvisingTool] Run started.")
        try:
            self.initialize_components()
            if not self.process_inputs():
                print("[SmartAdvisingTool] Input processing failed.")
                return False

            self.generate_course_plan()
            print("[SmartAdvisingTool] Run finished successfully.")
            return True
        except Exception as e:
            print("[SmartAdvisingTool] Run failed:", e)
            return False
        finally:
            self.cleanup_resources()

    def cleanup_resources(self) -> None:
        print("[SmartAdvisingTool] Cleaning up resources...")
        self._pdf_parser = None
        self._excel_parser_gsp = None
        self._excel_parser_4yr = None
        self._excel_exporter = None
        print("[SmartAdvisingTool] Cleanup complete.")

if __name__ == "__main__":
    SAT = SmartAdvisingTool()
    try:
        while True:
            print("Welcome to Better Advise!\nPlease select from the following menu.")
            print("1.\tRun")
            print("2.\tConfig")
            print("0.\tQuit")
            s = input(">> ").replace(" ", "")
            if(s=="1"):
                SAT.run()
            elif(s=="2"):
                if SAT._config_manager == None:
                    SAT._config_manager = ConfigManager(SAT._config_file)
                while True:
                    print("Pick a config item to change.")
                    print("1. degree_pdf_path")# = "input/allcscourses.pdf"
                    print("2. graduate_study_plan_path")# = "input/Graduate Study Plans -revised.xlsx"
                    print("3. four_year_schedule_path")# = "input/4-year schedule.xlsx"
                    print("4. output_excel_filename")# = "recommended_class_plan.xlsx"
                    print("5. output_directory")# = "outputs/"
                    print("6. course_catalog_url")# = "https://catalog.columbusstate.edu/course-descriptions/"
                    print("7. cache_prerequisites")# = "cacheprerequisites.txt"
                    print("8. prerequiste_cache_path")# = "prerequisites.cache"
                    print("9. max_semester_hours")# = 15"
                    print("0. Back and Save")
                    print("A. Back without Saving")
                    j = input("config>> ").replace(" ", "")
                    if(j == "1"):
                        print("Current value:", SAT._config_manager.get_setting("degree_pdf_path"))
                        SAT._config_manager.update_setting("degree_pdf_path", input("New value: "))
                    elif(j == "2"):
                        print("Current value:", SAT._config_manager.get_setting("graduate_study_plan_path"))
                        SAT._config_manager.update_setting("graduate_study_plan_path", input("New value: "))
                    elif(j == "3"):
                        print("Current value:", SAT._config_manager.get_setting("four_year_schedule_path"))
                        SAT._config_manager.update_setting("four_year_schedule_path", input("New value: "))
                    elif(j == "4"):
                        print("Current value:", SAT._config_manager.get_setting("output_excel_filename"))
                        SAT._config_manager.update_setting("output_excel_filename", input("New value: "))
                    elif(j == "5"):
                        print("Current value:", SAT._config_manager.get_setting("output_directory"))
                        SAT._config_manager.update_setting("output_directory", input("New value: "))
                    elif(j == "6"):
                        print("Current value:", SAT._config_manager.get_setting("course_catalog_url"))
                        SAT._config_manager.update_setting("course_catalog_url", input("New value: "))
                    elif(j == "7"):
                        print("Current value:", SAT._config_manager.get_setting("cache_prerequisites"))
                        SAT._config_manager.update_setting("cache_prerequisites", input("New value: "))
                    elif(j == "8"):
                        print("Current value:", SAT._config_manager.get_setting("prerequiste_cache_path"))
                        SAT._config_manager.update_setting("prerequiste_cache_path", input("New value: "))
                    elif(j == "9"):
                        print("Current value:", SAT._config_manager.get_setting("max_semester_hours"))
                        SAT._config_manager.update_setting("max_semester_hours", int(input("New value: ")))
                    elif(j=="0"):
                        SAT._config_manager.update_config_file()
                        break
                    elif(j.upper()=="A"):
                        break
                    else:
                        print("Invalid Input!")
            elif(s=="0"):
                break
            else:
                print("Invalid Input!")
    except Exception as e:
        print("Better-Advise failed:", e)