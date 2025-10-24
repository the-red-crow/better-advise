# Smart Class Planning Tool for Academic Advising

## Background

Academic advising, especially properly planning courses across semesters to ensure students graduate on time, requires significant time and effort from both students and faculty. We are planning to build a Python-based smart class planning tool, which can be executed on any platform such as Windows, Linux, etc.

It is important for students to enroll in the proper courses designed to meet the degree requirements. Many students mistakenly enroll in classes simply because the classes fit their schedule without considering factors such as prerequisite requirements and different course offering times over the academic year semesters.

## Project Overview

This smart advising tool can output a recommended class plan for a student to follow until the student's graduation. This software requires three inputs to generate an output excel form where recommended classes for different semesters are listed.

### Required Inputs

1. **Course Requirements List** - A list of courses a student still needs until the student's graduation, which will be obtained from Degreeworks as a PDF document.

2. **Graduate Study Plans (Revised)** - Shows the appropriate course plan for a student to take from his/her first semester till his/her graduation.

3. **4-Year Schedule** - Shows when the student's required courses will be offered.

## Requirements

Academic advising takes a long time for both students and faculty, especially when checking prerequisite issues. To facilitate class planning, we are to build a Python-based standalone application, which can be executed on the Windows platform.

### Functional Requirements

#### 1. Course Planning
The first goal of the software is to plan out classes among different semesters for a student until his/her graduation. The software takes three inputs and outputs an excel sheet where recommended classes are listed. The recommended plan should be outputted by the software in the form of an Excel document.

#### 2. Prerequisite Checking
Another function of the software is to detect if a student's plan has prerequisite issues. To do this, you need to construct a web crawler component within your software to grab the prerequisite information from CPSC Course Descriptions because the descriptions include prerequisite information which is sometimes missing in DegreeWorks.

### Non-Functional Requirements (Constraints)

1. **Configurability** - The software should be configurable. Specifically, the inputs must be separated from the software and be parsed by the software.

2. **Platform Compatibility** - The software should be implemented in Python and can be executed on Windows.