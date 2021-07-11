from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import StudentRegisterForm, InstructorRegisterForm, CourseCreationForm, AnnouncementCreationForm, \
    AssignmentCreationForm, SubmissionForm
from .models import User, Student, Instructor, Course, Enrollment, Announcement, Assignment, Submission, Attendance


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
                request.user.save()
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


def view_all_courses(request):
    # return all active courses
    courses = Course.objects.filter(is_active=True).order_by("name")
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


@login_required
def view_joined_courses(request):
    if request.user.is_student:
        # if the user is a student, return a template with the joined courses in the context
        student = Student.objects.get(pk=request.user)
        course_keys = Enrollment.objects.filter(student=student)
        courses = []
        for key in course_keys:
            courses.append(Course.objects.get(pk=key.course.id))
        return render(request, "classmanager/joined_courses.html", {
            "courses": courses
        })
    else:
        # If a user that isn't a student accesses this route, they are sent to the index route
        return HttpResponseRedirect(reverse("index"))


@login_required
def view_created_courses(request):
    if request.user.is_instructor:
        instructor = Instructor.objects.get(pk=request.user)
        courses = Course.objects.filter(instructor=instructor).order_by("-date_created")
        return render(request, "classmanager/created_courses.html", {
            "courses": courses
        })
    else:
        # If a user that isn't an instructor accesses this route, they are sent to the index route
        return HttpResponseRedirect(reverse("index"))


@login_required
def view_course(request, course_id):
    # check if course is valid
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return render(request, "classmanager/index.html", {
            "failure_message": "Sorry, the course you wanted does not exist or was deleted"
        })
    # check if user has permissions
    if request.user.is_student:
        # check if student is enrolled in the course
        student = Student.objects.get(pk=request.user)
        if len(Enrollment.objects.filter(course=course_id, student=student)) == 0:
            return render(request, "classmanager/index.html", {
                "failure_message": "Sorry, you need to join a course in order to view it"
            })
    elif request.user.is_instructor:
        # check if instructor is the creator of the course
        instructor = Instructor.objects.get(pk=request.user)
        if course.instructor != instructor:
            return render(request, "classmanager/index.html", {
                "failure_message": "Sorry, you need to create a course in order to view it"
            })
    else:
        return render(request, "classmanager/index.html", {
            "failure_message": "Sorry, you need to join a course as a student or create it as an instructor in order "
                               "to view it "
        })
    # get announcements, assignments, attendance and submissions.
    announcements = Announcement.objects.filter(course=course).order_by("-date_created")
    assignments = Assignment.objects.filter(course=course).order_by("-date_created")
    return render(request, "classmanager/view_course.html", {
        "course": course,
        "announcements": announcements,
        "assignments": assignments
    })


@login_required
def create_announcement(request, course_id):
    # check if user is an instructor
    context = {}
    course = Course.objects.get(pk=course_id)
    if not instructor_check(request, course, "announcement", context):
        return render(request, "classmanager/index.html", context)
    context["course"] = course

    if request.method == "POST":
        announcement_form = AnnouncementCreationForm(request.POST)
        if announcement_form.is_valid():
            new_announcement = announcement_form.save(commit=False)
            new_announcement.course = course
            new_announcement.save()
            context["success_message"] = "Announcement Created Successfully"
        else:
            context["failure_message"] = "Sorry, your announcement cannot be blank, please refresh, " \
                                         "write something and submit again"
        return render(request, "classmanager/create_announcement.html", context)
    else:
        announcement_form = AnnouncementCreationForm()
        context["announcement_form"] = announcement_form
        return render(request, "classmanager/create_announcement.html", context)


@login_required
def create_assignment(request, course_id):
    # check if user is an instructor
    context = {}
    course = Course.objects.get(pk=course_id)
    if not instructor_check(request, course, "assignment", context):
        return render(request, "classmanager/index.html", context)
    context["course"] = course
    if request.method == "POST":
        assignment_form = AssignmentCreationForm(request.POST)
        if assignment_form.is_valid():
            new_assignment = assignment_form.save(commit=False)
            new_assignment.course = course
            new_assignment.save()
            context["success_message"] = "Assignment Created Successfully"
        else:
            context["failure_message"] = "Sorry, your form is not valid, please reload the page and resubmit"
        return render(request, "classmanager/create_assignment.html", context)
    else:
        assignment_form = AssignmentCreationForm()
        context["assignment_form"] = assignment_form
        return render(request, "classmanager/create_assignment.html", context)


@login_required
def create_submission(request, course_id, assignment_id):
    context = {}
    # check if user is a student
    if not request.user.is_student:
        context["failure_message"] = "Sorry, you don't have the permission to create a submission for this assignment."
        return render(request, "classmanager/index.html", context)
    else:
        # check if student is enrolled in this class
        course = Course.objects.get(pk=course_id)
        student = Student.objects.get(pk=request.user)
        try:
            enrollment = Enrollment.objects.get(course=course, student=student)
        except Enrollment.DoesNotExist:
            # case where student is not enrolled in the class but tried to access page
            context["failure_message"] = "Sorry, you don't have the permission to create a submission for this " \
                                         "assignment. "
            return render(request, "classmanager/index.html", context)

    context["course"] = course
    assignment = Assignment.objects.get(pk=assignment_id)
    context["assignment"] = assignment

    if request.method == "POST":
        submission_form = SubmissionForm(request.POST)
        if submission_form.is_valid():
            new_submission = submission_form.save(commit=False)
            new_submission.student = student
            new_submission.assignment = assignment
            new_submission.save()
            context["success_message"] = "Assignment submitted successfully!"
            return render(request, "classmanager/create_submission.html", context)
    else:
        submission_form = SubmissionForm()
        context["submission_form"] = submission_form
        return render(request, "classmanager/create_submission.html", context)


