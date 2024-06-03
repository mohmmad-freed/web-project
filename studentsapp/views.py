from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Student, Course, CourseSchedule, StudentRegistration
from .forms import StudentRegistrationForm, StudentLoginForm, CourseForm, CourseScheduleForm, StudentForm, UserUpdateForm
from django.contrib.auth.models import User
from .decorators import student_required, admin_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    request.session.flush()  # Clear the session data
    return redirect('login')

@login_required
@admin_required
def course_report(request):
    courses = Course.objects.all()
    report_data = []

    for course in courses:
        enrollment_count = StudentRegistration.objects.filter(course=course).count()
        popularity = (enrollment_count / course.capacity) * 100 if course.capacity > 0 else 0
        report_data.append({
            'course': course,
            'enrollment_count': enrollment_count,
            'popularity': popularity
        })

    report_data.sort(key=lambda x: x['enrollment_count'], reverse=True)

    most_popular_course = report_data[0] if report_data else None
    least_popular_course = report_data[-1] if report_data else None

    context = {
        'report_data': report_data,
        'most_popular_course': most_popular_course,
        'least_popular_course': least_popular_course
    }
    return render(request, 'courses/course_report.html', context)

@login_required
@student_required
def delete_course(request, course_code):
    student = get_object_or_404(Student, id=request.session['student_id'])
    course = get_object_or_404(Course, code=course_code)
    
    registration = StudentRegistration.objects.filter(student=student, course=course).first()
    if registration:
        registration.delete()
        messages.success(request, f"You have successfully unregistered from {course.name}.")
    else:
        messages.error(request, "You are not registered for this course.")
    
    return redirect('home')

@login_required
@student_required
def register_course(request, course_code):
    student = get_object_or_404(Student, id=request.session['student_id'])
    course = get_object_or_404(Course, code=course_code)

    if StudentRegistration.objects.filter(student=student, course=course).exists():
        messages.error(request, "You are already registered for this course.")
        return redirect('home')

    student_courses = StudentRegistration.objects.filter(student=student)
    for registration in student_courses:
        if registration.course:
            registered_schedule = registration.course.scheduled
            new_schedule = course.scheduled
            if registered_schedule.days == new_schedule.days and (
                (registered_schedule.start_time <= new_schedule.start_time < registered_schedule.end_time) or 
                (registered_schedule.start_time < new_schedule.end_time <= registered_schedule.end_time)
            ):
                messages.error(request, f"Schedule conflict detected with course {registration.course.code}.")
                return redirect('home')

    for prerequisite in course.prerequisites.all():
        if not StudentRegistration.objects.filter(student=student, course=prerequisite).exists():
            messages.error(request, f"You do not meet the prerequisites for this course: {prerequisite.name}.")
            return redirect('home')

    if course.capacity <= StudentRegistration.objects.filter(course=course).count():
        messages.error(request, "This course is already full.")
        return redirect('home')

    StudentRegistration.objects.create(student=student, course=course)
    messages.success(request, "You have successfully registered for the course.")
    return redirect('home')

@login_required
@student_required
def profile(request):
    if 'student_id' not in request.session:
        messages.error(request, "Session expired or not set. Please log in again.")
        return redirect('login')
    
    student = get_object_or_404(Student, id=request.session['student_id'])
    user = student.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password1']:
                user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserUpdateForm(instance=user)
    
    context = {
        'student': student,
        'form': form
    }
    return render(request, 'courses/profile.html', context)

@login_required
@student_required
def home(request):
    query = request.GET.get('search_query', '')
    courses = Course.objects.filter(
        Q(code__icontains=query) | 
        Q(name__icontains=query) | 
        Q(instructor__icontains=query)
    )
    student = None
    registered_courses = set()
    if 'student_id' in request.session:
        student = Student.objects.get(id=request.session['student_id'])
        registered_courses = set(StudentRegistration.objects.filter(student=student).values_list('course__code', flat=True))

    course_data = []
    for course in courses:
        prerequisites_met = all(StudentRegistration.objects.filter(student=student, course=prerequisite).exists() for prerequisite in course.prerequisites.all())
        if prerequisites_met:
            registered_students_count = StudentRegistration.objects.filter(course=course).count()
            available_spots = course.capacity - registered_students_count
            course_data.append({
                'course': course,
                'available_spots': available_spots,
                'registered_students_count': registered_students_count,
                'is_registered': course.code in registered_courses,
            })

    context = {
        'student': student,
        'course_data': course_data,
        'query': query,
    }
    return render(request, "courses/dashbord.html", context)

def login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('student_course_list')
                else:
                    try:
                        student = Student.objects.get(user=user)
                        request.session['student_id'] = student.id
                    except Student.DoesNotExist:
                        messages.error(request, "Student profile not found.")
                        return redirect('login')
                    return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = StudentLoginForm()
    return render(request, 'courses/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = StudentRegistrationForm()
    return render(request, 'courses/register.html', {'form': form})

@login_required
@student_required
def my_courses(request):
    if 'student_id' not in request.session:
        messages.error(request, "Session expired or not set. Please log in again.")
        return redirect('login')
    
    try:
        student = get_object_or_404(Student, id=request.session['student_id'])
        student_courses = StudentRegistration.objects.filter(student=student)
    
        context = {
            'student': student,
            'student_courses': student_courses
        }
        return render(request, "courses/my_courses.html", context)
    except KeyError as e:
        messages.error(request, "Session error: please log in again.")
        return redirect('login')
    except Student.DoesNotExist:
        messages.error(request, "Student not found. Please log in again.")
        return redirect('login')

@login_required
@admin_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/addcourses.html', {'form': form})

@login_required
@admin_required
def course_lista(request):
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {'courses': courses})

@login_required
@admin_required
def add_schedule(request):
    if request.method == 'POST':
        form = CourseScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')  
    else:
        form = CourseScheduleForm()
    return render(request, 'courses/addSchedule.html', {'form': form})

@login_required
@admin_required
def schedule_list(request):
    schedules = CourseSchedule.objects.all()
    return render(request, 'courses/schedule_list.html', {'schedules': schedules})

@login_required
@admin_required
def student_course_list(request):
    students = Student.objects.all()
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Student.objects.create(user=user)
            return redirect('student_course_list')
    else:
        form = StudentForm()

    return render(request, 'courses/student_course_list.html', {'students': students, 'form': form})
