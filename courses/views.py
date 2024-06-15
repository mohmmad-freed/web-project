from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from django.contrib.auth.models import User, Group
from .decorators import *
from django.views.decorators.cache import cache_control
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


@allowed_users(allowed_roles=['admin'])
def save_selected_students(request):
    if request.method == 'POST':
        selected_student_ids = request.POST.getlist('student_ids[]')
        request.session['selected_student_ids'] = selected_student_ids

        
        courses = Course.objects.filter(students__id__in=selected_student_ids).distinct()

       
        course_data = []
        for course in courses:
            course_data.append({
                'code': course.code,
                'name': course.name,
                'prerequisites': ", ".join([prerequisite.name for prerequisite in course.prerequisites.all()]),
                'instructor': course.instructor,
                'completed': course.completed
            })

        return JsonResponse({'status': 'success', 'courses': course_data})
    return JsonResponse({'status': 'fail'})

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def update_course(request, course_code):
    course = get_object_or_404(Course, code=course_code)
    schedules = CourseSchedule.objects.all()
    prerequisites = Course.objects.exclude(code=course_code)  # Exclude current course from prerequisites

    if request.method == 'POST':
        form = CourseUpdateForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course {course.name} has been updated successfully.")
            return redirect('course_list')
    else:
        form = CourseUpdateForm(instance=course)

    context = {
        'course': course,
        'form': form,
        'schedules': schedules,
        'prerequisites': prerequisites,
    }

    return render(request, 'courses/Admin/update_course.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def student_registration(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_id')
        course_codes = request.POST.getlist('course_code')
        for student_id in student_ids:
            student = get_object_or_404(Student, id=student_id)
            for course_code in course_codes:
                course = get_object_or_404(Course, code=course_code)
                try:
                    StudentRegistration.objects.create(student=student, course=course)
                    messages.success(request, f"Successfully registered {student.user.username} for course {course.name}")
                except ValidationError as e:
                    messages.error(request, str(e))
        return redirect('student_registration')
    else:
        students = Student.objects.all()
        courses = Course.objects.all()

        selected_students = request.session.get('selected_students', [])
        if selected_students:
            courses = courses.filter(students__id__in=selected_students).distinct()

        context = {
            'students': students,
            'courses': courses,
        }
        return render(request, 'courses/Admin/student_registration.html', context)
@login_required(login_url="login")
@student_required

def courses(request):
    query = request.GET.get('search_query', '')
    student = None
    registered_courses = set()
    completed_courses = []

    if 'student_id' in request.session:
        student = Student.objects.get(id=request.session['student_id'])
        registered_courses = set(StudentRegistration.objects.filter(student=student).values_list('course__code', flat=True))
        completed_courses = StudentRegistration.objects.filter(student=student, completed=True)
        completed_courses_codes = [registration.course.code for registration in completed_courses]
    else:
        completed_courses_codes = []

    courses = Course.objects.filter(
        Q(code__icontains=query) | 
        Q(name__icontains=query)
    ).exclude(code__in=completed_courses_codes)

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
        'username': request.user.username,
        'completed_courses': completed_courses
    }
    return render(request, "courses/Student/courses.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
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
    return render(request, 'courses/Admin/course_report.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def delete_course(request, course_code):
    course = get_object_or_404(Course, code=course_code)
    course.delete()
    messages.success(request, f"Course {course.name} has been successfully deleted.")
    return redirect('course_list')

@login_required(login_url="login")
@student_required
def register_course(request, course_code):
    if 'student_id' not in request.session:
        raise PermissionDenied
    
    student = get_object_or_404(Student, id=request.session['student_id'])
    course = get_object_or_404(Course, code=course_code)

    if StudentRegistration.objects.filter(student=student, course=course).exists():
        messages.error(request, "You are already registered for this course.")
        return redirect('courses')

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
                return redirect('courses')

    for prerequisite in course.prerequisites.all():
        if not StudentRegistration.objects.filter(student=student, course=prerequisite).exists():
            messages.error(request, f"You do not meet the prerequisites for this course: {prerequisite.name}.")
            return redirect('courses')

    if course.capacity <= StudentRegistration.objects.filter(course=course).count():
        messages.error(request, "This course is already full.")
        return redirect('courses')

    StudentRegistration.objects.create(student=student, course=course)
    messages.success(request, "You have successfully registered for the course.")
    return redirect('courses')

@login_required(login_url="login")
@student_required
def profile(request):
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
    return render(request, 'courses/Student/profile.html', context)

@login_required(login_url="login")
@student_required
def home(request):
    if request.user.is_superuser:
        return redirect('homeAdmin')

    notifications = Notification.objects.filter(active=True).order_by('-date_created')

    context = {
        'notifications': notifications,
        'username': request.user.username,
    }
    return render(request, "courses/Student/home.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def homeAdmin(request):
    context = {
        'username': request.user.username,
    }
    return render(request, "courses/Admin/homeAdmin.html", context)

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
                    return redirect('homeAdmin')
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
    
    # Clear messages after processing the form
    storage = messages.get_messages(request)
    storage.used = True
    
    return render(request, 'courses/Student/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            group = Group.objects.get(name="student")
            user.groups.add(group)
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = StudentRegistrationForm()
    return render(request, 'courses/Student/register.html', {'form': form})

@login_required(login_url="login")
@student_required
def my_courses(request):
    if 'student_id' not in request.session:
        raise PermissionDenied
    
    student = get_object_or_404(Student, id=request.session.get('student_id'))
    student_courses = StudentRegistration.objects.filter(student=student)

    context = {
        'student': student,
        'student_courses': student_courses,
        'username': request.user.username,
    }
    return render(request, "courses/Student/my_courses.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/Admin/addcourses.html', {'form': form})

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def removeeditcourse(request):
    courses = Course.objects.all()
    return render(request, 'courses/Admin/remove&editcourse.html', {'courses': courses})

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def course_lista(request):
    courses = Course.objects.all()
    return render(request, 'courses/Admin/courses_list.html', {'courses': courses})

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def add_schedule(request):
    if request.method == 'POST':
        form = CourseScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')  
    else:
        form = CourseScheduleForm()
    return render(request, 'courses/Admin/addSchedule.html', {'form': form})

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def schedule_list(request):
    schedules = CourseSchedule.objects.all()
    return render(request, 'courses/Admin/schedule_list.html', {'schedules': schedules})

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
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

    return render(request, 'courses/Admin/student_course_list.html', {'students': students, 'form': form})

@login_required(login_url="login")
@student_required
def unregister_course(request, course_code):
    if 'student_id' not in request.session:
        raise PermissionDenied

    student = get_object_or_404(Student, id=request.session['student_id'])
    course = get_object_or_404(Course, code=course_code)

    registration = StudentRegistration.objects.filter(student=student, course=course).first()
    if not registration:
        messages.error(request, "You are not registered for this course.")
        return redirect('courses')

    registration.delete()
    messages.success(request, "You have successfully unregistered from the course.")
    return redirect('courses')
