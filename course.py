class Course():
    def __init__(self, code:str, name:str, hours:float, course_taken:bool = False, **prereq):
            self.code = code 
            self.name = name
            self.hours = hours
            self.courseTaken = course_taken
            self.prereq = list(prereq)

    def addPrereq(self, *args):
          for a in args:
                if a not in self.prereq:
                      self.prereq.append(a)
    def getPrereq(self):
          return self.prereq
    def getHours(self):
          return self.hours
    def isTaken(self):
          return self.courseTaken

