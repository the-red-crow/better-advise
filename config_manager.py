import os
from typing import Dict, Any
from pathlib import Path
import sys
if sys.version_info >= (3, 11):
    import tomllib as tomli
else:
    import tomli

class ConfigManager:
    """
    Manages configuration settings for the application.
    """
    
    def __init__(self, config_file: str = "config.toml"):
        """
        Initialize a ConfigManager object.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self._config_file = Path(config_file)
        self._settings = self.load_configuration()
        self.check_loaded_settings()
    
    def load_configuration(self) -> Dict:
        """
        Load configuration from file.
        
        Returns:
            Dict: Dictionary containing configuration settings
        """
        self.validate_path()

        with open(self._config_file, "rb") as f:
            loaded_settings = tomli.load(f)

        return loaded_settings

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
    
    def validate_path(self):
        """
        Validate configuration paths. If it doesn't exist, create it.
        """
        if not os.path.exists(self._config_file):
            self._settings = self.default_settings()
            self.update_config_file()

    
    def get_input_paths(self) -> Dict:
        """
        Get input file paths from configuration.
        
        Returns:
            Dict: Dictionary containing input file paths
        """
        return {
            "degree_pdf_path": self.get_setting("degree_pdf_path"),
            "graduate_study_plan_path": self.get_setting("graduate_study_plan_path"),
            "four_year_schedule_path": self.get_setting("four_year_schedule_path"),
        }

    def default_settings(self) -> Dict[str, Any]:
        """
        Set default configuration settings. Required minimum settings.
        """
        #  TODO: Need to finalize the settings
        return {"degree_pdf_path": "input/degreeworks.pdf",
        "graduate_study_plan_path" : "input/graduate_study_plan.xlsx",
        "four_year_schedule_path" : "input/four_year_schedule.xlsx",
        "output_excel_filename": "recommended_class_plan.xlsx",
        "output_directory": "outputs/",
        "course_catalog_url": "https://catalog.columbusstate.edu/course-descriptions/",
        "cache_prerequisites": "cacheprerequisites.txt",
        "prerequiste_cache_path": "prerequisites.cache",
        "max_semester_hours": 15
        }

    def check_loaded_settings(self):
        """
        Check if all required settings are loaded.
        """
        config_needs_update = False
        default_settings = self.default_settings()

        # TODO: Compare values for same type
        for key in default_settings.keys():
            default_value = default_settings[key]

            try:
                current_value = self._settings[key]
            except KeyError:
                # Adds the missing setting
                config_needs_update = True
                self.update_setting(key, default_value)
                continue

            # If the user had a bad setting in the config file
            if type(current_value) != type(default_value):
                raise ConfigError(
                    f"Invalid setting type for {key}: {current_value!r} "
                    f"(expected {type(default_value).__name__}). "
                    f"Please fix {self._config_file}"
                )

        if config_needs_update:
            self.update_config_file()

        return True


    def update_config_file(self):
        """
        Update/create configuration file with required minimum settings.
        """
        with open(self._config_file, "w") as f:
            for key, value in self._settings.items():
                write_str = f"{key} = "

                if type(value) == str:
                    write_str += f"\"{value}\"\n"
                else:
                    write_str += f"{value}\n"
                f.write(write_str)

class ConfigError(ValueError):
    """Raised for invalid configuration settings."""
    pass
