from django.contrib import admin

from Dashboard.models import Student, University, Course, CourseRegistration, StudentDegree, TimePlanBooking, Degree, \
    ExamOutcome, Semester, CourseSemester

"""
In this file the different database models are activated for the admin panel.
This allows to editing the information.

Admin panel is accessible with url: http://localhost:8000/admin/

username: admin
password: Test12345-

a new user can be created with the following command:

python manage.py createsuperuser

"""


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ["name", "ects_goal"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "ects_points", "expected_hours", "degree", "university", "bg_color", "fg_color")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "university"]


@admin.register(StudentDegree)
class StudentDegreeAdmin(admin.ModelAdmin):
    list_display = ["student", "degree", "start_date", "end_date", "ects_collected"]


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "spent_hours", "completed"]


@admin.register(ExamOutcome)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ["course_registration", "grade"]


@admin.register(Semester)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ["name", "degree", "number"]


@admin.register(CourseSemester)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ["id", "semester", "course", "degree"]

    # this method is used to show the degree name in the list of the admin panel
    def degree(self, obj):
        if obj.semester:
            return obj.semester.degree.name
        else:
            return ""


@admin.register(TimePlanBooking)
class TimePlanBookingAdmin(admin.ModelAdmin):
    list_display = ["course_registration", "from_date", "from_time", "until_date", "until_time"]
