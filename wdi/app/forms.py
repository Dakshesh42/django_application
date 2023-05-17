from django import forms
import datetime
from django.db.models import Sum
from datetime import timedelta
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ValidationError, ModelForm
from .models import Employee, Ips, Project, Attendance, Resource, Client, ClientContact, Menu, Sprint
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation, authenticate



class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Again',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = Employee
        fields = ['email', 'first_name', 'last_name', 'gender', 'phone', 'date_of_birth', 'joining_date', 'qualification', 'designation', 'address', 'ctc','resume', 'picture','edu_docs', 'aadhar', 'pan','certificate','additional_certificate']
        labels = {'email':'Email'}
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'phone': PhoneNumberPrefixWidget(initial='IN'),
            'date_of_birth':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'joining_date':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'designation':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'ctc':forms.NumberInput(attrs={'class':'form-control'}),
            'resume':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'picture':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'edu_docs':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'aadhar':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'pan':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'certificate':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'additional_certificate':forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.filter(email=email).exists():
                raise ValidationError("A User with this Email already exists")
        return self.cleaned_data
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditEmployeeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Employee
        # fields = ['email', 'name', 'gender', 'emp_code', 'phone', 'date_of_birth', 'joining_date', 'qualification', 'designation', 'address', 'resume', 'edu_docs', 'identity_docs', 'skill_docs']
        fields = '__all__'
        exclude = ('hr','acc','is_active','is_admin','emp_id', 'password')
        labels = {'email':'Email'}
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'joining_date':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'designation':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'ctc':forms.NumberInput(attrs={'class':'form-control'}),
            'resume':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'picture':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'edu_docs':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'aadhar':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'pan':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'certificate':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'additional_certificate':forms.ClearableFileInput(attrs={'class':'form-control'}),
        }    


class LoginForm(forms.Form):
    email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    

        # widgets = {
        #     'email':forms.EmailInput(attrs={'class':'form-control'}),
        #     # 'password':forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'})
        #     }
    def clean(self):
        if self.is_valid():

            email=self.cleaned_data.get('email')
            password=self.cleaned_data.get('password')

            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid LOGIN")    
# class LoginForm(AuthenticationForm):
#     email = UsernameField(widget=forms.EmailInput(attrs={'autofocus':True,'class':'form-control'}))
#     password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


# class IpsForm(forms.ModelForm):
#     class Meta:
#         model = Ips
#         fields = ['project', 'task', 'comments','hours']
#         labels = {'hours':'Hours(HH:MM:SS)'}
#         widgets = {
#             'project':forms.Select(attrs={'class':'form-control'}),
#             'task':forms.Select(attrs={'class':'form-control'}),
#             'comments':forms.TextInput(attrs={'class':'form-control'}),
#             'hours':forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control'}),
#         }

# class DurationWidget(forms.MultiWidget):
#     def __init__(self, attrs=None):
#         hours_choices = [(i, str(i)) for i in range(0, 11)]
#         minutes_choices = [(i, str(i).zfill(2)) for i in range(0, 60)]
#         widgets = [
#             forms.Select(attrs=attrs, choices=hours_choices),
#             forms.Select(attrs=attrs, choices=minutes_choices)
#         ]
#         super().__init__(widgets, attrs)

#     def decompress(self, value):
#         if value:
#             hours, minutes, seconds = value.components
#             return [hours, minutes]
#         return [None, None]

#     def value_from_datadict(self, data, files, name):
#         hours, minutes = super().value_from_datadict(data, files, name)
#         if hours and minutes:
#             return f"{hours}:{minutes}:00"
#         return None

# class DurationWidget(forms.MultiWidget):
#     def __init__(self, attrs=None):
#         hours_choices = [(i, str(i)) for i in range(0, 11)]
#         minutes_choices = [(i, str(i).zfill(2)) for i in range(0, 60)]
#         widgets = [
#             forms.Select(attrs=attrs, choices=hours_choices),
#             forms.Select(attrs=attrs, choices=minutes_choices)
#         ]
#         super().__init__(widgets, attrs)

#     def decompress(self, value):
#         if isinstance(value, str):
#             hours, minutes, seconds = value.split(':')
#             return [int(hours), int(minutes)]
#         elif value:
#             hours, minutes, seconds = value.components
#             return [hours, minutes]
#         return [None, None]

#     def value_from_datadict(self, data, files, name):
#         hours, minutes = super().value_from_datadict(data, files, name)
#         if hours and minutes:
#             return f"{hours}:{minutes}:00"
#         return None


