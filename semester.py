from course import Course
class Semester():
      def __init__(self,name:str,year:int, maxHours:int, *courses:Course):
            self.name = name
            self.year = year
            self.maxHours = maxHours
            self.courses = courses

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

# rcourse1 = Course("Test 1", "A test course", 3)
# rcourse2 = Course("Test 2", "A test course", 1)
# rcourse3 = Course("Test 3", "A test course", 4)
# rSem1 = Semester(15,rcourse1,rcourse2)
# print(rSem1.getHours())