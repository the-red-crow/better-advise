from typing import List

class Course():
    def __init__(self, code:str, name:str, hours:float, course_taken:bool = False, prereq:List[str] = []):
            self.code = code 
            self.name = name
            self.hours = hours
            self.courseTaken = course_taken
            self.prerequisites = prereq

    def addPrereq(self, *args):
          for a in args:
                if a not in self.prerequisites:
                      self.prerequisites.append(a)
    def getPrereq(self):
          return self.prerequisites
    def getHours(self):
          return self.hours
    def isTaken(self):
          return self.courseTaken

