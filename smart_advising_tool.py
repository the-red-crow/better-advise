from config_manager import ConfigManager
from pdf_parser import PDFParser
from excel_parser import ExcelParser
from web_crawler import WebCrawler
from prerequisite_checker import PrerequisiteChecker
from plan_generator import PlanGenerator
from excel_exporter import ExcelExporter
from dag_generator import DAGGenerator


class SmartAdvisingTool:
    """
    Main application class that orchestrates the academic planning process.
    """
    
    def __init__(self, config_file: str):
        """
        Initialize a SmartAdvisingTool object.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self._config_manager = None
        self._pdf_parser = None
        self._four_year_parser = None
        self._graduate_parser = None
        self._web_crawler = None
        self._prerequisite_checker = None
        self._plan_generator = None
        self._excel_exporter = None
        self._dag_generator = None
    
    def initialize_components(self) -> None:
        """
        Initialize all components of the advising tool.
        """
        self._config_manager = ConfigManager()
        self._pdf_parser = PDFParser(self._config_manager.get_setting("degreeworks_pdf_path"))
        self._four_year_parser = ExcelParser(self._config_manager.get_setting("four_year_schedule_path"))
        self._graduate_parser = ExcelParser(self._config_manager.get_setting("degreeworks_excel_path"))
        self._web_crawler = WebCrawler()
        self._prerequisite_checker = PrerequisiteChecker(self._web_crawler)
        self._excel_exporter = ExcelExporter(self._config_manager.get_setting("output_directory") + self._config_manager.get_setting("output_excel_file"))
        self._dag_generator = DAGGenerator()
        self._plan_generator = PlanGenerator(self._dag_generator, self._graduate_parser, self._for_year_parser, self._prerequisite_checker)


    def process_inputs(self) -> bool:
        """
        Process input files and extract course information.
        
        Returns:
            bool: True if processing successful, False otherwise
        """
        pass
    
    def generate_course_plan(self) -> str:
        """
        Generate the course plan and return the output path.
        
        Returns:
            str: Path to the generated course plan file
        """
        pass
    
    def run(self) -> bool:
        """
        Run the complete advising tool process.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def cleanup_resources(self) -> None:
        """
        Clean up resources and close connections.
        """
        pass