# class IpsForm(forms.ModelForm):
#     project = forms.ModelChoiceField(queryset=Project.objects.none(),widget=forms.Select(attrs={'class': 'form-control'}))
#     hours = forms.DurationField(widget=DurationWidget(attrs={'class': 'form-control formselect'}))

    

    # def clean(self):
    #     cleaned_data = super().clean()

    #     # Combine hours and minutes to create a duration
    #     hours = cleaned_data.get('hours', 0)
    #     minutes = cleaned_data.get('minutes', 0)
    #     duration = timezone.timedelta(hours=hours, minutes=minutes)

    #     # Set the duration in the cleaned_data dictionary
    #     cleaned_data['hours'] = duration

    #     return cleaned_data

    # class Meta:
    #     model = Ips
    #     fields = ['project', 'task', 'comments', 'hours', 'minutes']
    #     labels = {'hours':'Hours(HH:MM:SS)'}
    #     widgets = {
    #         'project':forms.Select(attrs={'class':'form-control'}),
    #         'task':forms.Select(attrs={'class':'form-control'}),
    #         'comments':forms.TextInput(attrs={'class':'form-control'}),
    #         'minutes': forms.NumberInput(attrs={'class': 'form-control', 'step': 15, 'min': 0, 'max': 45}),
    #         # 'hours':forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control'}),
    #     }
    # class Meta:
    #     model = Ips
    #     fields = ['project', 'task', 'comments', 'hours']
    #     labels = {'hours':'Hours(HH:MM:SS)'}
    #     widgets = {
    #         'project':forms.Select(attrs={'class':'form-control'}),
    #         'task':forms.Select(attrs={'class':'form-control'}),
    #         'comments':forms.TextInput(attrs={'class':'form-control'}),
    #     }

