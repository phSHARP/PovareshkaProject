from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, get_user
from .models import CourseType, Course
from .forms import CourseForm
import re
import urllib.parse


def index(request):
    return render(request, 'index.html')


def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('lk')
    else:
        form = AuthenticationForm()
    return render(request, 'log_in.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def article(request):
    match = re.fullmatch(r'/article/\?id=(\d+)', request.get_full_path_info())
    if match is not None:
        course_id = match.group(1)
        course = Course.objects.filter(id=course_id)[0]
        return render(request, 'article.html', {'course': course})


def details(request):
    match = re.fullmatch(r'/details/\?(\w+)=([\w ]+)', urllib.parse.unquote(request.get_full_path_info()))
    if match is not None:
        operation = match.group(1)
        if operation == 'type':
            course_type_name = match.group(2)
            course_type = CourseType.objects.filter(type_name=course_type_name)[0]
            courses = Course.objects.filter(course_type=course_type.id)
            return render(request, 'details.html', {'details_title': course_type.details_title, 'courses': courses})
        elif operation == 'search':
            search_string = match.group(2)
            courses = Course.objects.raw(f'SELECT * FROM PovareshkaProject_course WHERE name LIKE "%%{search_string}%%" OR receipt LIKE "%%{search_string}%%"')
            return render(request, 'details.html', {'details_title': f'Результаты поиска "{search_string}":', 'courses': courses})


def lk(request):
    current_user = get_user(request)
    courses = Course.objects.filter(author=current_user.id)
    return render(request, 'lk.html', {'username': current_user.username, 'courses': courses})


def new_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = get_user(request)
            course.save()
            return redirect('lk')
    else:
        form = CourseForm()
    return render(request, 'new_course.html', {'form': form})
