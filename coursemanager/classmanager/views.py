from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .forms import StudentRegisterForm, InstructorRegisterForm, CourseCreationForm
from .models import User, Student, Instructor, Course, Enrollment


def index(request):
    return render(request, "classmanager/index.html")


def login_view(request):
    login_form = AuthenticationForm()
    if request.method == "POST":
        # Attempt to sign user in
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "classmanager/login.html", {
                "login_form": login_form,
                "failure_message": "Invalid username and/or password."
            })
    else:
        return render(request, "classmanager/login.html", {
            "login_form": login_form
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
    if request.method == "POST":
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
                    context["failure_message"] = "Passwords do not match, please correct it."
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
                context["failure_message"] = "Sorry, this username is already taken, please try another one!"
            except KeyError or ValueError:
                context["failure_message"] = "Form is not valid, please correct it!"
            else:
                context["success_message"] = "User created, now fill out either a Student or Instructor form"
            return render(request, "classmanager/register_user.html", context)
    else:
        return render(request, "classmanager/register_user.html")


def register_role(request, role):
    role = role.lower()
    if request.method == "POST":
        # make form based on role (Student or Instructor)
        if role == "student":
            form = StudentRegisterForm(request.POST)
        else:
            form = InstructorRegisterForm(request.POST)
        context = {}

        # check if form is filled properly and user is authenticated
        if form.is_valid() and request.user.is_authenticated:
            # check if user already has an account
            if has_account(request):
                context["failure_message"] = "Sorry, you cannot create another Student/Instructor account"
            else:
                new_role = form.save(commit=False)
                new_role.user = request.user
                new_role.save()
                context["success_message"] = f"Great, you just made your {role} account, now you can participate in " \
                                             "classes and submit assignments! "
                # update user role
                if role == "student":
                    request.user.is_student = True
                else:
                    request.user.is_instructor = True
        else:
            # Send user error messages based on the situation
            if not request.user.is_authenticated:
                context["failure_message"] = f"Sorry, you need a User account to be able to register for your {role} " \
                                             "account "
            else:
                context["failure_message"] = "Sorry, form is not valid, please correct it or refresh it!"
        # render form success or failure page based on role
        return render(request, f"classmanager/register_{role}.html", context)
    else:
        if role == "student":
            form = StudentRegisterForm()
        else:
            form = InstructorRegisterForm()
        # render form based on role
        return render(request, f"classmanager/register_{role}.html", {
            f"{role}_form": form
        })


@login_required
def create_course(request):
    if request.method == "POST":
        context = {}
        course_form = CourseCreationForm(request.POST)
        if course_form.is_valid() and request.user.is_instructor:
            new_course = course_form.save(commit=False)
            new_course.instructor = Instructor.objects.get(pk=request.user)
            new_course.save()
            context["success_message"] = "Course Created Successfully"
        else:
            context["failure_message"] = "Your form is either not valid or you do not have permission " \
                                         "to create a new course!"
        return render(request, "classmanager/index.html", context)
    else:
        course_form = CourseCreationForm()
        return render(request, "classmanager/create_course.html", {
            "course_form": course_form
        })


def view_courses(request):
    # return all active courses
    courses = Course.objects.filter(is_active=True).order_by('name')
    return render(request, "classmanager/view_courses.html", {
        "courses": courses,
    })


@login_required
def join_course(request, course_id):
    context = {}
    if request.method == "POST":
        course = Course.objects.get(pk=course_id)
        student = Student.objects.get(pk=request.user)
        context["course"] = course
        # check if user is already enrolled in that specific course
        if len(Enrollment.objects.filter(course=course, student=student)) != 0:
            context["failure_message"] = "Sorry, You cannot join the same course twice"
            return render(request, "classmanager/join_course.html", context)
        new_enrollment = Enrollment(course=course, student=student)
        new_enrollment.save()
        context["success_message"] = "You have successfully joined this course!"
        return render(request, "classmanager/join_course.html", context)
    else:
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            context["failure_message"] = "Sorry, the course you wanted to join does not exist"
            return render(request, "classmanager/join_course.html", context)
        else:
            context["course"] = course
        return render(request, "classmanager/join_course.html", context)


def view_joined_courses(request):
    pass

def view_created_courses(request):
    pass

def contact_us(request):
    return render(request, "classmanager/contact_us.html")


# Check if user has created a Student or Instructor account already
def has_account(request):
    return request.user.is_student or request.user.is_instructor
