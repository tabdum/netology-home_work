class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade] # dict[course] = dict[course] + [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n")

class Lector(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lector_grades = {}
    def average(self):
        b = list(self.lector_grades.values())
        c = []
        for i in b:
            for j in i:
                c.append(j)
        h = sum(c)/len(c)
        return h
    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.average()}\n")

    def __eq__(self, other):
        return self.average() == other.average()
    def __ne__(self, other):
        return self.average() != other.average()
    def __lt__(self, other):
        return self.average() < other.average()
    def __le__(self, other):
        return self.average() <= other.average()
    def __gt__(self, other):
        return self.average() > other.average()
    def __ge__(self, other):
        return self.average() >= other.average()

class Student(Lector):
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def average(self):
        b = list(self.grades.values())
        c = []
        for i in b:
            for j in i:
                c.append(j)
        h = sum(c)/len(c)
        return h

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.average()}\n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                f"Завершенные курсы: {', '.join(self.finished_courses)}\n\n")


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
best_student.courses_in_progress += ['Java']
best_student.courses_in_progress += ['C+']
best_student.finished_courses += ['Введение в програмирование']

second_student = Student('Nadya', 'Petrova', 'wooman')
second_student.courses_in_progress += ['Python']


cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']

reviewer = Reviewer("Ben", 'TEN')
reviewer.courses_attached += ['Python']
reviewer.rate_hw(best_student, 'Python', 9)
reviewer.rate_hw(best_student, 'Python', 5)
reviewer.rate_hw(best_student, 'Python', 10)
reviewer.rate_hw(second_student, 'Python', 2)
reviewer.rate_hw(second_student, 'Python', 2)
reviewer.rate_hw(second_student, 'Python', 4)

cool_lector = Lector("Петр", "Петрович")
cool_lector.courses_attached += ['Python']
best_student.rate_hw(cool_lector, 'Python', 10)
best_student.rate_hw(cool_lector, 'Python', 5)
best_student.rate_hw(cool_lector, 'Python', 6)

second_lector = Lector('Вася', 'Васькин')
second_lector.courses_attached += ['Python']
best_student.rate_hw(second_lector, 'Python', 7)
best_student.rate_hw(second_lector, 'Python', 3)
best_student.rate_hw(second_lector, 'Python', 4)




# print(cool_lector.lector_grades)
# print(best_student.grades)
print(reviewer)
print(cool_lector)
print(best_student)

print(cool_lector < second_lector)
print(cool_lector > second_lector)
print(cool_lector <= second_lector)
print(cool_lector >= second_lector)
print(cool_lector != second_lector)
print(cool_lector == second_lector)
print(best_student < second_student)
print(best_student > second_student)
print(best_student <= second_student)
print(best_student >= second_student)
print(best_student != second_student)
print(best_student == second_student)



