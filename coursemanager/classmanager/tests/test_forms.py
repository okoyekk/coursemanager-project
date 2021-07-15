from django.test import TestCase
from ..models import Course
from ..forms import StudentRegisterForm, InstructorRegisterForm, CourseCreationForm, \
    AnnouncementCreationForm, AssignmentCreationForm, SubmissionForm
from .test_models import create_users, get_users, create_students, create_courses
from datetime import date, timedelta


class RegisterFormTests(TestCase):
    # tests student and instructor registration forms
    @classmethod
    def setUpTestData(cls):
        create_users()

    def test_valid_student_form(self):
        for student in create_students():
            data = {"date_of_birth": student.date_of_birth, "major": student.major,
                    "standing": student.standing, "credits": student.credits}
            form = StudentRegisterForm(data=data)
            self.assertTrue(form.is_valid())

    def test_invalid_student_form(self):
        data = {"date_of_birth": (date.today() + timedelta(3)), "major": "English",
                "standing": "Grad", "credits": -3}
        form = StudentRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_instructor_form(self):
        data = {"date_of_birth": date.today(), "department": "Math"}
        form = InstructorRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_instructor_form(self):
        data = {"date_of_birth": "today", "department": "MATH"}
        form = InstructorRegisterForm(data=data)
        self.assertFalse(form.is_valid())


class CreationFormTests(TestCase):
    # tests all creation forms, and submission form
    @classmethod
    def setUpTestData(cls):
        create_courses()

    def test_valid_course_form(self):
        for course in Course.objects.all():
            data = {"name": course.name, "department": course.department, "length": course.length}
            form = CourseCreationForm(data=data)
            self.assertTrue(form.is_valid())

    def test_invalid_course_form(self):
        data = {"name": 5, "department": "English", "length": -6}
        form = CourseCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_announcement_form(self):
        data = {"text": "Hello class"}
        form = AnnouncementCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_announcement_form(self):
        data = {"extra_tag": 99}
        form = AnnouncementCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_assignment_form(self):
        data = {"title": "Introduce Yourselves", "due_date": (date.today() + timedelta(7)),
                "points": 5, "description": ""}
        form = AssignmentCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_assignment_form(self):
        data = {}
        form = AssignmentCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_submission_form(self):
        data = {"text": "Hello"}
        form = SubmissionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_submission_form(self):
        data = {}
        form = AssignmentCreationForm(data=data)
        self.assertFalse(form.is_valid())
