from datetime import datetime, timedelta, time, date
from operator import attrgetter

from django.db.models import Sum, Avg, Q

from Dashboard.dto import WeekDto, WeekDayDto, TimeSlotDto, CourseDto, StudentDto, StudentDetailsDto, UniversityDto
from Dashboard.forms import TimePlanManagementForm, GradeManagementForm
from Dashboard.models import Course, CourseRegistration, Student, StudentDegree, TimePlanBooking, CourseSemester, \
    ExamOutcome, University

"""
This file contains all services that interact with the database models
"""


class UniversityService:
    """
    This service handled operations on the university database model.
    """

    def is_university_existing(self, university_id: int) -> bool:
        return University.objects.filter(_id=university_id).exists()

    def get_university_for_id(self, university_id: int) -> University:
        return University.objects.get(_id=university_id)

    def get_universities(self) -> list[University]:
        return University.objects.all()

    def get_university_list(self) -> list[UniversityDto]:
        # get a list of all universities and create dto objects
        universities = self.get_universities()
        return [UniversityDto(x.id, x.name) for x in universities]


class StudentService:
    """
    This service handles the base operations on the Student database model
    """

    def is_student_existing(self, student_id: int) -> bool:
        return Student.objects.filter(_id=student_id).exists()

    def get_student_for_id(self, student_id: int) -> Student:
        return Student.objects.filter(_id=student_id).first()

    def get_student_detail(self, student_id: int)-> StudentDetailsDto:
        """
        This function prefills the student details for the frontend display
        """
        # fetch degree and ensure only needed fields are given to frontend
        student_degree = self.get_student_degree_for_student(student_id)
        return StudentDetailsDto(student_degree.student.name,
                                               student_degree.student.university.name,
                                               student_degree.degree.name,
                                               student_degree.ects_collected,
                                               student_degree.degree.ects_goal)


    def get_students_for_university(self, university_id: int) -> list[Student]:
        return Student.objects.filter(_university___id=university_id)

    def get_student_list(self, university_id: int)-> list[StudentDto]:
        """
        This function prefills a list with student dto objects for the frontend display
        """
        # fetch all students of university and ensure only needed field are given to frontend
        students = self.get_students_for_university(university_id)
        return [StudentDto(x.id, x.name) for x in students]


    def get_student_grade_average(self, student_id: int) -> float:
        # fetch all exams that are passed
        exam_outcomes = ExamService().get_all_exam_outcomes_for_student(student_id).filter(_passed=True)

        # calculate the average of the grades
        average = exam_outcomes.aggregate(Avg('_grade'))['_grade__avg'] if exam_outcomes else 0
        return round(average, 2)

    def get_student_degree_for_student(self, student_id: int) -> StudentDegree:
        """
        A student can have multiple degrees but the one that has not ended will be fetched
        """
        return StudentDegree.objects.filter(_student___id=student_id, _end_date__gte=datetime.today()).first()


