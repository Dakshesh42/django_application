from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import Project, Employee, Ips, Attendance, Resource, Client, Milestone, Sprint
from .forms import SignUpForm, EditEmployeeForm
# Register your models here.

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['id','user','code', 'designation','address', 'joining_date', 'qualification', 'resume', 'identity','date_created','status']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'project_name', 'client', 'client_contact', 'start_date', 'delivery_date', 'currency', 'project_value', 'hours', 'max_hours', 'hours_approvedby', 'sales_rep', 'project_manager', 'status', 'type', 'date']

@admin.register(Ips)
class IpsAdmin(admin.ModelAdmin):
    list_display = ['id','employee', 'project', 'task','comments', 'hours','date']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','company_name', 'contact_number', 'email', 'address', 'city', 'state', 'country', 'billing_name', 'pan_number', 'gst_number', 'client_doc']

# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['id','name','project', 'hours','date']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['id','employee', 'project', 'hours', 'max_hours', 'date']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id','employee','checkin','checkout', 'date','status']

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['id','project','name','hours', 'delivery_date']

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ['id','name','milestone','hours']

# @admin.register(EmployeeProfile)
# class EmployeeProfileAdmin(admin.ModelAdmin):
#     list_display = ['id','details', 'picture', 'resume','edu_docs', 'identity_docs']


# class EmployeeAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = EditEmployeeForm
#     add_form = SignUpForm

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = (
#         'id',
#         'email', 
#         'name',
#         'gender',
#         'phone',
#         'date_of_birth',
#         'joining_date',
#         'qualification',
#         'designation',
#         'address',
#         'ctc',
#         'resume',
#         'edu_docs',
#         'aadhar',
#         'pan',
#         'certificate',
#         'additional_certificate',
#         'hr',
#         'acc',
#         'is_active',
#         'is_staff',
#         'is_admin',
#         'created_at',
#         'updated_at'
#         )
#     list_filter = (
#         'is_admin',
#         'phone',
#         'designation'
#         )
#     fieldsets = (
#         ('Employee Credentials', {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('name', 'gender','phone', 'date_of_birth', 'joining_date', 'qualification', 'designation', 'address','ctc','resume', 'edu_docs', 'aadhar', 'pan','certificate','additional_certificate')}),
#         ('Permissions', {'fields': ('is_admin', 'hr', 'acc',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'name', 'gender', 'phone', 'date_of_birth', 'joining_date', 'qualification', 'designation', 'address', 'ctc','hr', 'acc', 'resume', 'edu_docs', 'aadhar', 'pan','certificate', 'additional_certificate','password1', 'password2'),
#         }),
#     )
#     search_fields = ('email','designation','name')
#     ordering = ('email','id')
#     filter_horizontal = ()


# # Now register the new UserAdmin...
# admin.site.register(Employee, EmployeeAdmin)

class EmployeeAdmin(BaseUserAdmin):
    # The forms to add and change user instances


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 
                    'email',
                    'emp_id', 
                    'first_name', 
                    'last_name', 
                    'gender',
                    'phone', 
                    'date_of_birth', 
                    'joining_date', 
                    'qualification', 
                    'designation', 
                    'address', 
                    'ctc',
                    'resume',
                    'picture', 
                    'edu_docs', 
                    'aadhar', 
                    'pan',
                    'certificate', 
                    'additional_certificate',
                    'hr', 'acc', 'is_active', 'is_staff', 'is_admin', 'created_at', 'updated_at')
    list_filter = ('is_admin', 'phone', 'designation')
    fieldsets = (
        ('Employee Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender','phone', 'date_of_birth', 'joining_date', 'qualification', 'designation', 'address','ctc','resume', 'picture','edu_docs', 'aadhar', 'pan','certificate','additional_certificate')}),
        ('Permissions', {'fields': ('is_admin', 'hr', 'acc',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'gender', 'phone', 'date_of_birth', 'joining_date', 'qualification', 'designation', 'address', 'ctc','hr', 'acc', 'resume', 'picture', 'edu_docs', 'aadhar', 'pan','certificate', 'additional_certificate','password1', 'password2'),
        }),
    )
    search_fields = ('email','designation','first_name', 'last_name', 'emp_id')
    ordering = ('email','id')
    filter_horizontal = ()
    
    
admin.site.register(Employee, EmployeeAdmin)