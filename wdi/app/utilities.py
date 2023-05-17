from .models import Employee, Ips, Project, Attendance, Resource
from django.db.models import Sum
from datetime import time
from django.utils.timezone import timedelta
from django.utils import timezone




def get_attendance_for_date(date):
    # Get all attendances for the given date
    attendances = Attendance.objects.filter(date=date)

    # Create a dictionary to hold check-in and check-out times for each employee
    employee_times = {}

    # Iterate over each attendance object and populate the dictionary
    for attendance in attendances:
        employee_id = attendance.employee.emp_id

        if employee_id not in employee_times:
            # Initialize the dictionary entry for the employee if it doesn't exist
            employee_times[employee_id] = {
                'name': attendance.employee.first_name,
                'checkin': None,
                'checkout': None
            }

        # Update the check-in and check-out times for the employee
        if attendance.id:
            employee_times[employee_id]['id'] = attendance.id
        if attendance.checkin:
            employee_times[employee_id]['checkin'] = attendance.checkin
        if attendance.checkout:
            employee_times[employee_id]['checkout'] = attendance.checkout
        if attendance.status:
            employee_times[employee_id]['status'] = attendance.status
        

    return employee_times


# def get_employees_not_checked_in(date):
#     checked_in_employees = Attendance.objects.filter(
#         date=date, checkin__isnull=False
#     ).values_list("employee", flat=True)
#     employees_not_checked_in = Employee.objects.exclude(
#         id__in=checked_in_employees
#     ).values_list("id", flat=True)
#     return employees_not_checked_in


def get_employees_not_checked_in(date):
    checked_in_employee_ids = Attendance.objects.filter(date=date, checkin__isnull=False).values_list("employee", flat=True)
    marked_absent_employee_ids = Attendance.objects.filter(date=date, status='AB').values_list("employee", flat=True)
    employees_not_checked_in = Employee.objects.exclude(id__in=checked_in_employee_ids).exclude(id__in=marked_absent_employee_ids)
    return employees_not_checked_in


# def get_attendance_for_datetime(date):
#     # Get all attendances for the given date
#     attendances = Attendance.objects.filter(date=date)

#     # Create a dictionary to hold check-in and check-out times for each employee
#     employee_times = {}

#     # Create separate lists for employees who checked in before and after 12:30 PM
#     before_1230_employees = []
#     after_1230_employees = []

#     # Iterate over each attendance object and populate the dictionary
#     for attendance in attendances:
#         employee_id = attendance.employee.emp_id

#         if employee_id not in employee_times:
#             # Initialize the dictionary entry for the employee if it doesn't exist
#             employee_times[employee_id] = {
#                 'name': attendance.employee.first_name,
#                 'checkin': None,
#                 'checkout': None,
#                 'status': None
#             }

#         # Update the check-in and check-out times for the employee
#         if attendance.id:
#             employee_times[employee_id]['id'] = attendance.id
#         if attendance.checkin:
#             employee_times[employee_id]['checkin'] = attendance.checkin
#         if attendance.checkout:
#             employee_times[employee_id]['checkout'] = attendance.checkout
#         if attendance.status:
#             employee_times[employee_id]['status'] = attendance.status

#         # Add the employee to the appropriate list based on check-in time
#         # target_time = timezone.time(hour=12, minute=30)
#         target_time = timezone.make_aware(time(hour=12, minute=30), timezone.get_current_timezone())

#         checkin_time = employee_times[employee_id]['checkin']
#         if checkin_time and checkin_time.time() < target_time:
#             before_1230_employees.append(employee_times[employee_id])
#         elif checkin_time and checkin_time.time() >= target_time:
#             after_1230_employees.append(employee_times[employee_id])

#     return before_1230_employees, after_1230_employees

def get_attendance_for_datetime(date):
    # Get all attendances for the given date
    attendances = Attendance.objects.filter(date=date)

    # Create a dictionary to hold check-in and check-out times for each employee
    employee_times = {}

    # Create separate lists for employees who checked in before and after 12:30 PM
    before_1230_employees = []
    after_1230_employees = []

    # Get the timezone of the server
    server_timezone = timezone.get_current_timezone()

    # Iterate over each attendance object and populate the dictionary
    for attendance in attendances:
        employee_id = attendance.employee.emp_id

        if employee_id not in employee_times:
            # Initialize the dictionary entry for the employee if it doesn't exist
            employee_times[employee_id] = {
                'name': attendance.employee.first_name,
                'checkin': None,
                'checkout': None,
                'status': None
            }

        # Update the check-in and check-out times for the employee
        if attendance.id:
            employee_times[employee_id]['id'] = attendance.id
        if attendance.checkin:
            # Convert the check-in time to the server timezone
            employee_times[employee_id]['checkin'] = timezone.localtime(attendance.checkin, server_timezone)
        if attendance.checkout:
            employee_times[employee_id]['checkout'] = attendance.checkout
        if attendance.status:
            employee_times[employee_id]['status'] = attendance.status

        # Add the employee to the appropriate list based on check-in time
        target_time = timezone.make_aware(time(hour=12, minute=30), server_timezone)

        checkin_time = employee_times[employee_id]['checkin']
        if checkin_time and checkin_time.time() < target_time:
            before_1230_employees.append(employee_times[employee_id])
        elif checkin_time and checkin_time.time() >= target_time:
            after_1230_employees.append(employee_times[employee_id])

    return before_1230_employees, after_1230_employees



def get_remaining_project_hours(id):
    pro = Project.objects.get(id=id)
    total_hours = Resource.objects.filter(project=pro).aggregate(total_hours=Sum('hours'))['total_hours'] or timedelta(seconds=0)
    remaining_hours = pro.hours - total_hours
    total_seconds = remaining_hours.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    return f"{hours} hrs {minutes} mins"


def get_remaining_project_max_hours(id):
    pro = Project.objects.get(id=id)
    total_max_hours = Resource.objects.filter(project=pro).aggregate(total_max_hours=Sum('max_hours'))['total_max_hours'] or timedelta(seconds=0)
    remaining_max_hours = pro.max_hours - total_max_hours
    total_seconds = remaining_max_hours.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    return f"{hours} hrs {minutes} mins"


def format_duration(duration):
    hours = int(duration.total_seconds() / 3600)
    minutes = int((duration.total_seconds() % 3600) / 60)
    return f"{hours} hrs {minutes} mins"




