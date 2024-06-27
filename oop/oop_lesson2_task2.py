class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lector(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lector_grades = {}

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade] # dict[course] = dict[course] + [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_hw(self, lector, course, grade):
        if isinstance(lector, Lector) and course in lector.courses_attached and course in self.courses_in_progress:
            if course in lector.lector_grades:
                lector.lector_grades[course] += [grade]
            else:
                lector.lector_grades[course] = [grade]
        else:
            return "Ошибка"

best_student = Student('Ruoy', 'Eman', 'man')
best_student.courses_in_progress += ['Python']

cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']

reviewer = Reviewer("Ben", 'TEN')
reviewer.courses_attached += ['Python']
reviewer.rate_hw(best_student, 'Python', 10)
reviewer.rate_hw(best_student, 'Python', 10)
reviewer.rate_hw(best_student, 'Python', 10)

cool_lector = Lector("Петр", "Петрович")
cool_lector.courses_attached += ['Python']
best_student.rate_hw(cool_lector, 'Python', 10 )
best_student.rate_hw(cool_lector, 'Python', 10 )
best_student.rate_hw(cool_lector, 'Python', 10 )

print(cool_lector.lector_grades)

print(best_student.grades)