class CourseService:
    """
    This service handles the base operations on the Course database model
    """

    def is_course_existing(self, course_id: int) -> bool:
        return Course.objects.filter(_id=course_id).exists()

    def is_course_registered_for_student(self, student_id: int, course_id: int) -> bool:
        return CourseRegistration.objects.filter(_student___id=student_id, _course___id=course_id).exists()

    def get_course_for_id(self, course_id: int) -> Course:
        return Course.objects.filter(_id=course_id).first()

    def get_course_registration_for_student(self, student_id: int, course_id: int) -> CourseRegistration:
        return CourseRegistration.objects.filter(_student___id=student_id, _course___id=course_id).first()

    def get_courses_for_student(self, student_id: int) -> list[CourseRegistration]:
        student_degree = StudentService().get_student_degree_for_student(student_id)
        return CourseRegistration.objects.filter(_student___id=student_id, _course___degree=student_degree.degree).all()

    def get_course_semester(self, course_id: int) -> CourseSemester:
        return CourseSemester.objects.filter(_course___id=course_id).first()

    def save_grade_for_course(self, student_id: int, grade_form: GradeManagementForm):
        course_id = grade_form.cleaned_data["course_id"]
        grade = grade_form.cleaned_data["grade"]

        # verify that the registration exists, if not create a new one
        if not self.is_course_registered_for_student(student_id, course_id):
            self.save_new_course_registration(student_id, course_id)

        course_registration = self.get_course_registration_for_student(student_id, course_id)

        # save the exam using the exam service
        exam_service = ExamService()
        exam_service.save_exam_outcome_for_registration(course_registration.id, grade)

        # if exam is passed then mark course as complete
        course_registration.completed = grade <= 4 and grade >= 1
        course_registration.save()

        # fetch all completed course registrations for active degree and student that are completed
        degree = StudentService().get_student_degree_for_student(student_id)
        registrations = CourseRegistration.objects.filter(_student___id=student_id, _course___degree=degree.degree,
                                                          _completed=True)

        # sum up course total ects points
        if registrations:
            total_ects = registrations.aggregate(Sum("_course___ects_points"))["_course___ects_points__sum"]
        else:
            total_ects = 0

        # update totals on degree status
        degree.ects_collected = total_ects
        degree.save()

    def save_new_course_registration(self, student_id: int, course_id: int):
        CourseRegistration.objects.create(
            _course=Course.objects.filter(_id=course_id).first(),
            _student=StudentService().get_student_for_id(student_id))

    def get_course_list(self, student_id: int, sort_field='', sort_direction='') -> list[CourseDto]:
        """
        This helper method is used to create a list of course dto object for display and
        allows also to hand in sorting options for the display
        """
        course_list = []
        degree = StudentService().get_student_degree_for_student(student_id)
        courses = Course.objects.filter(_degree=degree.degree)
        exam_service = ExamService()

        # loop all courses
        for course in courses:
            # fetch the course registration if it exists
            registration = self.get_course_registration_for_student(student_id, course.id)

            grade = 0
            progress = 0
            hours_spent = 0
            if registration:
                # fetch grade information
                exam_outcome = exam_service.get_last_exam_outcome_for_registration(registration.id)
                if exam_outcome:
                    grade = exam_outcome.grade

                # fetch progress information
                hours_spent = registration.spent_hours
                progress = registration.spent_hours / course.expected_hours if registration is not None else 0
                progress = round(progress, 2)
                if grade > 0:
                    progress = 1

            # format the progress as nice decimal 0.00%
            display_progress = f"{progress:.2%}"
            if progress > 1:
                display_progress = f"-{(progress - 1):.2%}"

            # build the dto list
            course_list.append(
                CourseDto(
                    course_id=course.id,
                    name=course.name,
                    progress=progress if grade == 0 else 1,
                    formatted_progress=display_progress,
                    expected_hours=course.expected_hours,
                    spent_hours=hours_spent,
                    grade=grade
                )
            )

        # ensure that the correct sort field name is given otherwise remove sort
        if sort_field in ['name', 'progress', 'grade']:
            if sort_direction == 'asc' or sort_direction == '':
                return sorted(course_list, key=attrgetter(sort_field), reverse=True)
            elif sort_direction == 'desc':
                return sorted(course_list, key=attrgetter(sort_field), reverse=False)
        return course_list


