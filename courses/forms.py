from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.password_validation import validate_password, get_default_password_validators

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(StudentRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'instructor', 'scheduled', 'prerequisites', 'capacity']
        widgets = {
            'prerequisites': forms.CheckboxSelectMultiple,  # Optional: use checkboxes for multiple selection
        }
class StudentLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput())

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'instructor', 'scheduled', 'prerequisites', 'capacity']

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['scheduled'].queryset = self.get_available_schedules()

    def get_available_schedules(self):
        # احصل على جميع الجداول الزمنية
        schedules = CourseSchedule.objects.all()
        available_schedules = CourseSchedule.objects.none()
        for schedule in schedules:
            # تحقق إذا كان هناك تعارض في الوقت والقاعة
            if not Course.objects.filter(scheduled=schedule).exists():
                available_schedules |= CourseSchedule.objects.filter(id=schedule.id)
        return available_schedules
class CourseScheduleForm(forms.ModelForm):
    class Meta:
        model = CourseSchedule
        fields = ['days', 'start_time', 'end_time', 'room_no']

class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', "email", 'password']

class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")

            try:
                validate_password(password1, self.instance, password_validators=get_default_password_validators())
            except forms.ValidationError as error:
                self.add_error('password1', error)

        return cleaned_data

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
