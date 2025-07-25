from datetime import datetime, time, timedelta

from django import template
from django.utils.safestring import mark_safe

"""
This file contains all custom template tags used for rendering
"""

# init the django template library
register = template.Library()


@register.simple_tag
def get_grade_avg(request):
    """
    fetches the grade average from the service class and returns it to the frontend
    """
    from Dashboard.services import StudentService
    return StudentService().get_student_grade_average(request.session["student_id"])


@register.simple_tag
def get_formatted_date(date):
    """
    Formats a given date in european date format
    """
    return date.strftime("%d.%m.%Y")


@register.simple_tag
def get_formatted_time(hour, minute):
    """
    Formats a given hour and minute as time format
    """
    return time(hour, minute).strftime("%H:%M")


@register.simple_tag
def get_array_index_value(array, index):
    """
    Fetch an array index value
    """
    return array[index]


@register.simple_tag
def get_calendar_week(request):
    """
    Render the current calendar week
    """
    current_date = datetime.now()
    current_date += timedelta(weeks=int(request.GET.get("offset")) if request.GET.get("offset") is not None else 0)
    return f'KW{current_date.isocalendar()[1]}'


@register.simple_tag
def get_offset(request, factor):
    """
    Calculate and return the next offset
    """
    return (int(request.GET.get("offset")) if request.GET.get("offset") is not None else 0) + factor


@register.simple_tag
def get_today_as_us_format():
    """
    Returns the current date and time in us format for the html to prefill the date fields
    """
    return datetime.now().strftime("%Y-%m-%d")


@register.simple_tag
def get_current_hour_with_offset(offset):
    """
    Returns the current minute as %15 in time format for the html to prefill the time fields
    """
    current_date = datetime.now() + timedelta(hours=offset)
    minutes = current_date.minute - current_date.minute % 15
    return time(current_date.hour, minutes).strftime("%H:%M")


@register.simple_tag
def get_conic_gradient_degrees(total_ects, collected_ects):
    """
    Calculates the progress for the cake diagram as degree
    """
    return (360 / total_ects) * collected_ects


@register.simple_tag
def get_course_sort_link(request, field):
    """
    Generate the sorting link needed to sort the course list
    """
    course_sort_field = request.GET.get("sort")
    course_sort_direction = request.GET.get("direction")
    sort_direction = ''
    if field == course_sort_field:
        if course_sort_direction in ('asc', ''):
            sort_direction = 'desc'
        else:
            sort_direction = 'asc'

    sort_icon = '&#8597;'
    if sort_direction == 'asc':
        sort_icon = '&#8595;'
    elif sort_direction == 'desc':
        sort_icon = '&#8593;'

    # mark the text html as save otherwise it is not rendered as html
    return mark_safe(
        f'<a href="?sort={field}&direction={sort_direction}" class="courseHeadSorter">{field.title()} {sort_icon}</a>')

@register.filter
def compare_ids(id1, id2):
    """
    This filter is needed to compare the dropdown ids which may not have the same datatype
    so this function ensures both are string that can be compared
    """
    return str(id1) == str(id2)