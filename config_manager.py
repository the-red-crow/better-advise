from typing import Dict, Any
from pathlib import Path

class ConfigManager:
    """
    Manages configuration settings for the application.
    """
    
    def __init__(self, config_file: str):
        """
        Initialize a ConfigManager object.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self._config_file = config_file
        self._settings = {}
    
    def load_configuration(self) -> Dict:
        """
        Load configuration from file.
        
        Returns:
            Dict: Dictionary containing configuration settings
        """
        pass
    
    def get_setting(self, key: str) -> Any:
        """
        Get a specific configuration setting.
        
        Args:
            key (str): The setting key to retrieve
            
        Returns:
            Any: The setting value
        """
        return self._settings.get(key)
    
    def update_setting(self, key: str, value: Any) -> None:
        """
        Update a configuration setting.
        
        Args:
            key (str): The setting key to update
            value (Any): The new setting value
        """
        self._settings[key] = value
    
    def validate_paths(self) -> bool:
        """
        Validate configuration paths.
        
        Returns:
            bool: True if all paths are valid, False otherwise
        """
        pass
    
    def get_input_paths(self) -> Dict:
        """
        Get input file paths from configuration.
        
        Returns:
            Dict: Dictionary containing input file paths
        """
        pass

    def default_settings(self) -> Dict[str, Any]:
        """
        Set default configuration settings. Required minimum settings.
        """
        return {"degreeworks_pdf_path": None,
        "graduate_study_plan_path" : None,
        "four_year_schedule_path" : None,
        "output_excel_filename": "recommended_class_plan.xlsx",
        "output_directory": "outputs/",
        "course_catalog_url": "https://catalog.columbusstate.edu/course-descriptions/cpsc/",
        "crawler_timeout": 30,
        "crawler_max_retries": 3,
        "cache_prerequisites": None,
        "prerequiste_cache_path": "prerequisites.cache",
        "max_semester_hours": 15
        }

    def check_loaded_settings(self) -> bool:
        """
        Check if all required settings are loaded.

        Returns:
            bool: True if all required settings are present, False otherwise
        """
        default_settings = self.default_settings()
        # TODO: Compare values for same type
        for key in default_settings.keys():
            if key not in self._settings:
                return False
        return True

    def update_config_file(self):
        """
        Update/create configuration file with required minimum settings.
        """