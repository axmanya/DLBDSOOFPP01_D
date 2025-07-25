from datetime import datetime, time, date

"""
This file contains all data transfer objects (DTO)
"""


class UniversityDto:
    """
    This DTO stores base details of the university
    """
    _university_id: str
    _university_name: str

    @property
    def university_id(self):
        return self._university_id

    @university_id.setter
    def university_id(self, value):
        self._university_id = value

    @property
    def university_name(self):
        return self._university_name

    @university_name.setter
    def university_name(self, value):
        self._university_name = value

    def __init__(self, university_id, university_name):
        self._university_id = university_id
        self._university_name = university_name


class StudentDto:
    """
    This DTO stores base details of the student
    """
    _student_id: str
    _student_name: str

    @property
    def student_id(self):
        return self._student_id

    @student_id.setter
    def student_id(self, value):
        self._student_id = value

    @property
    def student_name(self):
        return self._student_name

    @student_name.setter
    def student_name(self, value):
        self._student_name = value

    def __init__(self, student_id, student_name):
        self._student_id = student_id
        self._student_name = student_name


class StudentDetailsDto:
    """
    This DTO stores degree details of the student that are shown on the dashboard
    """
    _student_name: str
    _university_name: str
    _degree_name: str
    _ects_collected: float
    _ects_goal: float

    @property
    def student_name(self) -> str:
        return self._student_name

    @student_name.setter
    def student_name(self, student_name: str):
        self._student_name = student_name

    @property
    def university_name(self) -> str:
        return self._university_name

    @university_name.setter
    def university_name(self, university_name: str):
        self._university_name = university_name

    @property
    def degree_name(self) -> str:
        return self._degree_name

    @degree_name.setter
    def degree_name(self, degree_name: str):
        self._degree_name = degree_name

    @property
    def ects_collected(self) -> float:
        return self._ects_collected

    @ects_collected.setter
    def ects_collected(self, ects_collected: float):
        self._ects_collected = ects_collected

    @property
    def ects_goal(self) -> float:
        return self._ects_goal

    @ects_goal.setter
    def ects_goal(self, ects_goal: float):
        self._ects_goal = ects_goal

    def __init__(self, student_name, university_name, degree_name, ects_collected, ects_goal):
        self._student_name = student_name
        self._university_name = university_name
        self._degree_name = degree_name
        self._ects_collected = ects_collected
        self._ects_goal = ects_goal


class CourseDto:
    """
    This DTO stores base details of the courses to be displayed
    """
    _course_id: str
    _name: str
    _progress: float
    _formatted_progress: str
    _expected_hours: float
    _spent_hours: float
    _grade: float

    @property
    def course_id(self) -> str:
        return self._course_id

    @course_id.setter
    def course_id(self, course_id: str):
        self._course_id = course_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def progress(self) -> float:
        return self._progress

    @progress.setter
    def progress(self, progress: float):
        self._progress = progress

    @property
    def formatted_progress(self) -> str:
        return self._formatted_progress

    @formatted_progress.setter
    def formatted_progress(self, formatted_progress: str):
        self._formatted_progress = formatted_progress

    @property
    def expected_hours(self) -> float:
        return self._expected_hours

    @expected_hours.setter
    def expected_hours(self, expected_hours: float):
        self._expected_hours = expected_hours

    @property
    def spent_hours(self) -> float:
        return self._spent_hours

    @spent_hours.setter
    def spent_hours(self, spent_hours: float):
        self._spent_hours = spent_hours

    @property
    def grade(self) -> float:
        return self._grade

    @grade.setter
    def grade(self, grade: float):
        self._grade = grade

    def __init__(self, course_id: int, name: str, progress=0, formatted_progress="", expected_hours=0, spent_hours=0,
                 grade=0):
        self._course_id = course_id
        self._name = name
        self._progress = progress
        self._formatted_progress = formatted_progress
        self._expected_hours = expected_hours
        self._spent_hours = spent_hours
        self._grade = grade


class TimeSlotDto:
    """
    This DTO stores the content of the time slot and also the time blocks
    """
    _slot_time: time
    _entry_name: str
    _bg_color: str
    _fg_color: str
    _booked: bool

    @property
    def slot_time(self) -> time:
        return self._slot_time

    @slot_time.setter
    def slot_time(self, slot_time: time):
        self._slot_time = slot_time

    @property
    def entry_name(self) -> str:
        return self._entry_name

    @entry_name.setter
    def entry_name(self, entry_name: str):
        self._entry_name = entry_name

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
    def booked(self) -> bool:
        return self._booked

    @booked.setter
    def booked(self, booked: bool):
        self._booked = booked

    def __init__(self, slot_time: time, entry_name: str = "", bg_color: str = "", fg_color: str = ""):
        self._slot_time = slot_time
        self._entry_name = entry_name
        self._bg_color = bg_color
        self._fg_color = fg_color
        if self._entry_name:
            self._booked = True


class WeekDayDto:
    """
    This DTO stores the time bookings of the weekdays
    """
    _day: int
    _date: date
    _time_slots = list[tuple()]

    @property
    def day(self) -> int:
        return self._day

    @day.setter
    def day(self, day: int):
        self._day = day

    @property
    def date(self) -> date:
        return self._date

    @date.setter
    def date(self, date: date):
        self._date = date

    @property
    def time_slots(self) -> list[tuple]:
        return self._time_slots

    @time_slots.setter
    def time_slots(self, time_slots: list[tuple]):
        self._time_slots = time_slots

    def __init__(self, day: int, week_date: datetime.date):
        self._day = day
        self._date = week_date
        self.time_slots = []


class WeekDto:
    """
    This DTO stores a week with multiple week days
    """
    _week_number: int
    _week_days: list[WeekDayDto]

    @property
    def week_number(self) -> int:
        return self._week_number

    @week_number.setter
    def week_number(self, week_number: int):
        self._week_number = week_number

    @property
    def week_days(self) -> list[WeekDayDto]:
        return self._week_days

    @week_days.setter
    def week_days(self, week_days: list[WeekDayDto]):
        self._week_days = week_days

    def __init__(self, week_number: int):
        self._week_number = week_number
        self.week_days = []
