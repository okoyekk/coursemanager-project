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
                context['failure_message'] = 'Sorry, this username is already taken, please try another one!'
            except KeyError or ValueError:
                context['failure_message'] = 'Form is not valid, please correct it!'
            else:
                context['success_message'] = 'User created, now fill out either a Student or Instructor form'
            return render(request, "classmanager/register_user.html", context)
    else:
        return render(request, "classmanager/register_user.html")


def register_role(request, role):
    role = role.lower()
    if request.method == 'POST':
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
                context['failure_message'] = 'Sorry, you cannot create another Student/Instructor account'
            else:
                new_role = form.save(commit=False)
                new_role.user = request.user
                new_role.save()
                context['success_message'] = f'Great, you just made your {role} account, now you can participate in ' \
                                             'classes and submit assignments! '
        else:
            # Send user error messages based on the situation
            if not request.user.is_authenticated:
                context['failure_message'] = f'Sorry, you need a User account to be able to register for your {role} ' \
                                             'account '
            else:
                context['failure_message'] = 'Sorry, form is not valid, please correct it or refresh it!'
        # render form success or failure page based on role
        return render(request, f"classmanager/register_{role}.html", context)
    else:
        if role == "student":
            form = StudentRegisterForm()
        else:
            form = InstructorRegisterForm()
        # render form based on role
        return render(request, f"classmanager/register_{role}.html", {
            f'{role}_form': form
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
