# Q&A About The Project

### 1. How can I get input 1 (i.e., a list of courses a student still needs) to test my SW?

=> For input one, please use your own DegreeWorks PDF files to parse and test, as DegreeWorks changes its format every 1-2 years, and we cannot provide them due to privacy issues.

Thus, you can either implement a web crawling to grab your DegreeWorks PDF file if possible, or you can manually download it and then parse it to obtain a list of courses a student (here means you) still needs.

### 2. I am not familiar with "a directed acyclic graph (DAG) - prerequisite graph of all required classes from the students' track" on the CSU website, could you provide me with URL or navigation of the webpage where I can find a DAG on CSU website?

=> Please Google it, there are many existing DAG implementations in Python. Because of the nature of this class, you have to learn how to solve a problem.

### 3. Also please confirm the rules and regulations that pertain to enrollment such as with:

* **prerequisite courses** - which need to be completed before a student enrolls in a core course

=> A prerequisite course is a course that must be successfully completed before a student can enroll in a more advanced course. For example, if Course B is listed as a prerequisite for Course C, it means that students must complete Course B before they are allowed to register for Course C.

* **core courses** - which are mandatory for every student enrolled in a given major

=> Yes, in this project, you only need to deal with core courses. You do not need to deal with electives.

* **dependent courses** - which need to be completed before the student plans to enroll in another course in the next semester, etc.

=> You can consider these as prerequisites.

### 4. In terms of getting the pre-req courses and class schedule in CSU website through web crawler, I would like to confirm whether I am browsing the appropriate CSU site for the info and please provide guidance if there is another place/page to obtain the info. I think I can scrape for pre-req courses but unsure about the class schedules

* For example, for Applied Computer Science (MS) pre-req courses, I can crawl in the Major Requirements under "program of study" section. Each course number is clickable and contains pre-req info in the pop-up box.

### 5. Just to confirm on the software type, are we implementing a Windows desktop GUI application using python?

=> There is no requirement for a GUI, you can implement yours with a command-based interface. However, you are welcome to implement one.

### 6. We have already processed the data in the CSU website as well as DAG graphs, but for some political, mathematical, chemistry, physics and language courses we don't have schedule information in the CSU website and also in DAG graph. so, for these kinds of courses can we ignore?

=> Yes, you can ignore these kinds of courses.