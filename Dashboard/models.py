from datetime import datetime

from django.db import models

"""
This file contains all database models
Properties encapsulate the information 
"""


class University(models.Model):
    """
    The university holds all models together here more simplified with the university name
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _name = models.CharField(db_column="name", max_length=100)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def __str__(self):
        return self._name


class Student(models.Model):
    """
    Students are assigned to an active university and registered by their name and a student id
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _first_name = models.CharField(db_column="first_name", max_length=100)
    _last_name = models.CharField(db_column="last_name", max_length=100)
    _university = models.ForeignKey(University, db_column="university", on_delete=models.CASCADE)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str):
        self._first_name = first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str):
        self._last_name = last_name

    @property
    def university(self) -> University:
        return self._university

    @university.setter
    def university(self, university: University):
        self._university = university

    def __str__(self):
        return self.name


class Degree(models.Model):
    """
    Degrees are assigned to an active university and require an ects goal to be reached
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _name = models.CharField(db_column="name", max_length=255)
    _ects_goal = models.IntegerField(db_column="ects_goal")
    _university = models.ForeignKey(University, db_column="university", on_delete=models.CASCADE)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def ects_goal(self) -> int:
        return self._ects_goal

    @ects_goal.setter
    def ects_goal(self, value: int):
        self._ects_goal = value

    @property
    def university(self) -> University:
        return self._university

    @university.setter
    def university(self, university: University):
        self._university = university

    def __str__(self):
        return self._name


class Course(models.Model):
    """
    Each university degree has a collection of course that need to be completed.
    Those grant predefined points of ects if the course is passed with a valid grade
    Also there is a suggested hours limit for each course defined

    For the calendar the display foreground and background colors are saved on the course
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _name = models.CharField(db_column="name", max_length=255)
    _ects_points = models.IntegerField(db_column="ects_points")
    _expected_hours = models.FloatField(db_column="expected_hours")
    _bg_color = models.CharField(db_column="bg_color", max_length=7, default="#000000")
    _fg_color = models.CharField(db_column="fg_color", max_length=7, default="#ffffff")
    _degree = models.ForeignKey(Degree, db_column="degree", on_delete=models.CASCADE)
    _university = models.ForeignKey(University, db_column="university", on_delete=models.CASCADE)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def ects_points(self) -> int:
        return self._ects_points

    @ects_points.setter
    def ects_points(self, ects_points: int):
        self._ects_points = ects_points

    @property
    def expected_hours(self) -> float:
        return self._expected_hours

    @expected_hours.setter
    def expected_hours(self, expected_hours: float):
        self._expected_hours = expected_hours

    @property
    def bg_color(self) -> str:
        return self._bg_color

    @bg_color.setter
    def bg_color(self, bg_color: str):
        self._bg_color = bg_color

    @property
    def fg_color(self) -> str:
        return self._fg_color

    @fg_color.setter
    def fg_color(self, fg_color: str):
        self._fg_color = fg_color

    @property
    def degree(self) -> Degree:
        return self._degree

    @degree.setter
    def degree(self, degree: Degree):
        self._degree = degree

    @property
    def university(self) -> University:
        return self._university

    @university.setter
    def university(self, university: University):
        self._university = university

    def __str__(self):
        return self.name


class Semester(models.Model):
    """
    Semesters allow to group the courses so that they can be searched and filtered later on
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _degree = models.ForeignKey(Degree, db_column="degree", on_delete=models.CASCADE)
    _name = models.CharField(db_column="name", max_length=255)
    _number = models.IntegerField(db_column="number")

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def degree(self) -> Degree:
        return self._degree

    @degree.setter
    def degree(self, degree: Degree):
        self._degree = degree

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, number: int):
        self._number = number

    def __str__(self):
        return self._name


class CourseSemester(models.Model):
    """
    Table to connect the courses with the semester entries
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _course = models.ForeignKey(Course, db_column="course", on_delete=models.CASCADE)
    _semester = models.ForeignKey(Semester, db_column="semester", on_delete=models.CASCADE)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def course(self) -> Course:
        return self._course

    @course.setter
    def course(self, course: Course):
        self._course = course

    @property
    def semester(self) -> Semester:
        return self._semester

    @semester.setter
    def semester(self, semester: Semester):
        self._semester = semester

    def __str__(self):
        """
            Format display name of entries to be displayed as course name - semester name
        """
        return f"{self.course.name} - {self.semester.name}"


