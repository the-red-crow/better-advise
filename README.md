# Smart Planning Tool

An intelligent academic advising tool that automatically generates optimized course schedules for university students by analyzing degree requirements, prerequisites, and course availability.

## Contributors
Team 3 – CPSC 6177

- Syed Osama Ali
- Dheeraj Kolla
- John Morales 
- Jitha Priya 
- Astrea Rojas 
  
## Purpose

**Problem**: Academic advising—especially properly planning courses across semesters to ensure students graduate on time—requires significant time and effort from both students and faculty. Students often make enrollment mistakes, such as:
- Enrolling in classes without considering prerequisite requirements
- Not accounting for course availability across semesters
- Missing required core courses for their degree

**Solution**: Better Advise is a Python-based smart class planning tool designed to automate this process. It generates a recommended class plan for students to follow until graduation by analyzing three key inputs: degree requirements, graduate study plans, and course scheduling information.

**Key Benefits**:
- Automated course scheduling without manual intervention
- Prerequisite-aware planning
- Semester credit hour capacity management
- Web integration for real-time course data

## Overview

Better Advise streamlines academic planning by:
- Parsing student degree requirements from DegreeWorks PDF exports
- Reading existing graduation study plans and 4-year schedules from Excel files
- Crawling the university course catalog to extract prerequisite information
- Generating optimal course plans that respect:
  - Prerequisite requirements
  - Course availability by semester
  - Maximum credit hour limits per semester
  - Student's completed courses
- Exporting the generated plan to Excel

## Features

- **Automated Scheduling** - Generates course plans without manual intervention
- **Prerequisite-Aware** - Ensures courses are scheduled after their prerequisites
- **Capacity Management** - Respects semester credit hour limits
- **Web Integration** - Automatically fetches course data from the university catalog
- **Flexible Input** - Accepts PDF degree sheets and Excel study plans
- **Excel Export** - Produces formatted Excel files with the recommended schedule
- **Configuration-Driven** - Easily adjust settings via `config.toml`
- **Text-based User Interface** - Easy operation

## Prerequisites

### System Requirements

- **Operating System**: Windows
- **Python**: Version 3.13 or higher - https://www.python.org/downloads/windows/
- **Git**: For cloning the repository (optional if downloading as ZIP) - https://git-scm.com/install/windows
- **Disk Space**: Minimal (~170MB including dependencies)

### Software Dependencies

Better Advise requires the following Python libraries (automatically installed via `pip install`):

**Core Libraries**:
- `beautifulsoup4==4.14.2` - HTML/XML parsing for web scraping
- `pandas==2.3.3` - Data manipulation and analysis
- `openpyxl==3.1.5` - Excel file reading and writing
- `pypdf==6.1.3` - PDF parsing for DegreeWorks extraction
- `requests==2.32.5` - HTTP requests for web crawler
- `tomli==2.3.0` - TOML configuration file parsing

**Build/Distribution**:
- `pyinstaller==6.16.0` - Creates standalone executable (optional)

See `requirements.txt` for the complete list of all dependencies including transitive dependencies.

## Download ##
Direct Download of standalone application.
https://github.com/the-red-crow/better-advise/releases 


## Setting up development environment in Windows for building
Install Python 3.13 or higher from the official website: https://www.python.org/downloads/windows/

- Ensure Python and pip are added to your system PATH during installation.

Install Git from: https://git-scm.com/download/win


### Clone the Repository using Git

In Command-line navigate to your desired directory and run:
```bash
git clone https://github.com/the-red-crow/better-advise.git
cd better-advise

```

## Build/Configuration/Installation/Deployment

### Installation Steps

After downloading the repository, follow these steps to set up Better Advise:

### 1. Create a Virtual Environment and activate (Optional but Recommended)

```bash
python -m venv venv
.\venv\Scripts\activate

```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt

```

This command installs all required Python packages listed in `requirements.txt`.

**Key Configuration Options**:
- `degree_pdf_path`: Path to your DegreeWorks PDF export
- `graduate_study_plan_path`: Path to your graduation study plan (Excel)
- `four_year_schedule_path`: Path to your 4-year course schedule (Excel)
- `max_semester_hours`: Maximum credit hours per semester
- `course_catalog_url`: University course catalog URL

#### 3. Prepare Input Files

Place the following files in your configured input directory:
- **DegreeWorks PDF**: Export your remaining degree requirements from DegreeWorks
- **Graduate Study Plan (Excel)**: Your institution's graduation study plan template
- **4-Year Schedule (Excel)**: Available course offerings by semester

#### 4. Build Standalone Executable

To create a standalone executable that runs without Python installed:

```bash
pyinstaller -F smart_advising_tool.py
```

The executable will be created in the `dist/` directory.

## Usage

### Running the Application

Double click `smart_advising_tool.exe` in the `dist/` folder 

Or run via command line:
```bash
python smart_advising_tool.py
```
Note: The program is not signed and may trigger security warnings.
For Windows 11: A blue box "Windows protected your PC" may appear. Click "More info" and then "Run anyway" to proceed.
and then the Run anyway button to execute the program.

**Expected Output**:
```
════════════════════════════════════════════════════
        BETTER ADVISE - Academic Planning Tool
