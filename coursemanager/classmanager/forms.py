from django import forms
from django.forms import ModelForm, Textarea
from django.utils import timezone
from .models import Student, Instructor, Course, Announcement, Assignment, Submission, Attendance
from datetime import datetime

# date picker for dates between today and january 1 1920
date_picker = forms.DateField(
    widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
        years=range(datetime.today().year, 1920, -1)
    ),
    initial=timezone.now()
)


class StudentRegisterForm(ModelForm):
    date_of_birth = date_picker

    class Meta:
        model = Student
        fields = ["date_of_birth", "major", "standing", "credits"]


class InstructorRegisterForm(ModelForm):
    date_of_birth = date_picker

    class Meta:
        model = Instructor
        fields = ["date_of_birth", "department"]


class CourseCreationForm(ModelForm):
    class Meta:
        model = Course
        fields = ["name", "department", "description", "length"]


class AnnouncementCreationForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ["text"]


class AssignmentCreationForm(ModelForm):
    title = forms.CharField()
    due_date = date_picker

    class Meta:
        model = Assignment
        fields = ["title", "file_url", "points", "due_date", "description"]


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ["text"]
