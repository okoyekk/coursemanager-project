from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .forms import StudentRegisterForm, InstructorRegisterForm
from .models import User, Student, Instructor


def index(request):
    return render(request, "classmanager/index.html")


def login_view(request):
    login_form = AuthenticationForm()
    if request.method == "POST":
        # Attempt to sign user in
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "classmanager/login.html", {
                'login_form': login_form,
                "failure_message": "Invalid username and/or password."
            })
    else:
        return render(request, "classmanager/login.html", {
            'login_form': login_form
        })


@login_required
def logout_view(request):
    # Logs out user if authenticated
    # TODO make a message appear on index to say user just logged out
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    return render(request, "classmanager/register.html")


def register_user(request):
    if request.method == 'POST':
        user_form = request.POST
        context = {}
        # if user is not authenticated, try registering them (New user)
        if not request.user.is_authenticated:
            try:
                username = user_form["username"]
                password = user_form["password"]
                # Return a new register form if passwords don't match
                # TODO add javascript validation to avoid this
                if user_form["password"] != user_form["confirmation"]:
                    context['failure_message'] = 'Passwords do not match, please correct it.'
                else:
                    # Attempt creating a new user
                    user = User.objects.create_user(username=username, email=user_form["email"], password=password,
                                                    first_name=user_form["first-name"],
                                                    last_name=user_form["last-name"])
                    user.save()
                    # log in user if it was created without any exception
                    user = authenticate(username=username, password=password)
                    login(request, user)
            except IntegrityError:
                context['failure_message'] = 'Sorry, this username is already taken'
            except KeyError or ValueError:
                context['failure_message'] = 'Form is not valid, please correct it!'
            else:
                context['success_message'] = 'User created, now fill out either a Student or Instructor form'
            return render(request, "classmanager/register_user.html", context)
    else:
        return render(request, "classmanager/register_user.html")


def register_student(request):
    if request.method == 'POST':
        student_form = StudentRegisterForm(request.POST)
        context = {}
        # check if form is filled properly and user is authenticated
        if student_form.is_valid() and request.user.is_authenticated:
            # check if user already has an account
            if has_account(request):
                context['failure_message'] = 'Sorry, you cannot create another Student/Instructor account'
            else:
                new_student = student_form.save(commit=False)
                new_student.user = request.user
                new_student.save()
                context['success_message'] = 'Great, you just made a student account, now you can participate in ' \
                                             'classes and submit assignments! '
        else:
            # Send user error messages based on the situation
            if not request.user.is_authenticated:
                context['failure_message'] = 'Sorry, you need a User account to be able to register for a student ' \
                                             'account '
            else:
                context['failure_message'] = 'Sorry, form is not valid, please correct it or refresh it!'
        return render(request, "classmanager/register_student.html", context)
    else:
        student_form = StudentRegisterForm()
        return render(request, "classmanager/register_student.html", {
            'student_form': student_form
        })


def register_instructor(request):
    if request.method == 'POST':
        instructor_form = InstructorRegisterForm(request.POST)
        context = {}
        # check if form is filled properly and user is authenticated
        if instructor_form.is_valid() and request.user.is_authenticated:
            # check if user already has an account
            if has_account(request):
                context['failure_message'] = 'Sorry, you cannot create another Student/Instructor account'
            else:
                new_instructor = instructor_form.save(commit=False)
                new_instructor.user = request.user
                new_instructor.save()
                context['success_message'] = 'Great, you just made an Instructor account, now you can manage ' \
                                             'classes and assignments! '
        else:
            # Send user error messages based on the situation
            if not request.user.is_authenticated:
                context['failure_message'] = 'Sorry, you need a User account to be able to register for an Instructor ' \
                                             'account '
            else:
                context['failure_message'] = 'Sorry, form is not valid, please correct it or refresh it!'
        return render(request, "classmanager/register_instructor.html", context)
    else:
        # Take user back to index if user is a student
        instructor_form = InstructorRegisterForm()
        return render(request, "classmanager/register_instructor.html", {
            'instructor_form': instructor_form
        })


def contact_us(request):
    return render(request, "classmanager/contact_us.html")


# Check if user has created a Student or Instructor account already
def has_account(request):
    x = Student.objects.all().filter(user=request.user).count()
    y = Instructor.objects.all().filter(user=request.user).count()
    if x == 0 and y == 0:
        return False
    else:
        return True
