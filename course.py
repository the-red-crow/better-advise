class Course():
    def __init__(self, code:str, name:str, desc:str, hours:float, courseTaken:bool, letterGrade:str, semestersoffered:list[str], **prereq):
            self.code = code 
            self.name = name
            self.desc = desc
            self.hours = hours
            self.courseTaken = courseTaken
            self.letterGrade = letterGrade
            self.semestersoffered = semestersoffered
            self.prereq = prereq

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
    def getGrade(self):
          return self.letterGrade
    def setGrade(self, grade:str):
          self.letterGrade = grade
    
