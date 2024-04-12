from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Assignment, Submission, User
from django.http import HttpResponseBadRequest

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def register_user(request):
    if request.method == 'POST':
        # Process user registration form
        form = UserCreationForm(request.POST)  # Create user creation form
        if form.is_valid():
            form.save()  # Save the new user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Access password securely
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the newly registered user
                return redirect('student_view.html')  # Redirect to your desired homepage after registration
            else:
                # Handle authentication failure (shouldn't happen ideally)
                return render(request, 'register.html', {'form': form, 'error': 'Authentication failed'})
        else:
            # Handle form validation errors
            return render(request, 'register.html', {'form': form})
    else:
        # Display registration form
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        # Process login form
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Log in the authenticated user
            return redirect('student_view.html')  # Redirect to your desired homepage after login
        else:
            # Handle invalid credentials
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        # Display login form
        return render(request, 'login.html')

@login_required
def student_view(request):
    assignments = Assignment.objects.filter(course__in=request.user.course_set.all())
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'student_view.html', {'assignments': assignments, 'submissions': submissions})
def calculate_grade(content, keywords, marking_scheme):
    # Implement your custom grading logic here (replace with actual logic)
    # Simulate basic keyword matching for demonstration purposes
    grade = 0
    for keyword in keywords.split(','):
        if keyword.strip() in content:
            grade += marking_scheme.get(keyword.strip(), 0)
    return grade

@login_required
def student_view(request):
    assignments = Assignment.objects.filter(course__in=request.user.course_set.all())
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'student_view.html', {'assignments': assignments, 'submissions': submissions})

@login_required
def assignment_detail(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    if request.method == 'POST':
        content = request.POST['content']
        if len(content) == 0:
            return HttpResponseBadRequest('Submission content cannot be empty')
        submission = Submission.objects.create(student=request.user, assignment=assignment, content=content)
        submission.grade = calculate_grade(content, assignment.keywords, assignment.marking_scheme)
        submission.save()
        return redirect('student_view')
    return render(request, 'assignment_detail.html', {'assignment': assignment})

@login_required
def lecturer_view(request):
    courses = Course.objects.filter(lecturer=request.user)
    assignments = Assignment.objects.filter(course__in=courses)
    return render(request, 'lecturer_view.html', {'courses': courses, 'assignments': assignments})

@login_required
def create_assignment(request, course_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = datetime.datetime.strptime(request.POST['due_date'], '%Y-%m-%d %H:%M')
        keywords = request.POST['keywords']
        try:
            marking_scheme = json.loads(request.POST['marking_scheme'])  # Parse JSON marking scheme
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON format for marking scheme')
        course = Course.objects.get(pk=course_id)
        Assignment.objects.create(title=title, description=description, due_date=due_date,
                                  keywords=keywords, marking_scheme=marking_scheme, course=course)
        return redirect('lecturer_view')
    return render(request, 'create_assignment.html')

@login_required
def view_submissions(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'view_submissions.html', {'assignment': assignment, 'submissions':submissions})

