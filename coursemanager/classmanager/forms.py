from django.forms import ModelForm
from .models import User, Student, Instructor


# Create form for Student
class StudentRegisterForm(ModelForm):
    class Meta:
        model = Student
        fields = ['date_of_birth', 'major', 'standing', 'credits']


# Create form for Instructor
class InstructorRegisterForm(ModelForm):
    class Meta:
        model = Instructor
        fields = ['date_of_birth', 'department']

