import calendar
import datetime
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .forms import TaskForm
from .models import Task


# Create your views here.
def projecthomepage(request):
    return render(request, 'adminapp/ProjectHomePage.html')


def printpagecall(request):
    return render(request, 'adminapp/printer.html')


def printpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        print(f'User input: {user_input}')
        a1 = {'user_input': user_input}
        return render(request, 'adminapp/printer.html', a1)
    return render(request, 'adminapp/printer.html')


def exceptionpagecall(request):
    return render(request, 'adminapp/ExceptionExample.html')


def exceptionpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        result = None
        error_message = None
        try:
            num = int(user_input)
            result = 10 / num
        except Exception as e:
            error_message = str(e)
        return render(request, 'adminapp/ExceptionExample.html', {'result': result, 'error': error_message})
    return render(request, 'adminapp/ExceptionExample.html')


def randompagecall(request):
    return render(request, 'adminapp/randomexample.html')


def randomlogic(request):
    if request.method == "POST":
        number1 = int(request.POST['number1'])
        ran = ''.join(random.sample(string.ascii_uppercase + string.digits, k=number1))
        a1 = {'ran': ran}
        return render(request, 'adminapp/randomexample.html', a1)
    return render(request, 'adminapp/randomexample.html')


def calculatorpagecall(request):
    return render(request, 'adminapp/calculator.html')


def calculatorlogic(request):
    result = None
    if request.method == 'POST':
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        operation = request.POST.get('operation')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else 'Infinity'

    return render(request, 'adminapp/calculator.html', {'result': result})


def datetimepagecall(request):
    return render(request, 'adminapp/datetimepage.html')


def datetimepagelogic(request):
    if request.method == "POST":
        number1 = int(request.POST['date1'])
        x = datetime.datetime.now()
        ran = x + datetime.timedelta(days=number1)
        ran1 = ran.year
        ran2 = calendar.isleap(ran1)
        ran3 = "Leap Year" if ran2 else "Not Leap Year"
        a1 = {'ran': ran, 'ran3': ran3, 'ran1': ran1, 'number1': number1}
        return render(request, 'adminapp/datetimepage.html', a1)
    return render(request, 'adminapp/datetimepage.html')


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request, 'adminapp/To-Do-List.html', {'form': form, 'tasks': tasks})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')


def UserRegisterPageCall(request):
    return render(request, 'adminapp/Register.html')


def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                login(request, user)
                messages.info(request, 'Account created and logged in successfully!')

                # Redirect based on username length
                if len(username) == 4:
                    return redirect('facultyhomepage')  # Adjust to faculty homepage URL
                elif len(username) == 10:
                    return redirect('studenthomepage')  # Adjust to student homepage URL
                else:
                    return redirect('projecthomepage')  # Default or project homepage
        else:
            messages.info(request, 'Passwords do not match.')
    return render(request, 'adminapp/Register.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check the length of the username and redirect accordingly
            if len(username) == 4:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"Successfully logged in as {username}.")
                    return redirect('facultyhomepage')  # Adjust to faculty homepage URL
                else:
                    messages.error(request, "Invalid username or password.")
            elif len(username) == 10:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"Successfully logged in as {username}.")
                    return redirect('studenthomepage')  # Adjust to student homepage URL
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Username length must be 4 or 10 characters.")
        else:
            print(form.errors.as_data())  # For debugging purposes
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()

    return render(request, 'adminapp/Login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


def add_post(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)  # Use a dedicated PostForm if available
        if form.is_valid():
            form.save()
            return redirect('add_post')  # Redirect to a page displaying posts
    else:
        form = TaskForm()
    posts = Task.objects.all()  # Consider renaming 'Task' to 'Post' if it's meant for blog posts
    return render(request, 'facultyapp/blogPost.html', {'form': form, 'posts': posts})  # Use 'posts' instead of 'tasks'


def delete_post(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_post')


def facultyhomepage(request):
    return render(request, 'facultyapp/FacultyHomePage.html')


def studenthomepage(request):
    return render(request, 'studentapp/StudentHomePage.html')


from .forms import StudentForm
from .models import StudentList


'''def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_details')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})'''

from django.contrib.auth.models import User
from .models import StudentList
from .forms import StudentForm
from django.shortcuts import redirect, render
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            register_number = form.cleaned_data['Register_Number']
            try:
                user = User.objects.get(username=register_number)
                student.user = user  # Assign the matching User to the student
            except User.DoesNotExist:
                form.add_error('Register_Number', 'No user found with this Register Number')
                return render(request, 'adminapp/add_student.html', {'form': form})
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})


def student_list(request):
    students = StudentList.objects.all()
    return render(request, 'adminapp/show_details.html', {'students': students})