class StudentDegree(models.Model):
    """
    Students register themself for degrees.
    This relation is captured within the StudentDegree model.
    A degree is started at a date and needs to be finished within a given time.
    Also the already collected ects are stored to check the progress of the degree
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _student = models.ForeignKey(Student, db_column="student", on_delete=models.CASCADE)
    _degree = models.ForeignKey(Degree, db_column="degree", on_delete=models.CASCADE)
    _start_date = models.DateField(db_column="start_date")
    _end_date = models.DateField(db_column="end_date")
    _ects_collected = models.IntegerField(db_column="ects_collected")

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def student(self) -> Student:
        return self._student

    @student.setter
    def student(self, student: Student):
        self._student = student

    @property
    def degree(self) -> Degree:
        return self._degree

    @degree.setter
    def degree(self, degree: Degree):
        self._degree = degree

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @start_date.setter
    def start_date(self, start_date: datetime):
        self._start_date = start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: datetime):
        self._end_date = end_date

    @property
    def ects_collected(self) -> int:
        return self._ects_collected

    @ects_collected.setter
    def ects_collected(self, ects_collected: int):
        self._ects_collected = ects_collected

    def __str__(self):
        """
            Format display name of entries to be displayed as student name - degree name
        """
        return f'{self._student.name} - {self._degree.name}'


class CourseRegistration(models.Model):
    """
    Students register for one or more courses that need to be completed for their degree.
    The relation between student and course is captured within the CourseRegistration model.
    Each registered course captures the spent hours and also the grade of the course to determine
    the status
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _student = models.ForeignKey(Student, db_column="student", on_delete=models.CASCADE)
    _course = models.ForeignKey(Course, db_column="course", on_delete=models.CASCADE)
    _spent_hours = models.FloatField(db_column="spent_hours", default=0)
    _completed = models.BooleanField(db_column="completed", default=False)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def student(self) -> Student:
        return self._student

    @student.setter
    def student(self, student: Student):
        self._student = student

    @property
    def course(self) -> Course:
        return self._course

    @course.setter
    def course(self, course: Course):
        self._course = course

    @property
    def spent_hours(self) -> float:
        return self._spent_hours

    @spent_hours.setter
    def spent_hours(self, spent_hours: float):
        self._spent_hours = spent_hours

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, completed: bool):
        self._completed = completed

    def __str__(self):
        """
        Format display name of entries to be displayed as student name - course name
        """
        return f'{self.student.name} - {self.course.name}'


class ExamOutcome(models.Model):
    """
    This table stores the exam results with the grades and is linked to a course registration
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _course_registration = models.ForeignKey(CourseRegistration, db_column="course_registration",
                                             on_delete=models.CASCADE)
    _grade = models.FloatField(db_column="grade")
    _passed = models.BooleanField(db_column="passed", default=False)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def course_registration(self) -> CourseRegistration:
        return self._course_registration

    @course_registration.setter
    def course_registration(self, course_registration: CourseRegistration):
        self._course_registration = course_registration

    @property
    def grade(self) -> float:
        return self._grade

    @grade.setter
    def grade(self, grade: float):
        self._grade = grade

    @property
    def passed(self) -> bool:
        return self._passed

    @passed.setter
    def passed(self, passed: bool):
        self._passed = passed

    def __str__(self):
        """
            Format display name of the entries to be displayed as student name - course name - grade
        """
        return f'{self._course_registration.student.name} - {self._course_registration.course.name} - {self._grade}'


class TimePlanBooking(models.Model):
    """
    Students have a time plan which covers the course registrations.
    Each time plan entry captures date and time for the learning sessions
    of the course.
    """
    _id = models.AutoField(db_column="id", primary_key=True)
    _course_registration = models.ForeignKey(CourseRegistration, db_column="course_registration",
                                             on_delete=models.CASCADE)
    _from_date = models.DateField(db_column="from_date")
    _from_time = models.TimeField(db_column="from_time")
    _until_date = models.DateField(db_column="until_date")
    _until_time = models.TimeField(db_column="until_time")

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def course_registration(self) -> CourseRegistration:
        return self._course_registration

    @course_registration.setter
    def course_registration(self, course_registration: CourseRegistration):
        self._course_registration = course_registration

    @property
    def from_date(self) -> datetime:
        return self._from_date

    @from_date.setter
    def from_date(self, from_date: datetime):
        self._from_date = from_date

    @property
    def from_time(self) -> datetime:
        return self._from_time

    @from_time.setter
    def from_time(self, from_time: datetime):
        self._from_time = from_time

    @property
    def until_date(self) -> datetime:
        return self._until_date

    @until_date.setter
    def until_date(self, until_date: datetime):
        self._until_date = until_date

    @property
    def until_time(self) -> datetime:
        return self._until_time

    @until_time.setter
    def until_time(self, until_time: datetime):
        self._until_time = until_time

    def __str__(self):
        """
        Format display name of the entries to be displayed as course name - student name - id
        """
        return f'{self._course_registration.course.name} - {self._course_registration.student.name} - {self.id}'
