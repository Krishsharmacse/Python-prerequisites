class student:
    name=""
    rollno=2
    id=""
    def __init__(self, name, rollno, id):
        self.name = name
        self.rollno = rollno
        self.id = id

class person(student):
    marks=75
    def __init__(self,name,rollno,id,n,marks):
        
        self.marks=marks
kisu=person("misu",18,1234,1800)
print(kisu.marks)
    