class CalendarService:
    """
    This service handles the base operations on the TimePlanBooking database model.
    It also provides functionality to render the student calendar
    """

    def get_time_plan_bookings_for_student(self, student_id: int) -> list[TimePlanBooking]:
        return TimePlanBooking.objects.filter(_course_registration___student__id=student_id).all()

    def get_time_plan_bookings_form_date(self, student_id: str, from_date: date) -> list[TimePlanBooking]:
        return TimePlanBooking.objects.filter(_course_registration___student___id=student_id,
                                              _from_date=from_date).all()

    def get_time_plan_booking_between(self, student_id: str, from_date: date, from_time: time, until_time: time) -> \
            list[TimePlanBooking]:
        # this model filter uses the Q object to build a more complex query
        # this allows the use of logic operations like AND , OR
        return TimePlanBooking.objects.filter(
            Q(_course_registration___student___id=student_id) &
            Q(_from_date=from_date) &
            Q(_from_time__lt=until_time) &
            Q(_until_time__gt=from_time)
        ).all()

    def save_time_plan_booking(self, student: Student, time_plan_form: TimePlanManagementForm):
        """
        This method is a helper to properly update the exam results and also
        update the status of the courses and registrations
        """
        course_registration = CourseRegistration.objects.filter(_student=student,
                                                                _course___id=time_plan_form.cleaned_data[
                                                                    "course_id"]).first()
        # verify that the course registration exists, otherwise create new one
        if not course_registration:
            CourseService().save_new_course_registration(student.id, time_plan_form.cleaned_data["course_id"])
            course_registration = CourseRegistration.objects.filter(_student=student,
                                                                    _course___id=time_plan_form.cleaned_data[
                                                                        "course_id"]).first()

        # verify that the from time is in 15 min steps
        from_time = time_plan_form.cleaned_data["from_time"]
        if from_time.minute % 15 > 0:
            from_time = time(from_time.hour, from_time.minute - from_time.minute % 15)

        # verify that the until time is in 15 min steps
        until_time = time_plan_form.cleaned_data["until_time"]
        if until_time.minute % 15 > 0:
            until_time = time(until_time.hour, until_time.minute - until_time.minute % 15)

        # create and save the new time booking
        TimePlanBooking.objects.create(
            _course_registration=course_registration,
            _from_date=time_plan_form.cleaned_data["from_date"],
            _from_time=from_time,
            _until_date=time_plan_form.cleaned_data["until_date"],
            _until_time=until_time
        )

        # recalculate the spent time with timedelta to seconds
        time_in_seconds = 0
        result = TimePlanBooking.objects.filter(_course_registration=course_registration).all()
        for entry in result:
            time_in_seconds += (datetime.combine(entry.until_date, entry.until_time) -
                                datetime.combine(entry.from_date, entry.from_time)).total_seconds()

        # convert seconds to hours
        spent_hours = 0
        if time_in_seconds > 0:
            spent_hours = time_in_seconds / 60 / 60

        # assign the spent hours back to the registration
        course_registration.spent_hours = spent_hours
        course_registration.save()

    def generate_calendar_week(self, student_id: int, week_offset=0) -> WeekDto:
        """
            This method generated a data matrix for the display of the calendar
            The data matrix contains 1 Week = 7 Weekdays , each day has 24h and one hour is
            splitted into 4 - 15min blocks.
        """

        current_date = datetime.today()
        if week_offset != 0:
            # add number offset from calendar wek back and next to the current week
            current_date += timedelta(weeks=week_offset)

        week_number = current_date.isocalendar()[1]
        week = WeekDto(week_number=week_number)

        # the weekday 0 is always monday, so if the current weekday is subtracted from
        # the current date this results in the monday of that week
        first_day_of_week = current_date - timedelta(days=current_date.weekday())

        # loop the weekdays for the current week from monday
        for day in range(0, 7):
            current_week_day = first_day_of_week + timedelta(days=day)
            week_day = WeekDayDto(day, current_week_day)

            # each day has 24h hours
            for hour in range(0, 24):
                time_blocks = []

                # calendar hour is splitted into 15 minute blocks and has max 60 min
                for minute in range(0, 60, 15):
                    from_time = time(hour, minute)

                    # verify that there is no error if 60 is given
                    buffer = minute + 15 if minute + 15 < 60 else 59
                    until_time = time(hour, buffer)

                    # fetch the time plan bookings for the current student, degree und in the time range
                    booking = TimePlanBooking.objects.filter(_course_registration___student___id=student_id,
                                                             _from_date=current_week_day,
                                                             _from_time__lte=from_time,
                                                             _until_time__gte=until_time).first()

                    # create dto object for the timeslot
                    time_slot = TimeSlotDto(from_time,
                                            booking.course_registration.course.name if booking else "",
                                            booking.course_registration.course.bg_color if booking else "",
                                            booking.course_registration.course.fg_color if booking else "")
                    time_blocks.append(time_slot)

                # here we have a tuple list with 4 items per hour that is added
                week_day.time_slots.append((hour, time_blocks))

            # here we add the complete day with 24 entries
            week.week_days.append(week_day)

        return week


class ExamService:
    def is_exam_outcome_existing(self, course_registration: int) -> bool:
        return ExamOutcome.objects.filter(_course_registration___id=course_registration).exists()

    def get_last_exam_outcome_for_registration(self, course_registration: int) -> ExamOutcome:
        return ExamOutcome.objects.filter(_course_registration___id=course_registration).last()

    def get_all_exam_outcomes_for_registration(self, course_registration: int) -> list[ExamOutcome]:
        return ExamOutcome.objects.filter(_course_registration___id=course_registration).all()

    def get_all_exam_outcomes_for_student(self, student_id: int) -> list[ExamOutcome]:
        return ExamOutcome.objects.filter(_course_registration___student___id=student_id).all()

    def save_exam_outcome_for_registration(self, course_registration: int, grade: float):
        """
        This method saves the exam result, currently there will be only one
        entry that is overridden with the corrected grade, if none exists a new one is created
        """
        if not self.is_exam_outcome_existing(course_registration):
            ExamOutcome.objects.create(_course_registration_id=course_registration, _grade=grade)
        else:
            outcome = self.get_last_exam_outcome_for_registration(course_registration)
            outcome.grade = grade
            outcome._passed = grade <= 4 and grade >= 1
            outcome.save()
