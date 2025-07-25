from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from Dashboard.forms import GradeManagementForm, TimePlanManagementForm, SwitchStudentForm, SwitchUniversityForm
from Dashboard.services import CourseService, CalendarService, StudentService, UniversityService

"""
This file contains all views to render html
The rendering itself happens int template/dashboard/dashboard.html
"""


class DashboardView(TemplateView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create instances for the needed services
        self.__university_service = UniversityService()
        self.__student_service = StudentService()
        self.__course_service = CourseService()
        self.__calendar_service = CalendarService()

        # define the values for the forms to handle
        self.__grade_form = "gradeManagement"
        self.__time_plan_form = "timePlanManagement"
        self.__student_form = "studentSelection"
        self.__university_form = "universitySelection"

    def get(self, request, *args, **kwargs):
        """
        This method is called it a GET request is sent
        """
        return self.prepare_template_response(request, {})

    def post(self, request, *args, **kwargs):
        """
        This method is called if a POST request is sent with form data
        """
        form_errors = {}
        student_id = self.__get_student_id_from_session(request)

        # is the grade form submitted
        if request.POST.get("formType") == self.__grade_form:
            # parse the form data and check validity
            form = GradeManagementForm(request.POST)
            if form.is_valid():
                self.__course_service.save_grade_for_course(student_id, form)
            else:
                form_errors = form.errors["__all__"]

        # is the time plan form submitted
        elif request.POST.get("formType") == self.__time_plan_form:
            # the student_id is copied from the session and added to the form
            form = request.POST.copy()
            form["student_id"] = student_id

            # parse the form data and check validity
            time_plan_form = TimePlanManagementForm(form)
            if time_plan_form.is_valid():
                self.__calendar_service.save_time_plan_booking(
                    self.__student_service.get_student_for_id(student_id),
                    time_plan_form)
            else:
                form_errors = time_plan_form.errors["__all__"]


        # is the switch student form submitted
        elif request.POST.get("formType") == self.__student_form:
            # parse the form data and check validity
            form = SwitchStudentForm(request.POST)
            if form.is_valid():
                self.__set_student_id_from_session(request, form.cleaned_data['student_id'])

        # is the switch university form submitted
        elif request.POST.get("formType") == self.__university_form:
            form = SwitchUniversityForm(request.POST)
            if form.is_valid():
                self.__set_university_id_from_session(request, form.cleaned_data['university_id'])

        return self.prepare_template_response(request, form_errors)

    def prepare_template_response(self, request, form_errors):
        """
        This helper method is used to reduce code duplication for get and post
        it prepares the template context to render the view
        """
        # prepare the university session attribute
        if not self.__get_university_id_from_session(request):
            self.__set_university_id_from_session(request, 1)

        # prepare the student session attribute
        if not self.__get_student_id_from_session(request):
            self.__set_student_id_from_session(request, self.__student_service.get_students_for_university(
                self.__get_university_id_from_session(request)).first().id)

        # capture GET parameters to filter and sort the search and calendar
        week_offset = int(request.GET.get("offset")) if request.GET.get("offset") is not None else 0
        course_sort_field = request.GET.get("sort") if request.GET.get("sort") is not None else ''
        course_sort_direction = request.GET.get("direction") if request.GET.get("direction") is not None else ''

        # fetch needed session attributes
        student_id = self.__get_student_id_from_session(request)
        university_id = self.__get_university_id_from_session(request)

        # prepare rendering context and fill in data objects
        return TemplateResponse(request, "Dashboard/dashboard.html", {
            "universities": self.__university_service.get_university_list(),
            "students": self.__student_service.get_student_list(university_id),
            "studentDetail": self.__student_service.get_student_detail(student_id),
            "courses": self.__course_service.get_course_list(student_id, course_sort_field, course_sort_direction),
            "calendarWeek": self.__calendar_service.generate_calendar_week(student_id, week_offset),
            "formErrors": form_errors,
        })

    # helper method to access university id from session
    def __get_university_id_from_session(self, request) -> int | None:
        return request.session.get('university_id')

    # helper method to set university id to session
    def __set_university_id_from_session(self, request, value):
        request.session['university_id'] = value
        if self.__get_student_id_from_session(request):
            del request.session['student_id']

    # helper method to access student id from session
    def __get_student_id_from_session(self, request) -> int | None:
        return request.session.get('student_id')

    # helper method to set student id to session
    def __set_student_id_from_session(self, request, value):
        request.session['student_id'] = value
