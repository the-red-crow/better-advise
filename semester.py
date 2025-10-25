from course import Course
from typing import List
class Semester():
      def __init__(self,name:str,year:int, maxHours:int, courses:List[Course]):
            self.name = name
            self.year = year
            self.maxHours = maxHours
            self.courses = list(courses)

      def getTotalCredits(self):
            hours = 0
            for course in self.courses:
                  hours += course.getHours()
            return hours
      
      def addCourse(self, course: Course):
            if self.getTotalCredits() + course.getHours() <= self.maxHours:
                  self.courses.append(course)
                  return True
            return False

      def removeCourse(self, course: Course):
            if course in self.courses:
                  self.courses.remove(course)
                  return True
            return False

