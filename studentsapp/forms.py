from django import forms
from .models import CourseSchedule, Student, Course

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CourseRegistrationForm(forms.Form):
    course_schedule = forms.ModelChoiceField(queryset=CourseSchedule.objects.all())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CourseRegistrationForm, self).__init__(*args, **kwargs)

    def clean_course_schedule(self):
        course_schedule = self.cleaned_data.get('course_schedule')
        course = course_schedule.course
        student = Student.objects.get(user=self.user)
        
        # Check if the student has completed all prerequisites
        prerequisites = course.prerequisites.all()
        completed_courses = student.schedules.filter(course__in=prerequisites)
        if prerequisites.count() != completed_courses.count():
            raise forms.ValidationError("You must complete all prerequisites before registering for this course.")
        
        return course_schedule
