from django import forms
from django.core.exceptions import ValidationError

"""
This file contains all django forms for validations of input data
"""


class SwitchUniversityForm(forms.Form):
    """
    This form is used to switch between the universities
    """
    university_id = forms.CharField(required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        university_id = cleaned_data["university_id"]

        # verify that the university id is a numeric value
        if not university_id.isnumeric():
            raise ValidationError("invalid university id")

        # to prevent a recurrent import the module is only imported for single use here
        from Dashboard.services import UniversityService

        # ensure the provided university id exists in the database
        if not UniversityService().is_university_existing(university_id):
            raise ValidationError(f"university with id {university_id} was not found")

        return cleaned_data


class SwitchStudentForm(forms.Form):
    """
    This form is used to switch between students of a university
    """
    student_id = forms.CharField(required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        student_id = cleaned_data["student_id"]

        # verify that the student id is a numeric value
        if not student_id.isnumeric():
            raise ValidationError("invalid student id")

        # to prevent a recurrent import the module is only imported for single use here
        from Dashboard.services import StudentService

        # ensure the provided student id exists in the database
        if not StudentService().is_student_existing(student_id):
            raise ValidationError(f"student with id {student_id} was not found")

        return cleaned_data


class GradeManagementForm(forms.Form):
    """
    This form is used to update the grade of a course for the selected student
    """
    course_id = forms.CharField(required=True)
    grade = forms.FloatField(min_value=0, max_value=6, required=True)

    def clean(self):
        clean_data = self.cleaned_data
        course_id = clean_data["course_id"]
        grade = clean_data["grade"]

        # verify that the course id is a numeric value
        if not course_id.isnumeric():
            raise ValidationError(f'course id is not is invalid')

        # verify grade is within acceptable range, 0 means delete grade
        if grade > 0 and grade < 1:
            raise ValidationError(f'grade is not valid only 1-6 or 0 are allowed')

        # the import below is needed to prevent recurrent module imports
        from Dashboard.services import CourseService

        # ensure the provided course id exists in the database
        if not CourseService().is_course_existing(course_id):
            raise ValidationError(f'course with id {course_id} does not exist')

        return clean_data


class TimePlanManagementForm(forms.Form):
    """
    This form is used to create new time plan entries within the students calendar
    """
    course_id = forms.CharField(required=True)
    student_id = forms.CharField(required=True)
    from_date = forms.DateField(required=True)
    from_time = forms.TimeField(required=True)
    until_date = forms.DateField(required=True)
    until_time = forms.TimeField(required=True)

    def clean(self):
        clean_data = self.cleaned_data

        # extract the values from the cleaned form data
        student_id = clean_data["student_id"]
        course_id = clean_data["course_id"]
        from_date = clean_data["from_date"]
        to_date = clean_data["until_date"]
        from_time = clean_data["from_time"]
        until_time = clean_data["until_time"]

        # verify that the course id is a numeric value
        if not course_id.isnumeric():
            raise ValidationError(f'course id is not is invalid')

        # the import below is needed to prevent recurrent module imports
        from Dashboard.services import CourseService, CalendarService

        # verify the course with the provided id exists
        if not CourseService().is_course_existing(course_id):
            raise ValidationError(f'course with id {course_id} does not exist')

        # to reduce complexity only allow bookings on the same day
        if from_date != to_date:
            raise ValidationError(f'currently only bookings on the same day are allowed')

        # from_date must be smaller or equal until date
        if from_date > to_date:
            raise ValidationError(f'Fromdate {from_date} must be before Untildate {to_date}')

        # if from_date and to_date is on the same day, also check that the until time is bigger
        if from_date == to_date and from_time >= until_time:
            raise ValidationError(f'Fromtime {from_time} must be before Untiltime {until_time}')

        # check if there is already an entry within the given timespan
        if CalendarService().get_time_plan_booking_between(student_id, from_date, from_time, until_time).exists():
            raise ValidationError(f'Booking are conflicting, please choose another date or time')

        return clean_data