class IpsForm(forms.ModelForm):
    hours = forms.ChoiceField(choices=[(i, i) for i in range(1, 13)], label='Hours',widget=forms.Select(attrs={'class':'form-control'}))
    minutes = forms.ChoiceField(choices=[(i, i) for i in range(0, 60, 15)], label='Minutes',widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = Ips
        fields = ['project', 'task', 'comments']
        widgets = {
            'project':forms.Select(attrs={'class':'form-control','id':'ip_pro'}),
            'task':forms.Select(attrs={'class':'form-control'}),
            'comments':forms.TextInput(attrs={'class':'form-control'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'client', 'client_contact', 'start_date', 'delivery_date', 'currency', 'project_value', 'hours_approvedby', 'sales_rep', 'project_manager', 'status', 'type', 'hours', 'max_hours', 'no_milestone']
        widgets = {
            'project_name':forms.TextInput(attrs={'class':'form-control'}),
            'client':forms.Select(attrs={'class':'form-control'}),
            'client_contact':forms.TextInput(attrs={'class':'form-control'}),
            'start_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'delivery_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'currency':forms.Select(attrs={'class':'form-control'}),
            'project_value':forms.NumberInput(attrs={'class':'form-control'}),
            'hours_approvedby':forms.TextInput(attrs={'class':'form-control'}),
            'sales_rep':forms.TextInput(attrs={'class':'form-control'}),
            'project_manager':forms.TextInput(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control'}),
            'hours':forms.NumberInput(attrs={'class':'form-control'}),
            'max_hours':forms.NumberInput(attrs={'class':'form-control'}),
            'no_milestone':forms.NumberInput(attrs={'class':'form-control','id':'num-input'}),
        }


class EmployeePasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))



class CheckoutForm(forms.ModelForm):
    checkout = forms.DateTimeField(initial=datetime.datetime.now(), 
        widget=forms.HiddenInput())
    class Meta:
        model = Attendance
        fields = ['checkout']
        
        
class ResourceForm(forms.ModelForm):
    hours = forms.ChoiceField(choices=[(i, i) for i in range(50, 2501, 50)], label='Hours',widget=forms.Select(attrs={'class':'form-control'}))
    max_hours = forms.ChoiceField(choices=[(i, i) for i in range(100, 5001, 100)], label='Max Hours',widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Resource
        fields = ('employee', 'project')
        widgets = {
                'employee' : forms.Select(attrs={'class':'form-control'}),
                'project' : forms.Select(attrs={'class':'form-control','id':'res_project'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        emp = cleaned_data.get('employee')
        hours = cleaned_data.get('hours')
        if hours:
            small = timedelta(hours=int(hours))
        else:
            small = 'Not Assigned'
        max_hours = cleaned_data.get('max_hours')
        if max_hours:
            big = timedelta(hours=int(max_hours))
        else:
            big = 'Not Assigned'
        old=Resource.objects.filter(employee=emp, project=project).exists()

        # if old:
        #     raise ValidationError("Resource already allocated.")

        if project and hours:
            # Check if the total resource hours for this project exceed the project hours
            total_resource_hours = project.resource_set.exclude(pk=self.instance.pk).aggregate(Sum('hours'))['hours__sum'] or timedelta()
            if total_resource_hours + small > project.hours:
                raise ValidationError(f"The total resource hours exceed the project hours ({project.hours.total_seconds() / 3600} hrs).")

        if project and max_hours:
            # Check if the total resource max_hours for this project exceed the project max_hours
            total_resource_max_hours = project.resource_set.exclude(pk=self.instance.pk).aggregate(Sum('max_hours'))['max_hours__sum'] or timedelta()
            if total_resource_max_hours + big > project.max_hours:
                raise ValidationError(f"The total resource max_hours exceed the project max_hours ({project.max_hours.total_seconds() / 3600} hrs).")


class ReportForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    model = forms.ChoiceField(choices=[
        ('ips', 'Ips'),
        ('resource', 'Resource'),
        ('task', 'Task'),
        ('project', 'Project'),
        ('employee', 'Employee'),
    ])

    def get_queryset(self):
        if not self.is_valid():
            return None

        model = self.cleaned_data['model']
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        if model == 'ips':
            return Ips.objects.filter(date__range=(start_date, end_date))
        elif model == 'resource':
            return Resource.objects.filter(date__range=(start_date, end_date))
        elif model == 'task':
            return Task.objects.filter(date__range=(start_date, end_date))
        elif model == 'project':
            return Project.objects.filter(date__range=(start_date, end_date))
        elif model == 'employee':
            return Employee.objects.filter(created_at__range=(start_date, end_date))
        else:
            return None
        
        
class AttendanceFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type':'date'}))
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name','company_name', 'contact_number', 'email', 'address', 'city', 'state', 'country', 'billing_name', 'pan_number', 'gst_number', 'client_doc']
        widgets = {
                'client_name' : forms.TextInput(attrs={'class':'form-control'}),
                'company_name' : forms.TextInput(attrs={'class':'form-control'}),
                'contact_number' : forms.NumberInput(attrs={'class':'form-control'}),
                'email' : forms.EmailInput(attrs={'class':'form-control'}),
                'address' : forms.TextInput(attrs={'class':'form-control'}),
                'city' : forms.TextInput(attrs={'class':'form-control'}),
                'state' : forms.TextInput(attrs={'class':'form-control'}),
                'country' : forms.Select(attrs={'class':'form-control'}),
                'billing_name' : forms.TextInput(attrs={'class':'form-control'}),
                'pan_number' : forms.TextInput(attrs={'class':'form-control'}),
                'gst_number' : forms.TextInput(attrs={'class':'form-control'}),
                'client_doc' : forms.ClearableFileInput(attrs={'class':'form-control'}),
        }


class ClientContactForm(forms.ModelForm):
    class Meta:
        model = ClientContact
        fields = ['client','first_name', 'last_name', 'designation', 'gender', 'company_email', 'personal_email', 'phone', 'skype_id', 'whatsapp']
        widgets = {
                'client' : forms.Select(attrs={'class':'form-control'}),
                'first_name' : forms.TextInput(attrs={'class':'form-control'}),
                'last_name' : forms.TextInput(attrs={'class':'form-control'}),
                'designation' : forms.TextInput(attrs={'class':'form-control'}),
                'gender' : forms.Select(attrs={'class':'form-control'}),
                'company_email' : forms.EmailInput(attrs={'class':'form-control'}),
                'personal_email' : forms.EmailInput(attrs={'class':'form-control'}),
                'phone' : forms.NumberInput(attrs={'class':'form-control'}),
                'skype_id' : forms.TextInput(attrs={'class':'form-control'}),
                'whatsapp' : forms.NumberInput(attrs={'class':'form-control'}),
        }


class MenuForm(forms.Form):
    OPTIONS = [
        ('Ritesh Pandey', 'Ritesh Pandey'),
        ('Rushabh Parekh', 'Rushabh Parekh'),
    ]
    ONIONS = [
        ('CEO', 'CEO'),
        ('Project Manager', 'Project Manager'),
    ]
    staff = forms.ChoiceField(choices=OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))
    staff_desig = forms.ChoiceField(choices=ONIONS, widget=forms.Select(attrs={'class': 'form-control'}))
    client_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    for_client = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ('name', 'hours')
        widgets = {
                'name' : forms.TextInput(attrs={'class':'form-control'}),
                'hours' : forms.NumberInput(attrs={'class':'form-control'}),
        }
