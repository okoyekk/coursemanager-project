from django.forms import ModelForm, Textarea
from .models import Student, Instructor, Course, Announcement, Assignment, Submission, Attendance


class StudentRegisterForm(ModelForm):
    class Meta:
        model = Student
        fields = ["date_of_birth", "major", "standing", "credits"]


class InstructorRegisterForm(ModelForm):
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
    class Meta:
        model = Assignment
        fields = ["title", "description", "file_url", "points", "due_date"]


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ["text"]
