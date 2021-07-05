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
    if request.method == 'POST':
        # check which form was submitted and save if valid
        user_form = request.POST
        student_form = StudentRegisterForm(request.POST)
        instructor_form = InstructorRegisterForm(request.POST)
        context = {
            'student_form': student_form,
            'instructor_form': instructor_form,
        }
        # if user is not authenticated, try registering them (New user)
        if not request.user.is_authenticated:
            try:
                first_name = user_form["first-name"]
                last_name = user_form["last-name"]
                email = user_form["email"]
                username = user_form["username"]
                password = user_form["password"]
                confirmation = user_form["confirmation"]
                # Return a new register form if passwords don't match
                # TODO add javascript validation to avoid this
                if password != confirmation:
                    context['failure_message'] = 'Passwords do not match, please correct it.'
                    return render(request, "classmanager/register.html", context)
                # Attempt creating a new user
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                user.save()
                # log in user if it was created without any exception
                user = authenticate(username=username, password=password)
                login(request, user)
            except IntegrityError:
                context['failure_message'] = 'Sorry, this username is already taken'
            except KeyError:
                context['failure_message'] = 'Sorry, you must create a User account and be logged in before you can ' \
                                             'create a Student or Instructor account '
            except ValueError:
                context['failure_message'] = 'Form is not valid, please correct it!'
            else:
                context['success_message'] = 'User created, now fill out either a Student or Instructor form'
        # only save new student if user is authenticated
        elif student_form.is_valid() and request.user.is_authenticated:
            try:
                new_student = student_form.save(commit=False)
                new_student.user = request.user
                new_student.save()
            except IntegrityError:
                context['failure_message'] = 'Sorry, you cannot create another Student account'
            else:
                context['success_message'] = 'Great, you just made a student account, now you can participate in ' \
                                             'classes and submit assignments! '
        # only save new student if user is authenticated
        elif instructor_form.is_valid() and request.user.is_authenticated:
            try:
                new_instructor = student_form.save(commit=False)
                new_instructor.user = request.user
                new_instructor.save()
            except IntegrityError:
                context['failure_message'] = 'Sorry you cannot create another Instructor account'
            else:
                context['success_message'] = 'Great, you just made an instructor account, now you can create classes ' \
                                             'and manage them!'
        else:
            context['failure_message'] = 'Form is not valid, please correct it!'
        return render(request, "classmanager/register.html", context)
    else:
        # Generate forms and return to user
        student_form = StudentRegisterForm()
        instructor_form = InstructorRegisterForm()
        return render(request, "classmanager/register.html", {
            'student_form': student_form,
            'instructor_form': instructor_form
        })


def contact_us(request):
    return render(request, "classmanager/contact_us.html")
