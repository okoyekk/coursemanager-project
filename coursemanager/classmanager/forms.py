from django.forms import ModelForm, Textarea
from .models import Student, Instructor, Course


# Create form for Student
class StudentRegisterForm(ModelForm):
    class Meta:
        model = Student
        fields = ["date_of_birth", "major", "standing", "credits"]


# Create form for Instructor
class InstructorRegisterForm(ModelForm):
    class Meta:
        model = Instructor
        fields = ["date_of_birth", "department"]


# Create form for Course
class CourseCreationForm(ModelForm):
    class Meta:
        model = Course
        fields = ["name", "department", "description"]