════════════════════════════════════════════════════

Select an option:
1. Run
2. Config
3. Quit

Enter your choice:
```

### Menu Options

- **Run** - Execute the full advising workflow to generate your course plan
- **Config** - Modify configuration settings (file paths, semester hours limit, etc.)
- **Quit** - Exit the application

### Step-by-Step Workflow

#### Step 1: Prepare Your Input Files

Place these files in your configured input directory (default: `input/`):

1. **DegreeWorks PDF Export**
   - Log into your student portal
   - Go to DegreeWorks
   - Export your degree audit as a PDF
   - Save as specified in `config.toml` (e.g., `input/degreeworks.pdf`)

2. **Graduate Study Plan (Excel)**
   - Download from your institution (typically provided by your college)
   - Save as specified in `config.toml` (e.g., `input/graduate_study_plan.xlsx`)

3. **4-Year Schedule (Excel)**
   - Contains course offerings by semester
   - Save as specified in `config.toml` (e.g., `input/four_year_schedule.xlsx`)

#### Step 2: Run the Tool

Select option `1` (Run) from the menu.

#### Step 3: Monitor the Process

The tool will:
1. **Parse Input Files** - Extract degree requirements, study plan, and course schedule
2. **Fetch Course Data** - Scrape the university catalog for prerequisite information
3. **Analyze Dependencies** - Build a dependency graph of all courses
4. **Generate Plan** - Create an optimal course schedule respecting:
   - Prerequisites
   - Course availability by semester
   - Maximum credit hours per semester
5. **Export Results** - Save the recommended plan to Excel

**Expected Output Example**:
```
>> 1
[SmartAdvisingTool] Run started.
[SmartAdvisingTool] Initializing components...
Connecting to catalog...
Connecting to catalog...
[SmartAdvisingTool] Components initialized.
[SmartAdvisingTool] Processing inputs...
[SmartAdvisingTool] PDFParser found 8 remaining courses
[SmartAdvisingTool] Graduate Study Plan courses: 8
[SmartAdvisingTool] Four-Year Schedule terms: 94
[SmartAdvisingTool] Remaining: 8 | Completed: 0
[SmartAdvisingTool] Generating course plan...
Connecting to catalog...
Connecting to catalog...
Connecting to catalog...
Connecting to catalog...
[SmartAdvisingTool] Plan exported: outputs\recommended_class_plan.xlsx
[SmartAdvisingTool] Run finished successfully.
[SmartAdvisingTool] Cleaning up resources...
[SmartAdvisingTool] Cleanup complete.
```

#### Step 4: Review Your Generated Plan

Check the `outputs/` directory for your generated plan file (default: `recommended_class_plan.xlsx`). The Excel file contains:
- Summary page
- A page for each semester with scheduled courses


**Configuration Details**:
- `degree_pdf_path`: Path to your DegreeWorks PDF export
- `graduate_study_plan_path`: Path to your graduation study plan (Excel)
- `four_year_schedule_path`: Path to your 4-year course schedule (Excel)
- `output_excel_filename`: Name of the generated plan file
- `output_directory`: Where to save the generated plan
- `course_catalog_url`: University catalog URL for prerequisite scraping
- `max_semester_hours`: Maximum credit hours per semester (typically 15-18)

## Project Structure

```
better-advise/
├── smart_advising_tool.py      # Main entry point and CLI menu
├── config.toml                 # Configuration settings
├── config_manager.py           # Config file handling
│
├── Course Models
├── course.py                   # Course class definition
├── semester.py                 # Semester class definition
├── academic_plan.py            # Academic plan management
│
├── Input Processing
├── pdf_parser.py               # DegreeWorks PDF parser
├── excel_parser.py             # Excel file parser
├── web_crawler.py              # Course catalog web scraper
├── prerequisite_checker.py     # Prerequisite validation
│
├── Plan Generation
├── plan_generator.py           # Advanced plan generator
├── dag_generator.py            # Dependency graph builder
│
├── Input/Output Directories
├── input/                      # Input files (PDFs, Excel files)
├── outputs/                    # Generated course plans
└── docs/                       # Project documentation
```

## Technologies Used

- **PDF Processing**: pypdf
- **Excel Handling**: openpyxl, pandas
- **Web Scraping**: requests, beautifulsoup4
- **Configuration**: tomli
- **Build/Distribution**: pyinstaller

## Development

This project was developed as part of CPSC6177 (Software Design) at Columbus State University, demonstrating:
- Object-oriented design principles
- Modular architecture
- Data processing pipelines

## Documentation

For more details, see:
- `docs/project-specs.md` - Complete project specifications and requirements
- `docs/q and a about the project.md` - Frequently asked questions and clarifications

## Support

For issues or questions, please open an issue in the repository.