@login_required
def create_attendance(request, course_id):
    # check if user is an instructor
    context = {}
    if not instructor_check(request, course_id, "assignment", context):
        return render(request, "classmanager/index.html", context)
    course = Course.objects.get(pk=course_id)
    context["course"] = course
    if request.method == "POST":
        attendance_form = request.POST
        week = int(attendance_form["week"])
        student_ids = []
        # iterate over attendance form and check for students that were ticked ('on'). then put those in a list
        for k, v in attendance_form.items():
            if v == "on":
                student_ids.append(k)
        # create and save new attendance for each student in selected week
        for student_id in student_ids:
            new_attendance = Attendance(student=Student.objects.get(pk=student_id), course=course, week=week)
            new_attendance.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        # get all students enrolled in class and put in a list
        student_keys = Enrollment.objects.filter(course=course)
        student_list = []
        for key in student_keys:
            student_list.append(Student.objects.get(pk=key.student))
        if len(student_list) < 1:
            context["failure_message"] = "Sorry you cannot take an attendance for an empty class"
            return render(request, "classmanager/index.html", context)
        else:
            context["weeks"] = range(1, course.length)
            context["students"] = student_list
            return render(request, "classmanager/create_attendance.html", context)


@login_required
def view_all(request, activity, course_id):
    # check if course is valid
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return render(request, "classmanager/index.html", {
            "failure_message": "Sorry, the course you wanted does not exist or was deleted"
        })
    context = {"course": course}
    if activity == "announcements":
        announcements = Announcement.objects.filter(course=course).order_by("-date_created")
        context["announcements"] = announcements
        return render(request, "classmanager/view_announcements.html", context)
    elif activity == "assignments":
        assignments = Assignment.objects.filter(course=course).order_by("-date_created")
        context["assignments"] = assignments
        return render(request, "classmanager/view_assignments.html", context)
    else:
        return render(request, "classmanager/index.html", {
            "failure_message": "Sorry, the activity you tried to access does not exist"
        })


@login_required
def view_submissions(request, course_id, assignment_id):
    # *instructor only route* (to view all submissions of a specific assignment)
    # check if user is an instructor
    context = {}
    if not instructor_check(request, course_id, "assignment", context):
        return render(request, "classmanager/index.html", context)
    course = Course.objects.get(pk=course_id)
    context["course"] = course
    # get assignment record
    try:
        assignment = Assignment.objects.get(pk=assignment_id)
    except Assignment.DoesNotExist:
        context["failure_message"] = "The Assignment you are searching for does not exist"
        return render(request, "classmanager/index.html", context)
    else:
        context["assignment"] = assignment
        # get submissions for assignment
        submissions = Submission.objects.filter(assignment=assignment)
        context["submissions"] = submissions
        return render(request, "classmanager/view_submissions.html", context)


@login_required
def view_all_submissions(request, course_id):
    # *student only route* (to view all their submissions in a course)
    context = {}
    if not request.user.is_student:
        context["failure_message"] = "Sorry you cannot access this page"
        return render(request, "classmanager/index.html", context)
    try:
        # search for all submissions made by student in that course
        course = Course.objects.get(pk=course_id)
        student = Student.objects.get(pk=request.user)
        submissions = Submission.objects.filter(assignment__course=course, student=student).order_by("-date_submitted")
    except Course.DoesNotExist or Student.DoesNotExist:
        context["failure_message"] = "Sorry but records do not exist for this student/course"
        return render(request, "classmanager/index.html", context)
    else:
        context["course"] = course
        context["student"] = student
        context["submissions"] = submissions
        return render(request, "classmanager/view_all_submissions.html", context)


@login_required
def grade_submission(request, submission_id):
    context = {}
    # check if submission is valid
    try:
        submission = Submission.objects.get(pk=submission_id)
        course = Course.objects.get(pk=submission.assignment.course.id)
    except Submission.DoesNotExist:
        context["failure_message"] = "The Submission you are trying to grade for does not exist"
        return render(request, "classmanager/index.html", context)
    # check if user is an instructor
    if not instructor_check(request, course.id, "assignment", context):
        return render(request, "classmanager/index.html", context)

    context["submission"] = submission
    context["course"] = course
    if request.method == "POST":
        score = request.POST["score"]
        submission.score = score
        submission.save()
        context["success_message"] = "Score updated successfully!"
    return render(request, "classmanager/grade_submission.html", context)



@login_required
def view_my_profile(request):
    pass


def contact_us(request):
    # TODO
    return render(request, "classmanager/contact_us.html")


# Check if user has created a Student or Instructor account already
def has_account(request):
    return request.user.is_student or request.user.is_instructor


# check if user is permitted to perform an instructor action in a specific course
def instructor_check(request, course_id, action, context):
    # check if course is valid
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        context["failure_message"] = "The course you are searching for does not exist"
        return False
    else:
        # check if user is an instructor
        if not request.user.is_instructor:
            context["failure_message"] = f"Sorry, you don't have the permission to create an {action} in this course."
            return False
        else:
            # check if instructor is the instructor of the course
            course_instructor = course.instructor
            instructor = Instructor.objects.get(pk=request.user)
            # return failure message if not course instructor
            if course_instructor != instructor:
                context["failure_message"] = f"Sorry, you don't have the permission to create an {action} in this " \
                                             "course. "
                return False
        return True
