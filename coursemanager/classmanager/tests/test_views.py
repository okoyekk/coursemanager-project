from django.test import TestCase
from .test_models import create_users, get_users, create_students, create_courses
from django.urls import reverse
from ..models import User, Student, Instructor, Course, Enrollment, \
    Announcement, Assignment, Submission, Attendance, Grade


def setup_objects():
    # creates 4 dummy users (1 unassigned user, 2 students and 1 instructor) and 2 courses
    create_courses()
    for user in get_users():
        user.set_password("123")
        user.save()
    # creates a user without a role
    user = User.objects.create(first_name="Bar", last_name="Baz", username="bbaz",
                               email="bar@gmail.com")
    user.set_password("123")
    user.save()


class RegistrationAndLoginTest(TestCase):
    # tests all views related to user management and role assignment
    @classmethod
    def setUpTestData(cls):
        # create 4 dummy users (1 unassigned user, 2 students and 1 instructor) and 2 courses
        setup_objects()

    def setUp(self):
        # get users
        self.u1, self.u2, self.u3 = get_users()
        #  get last user without a role
        self.u4 = User.objects.get(username="bbaz")
        # create students and instructor
        self.s1, self.s2 = create_students()
        self.instructor = Instructor.objects.get(pk=self.u2)
        # create data as sample valid user data
        self.data = {"first-name": "foo", "last-name": "bar", "email": "foo@test.net", "username": "foo",
                     "password": "123", "confirmation": "123"}
        # get both dummy courses
        courses = Course.objects.all()
        self.c1, self.c2 = courses[0], courses[1]

    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "classmanager/index.html")

    def test_login_and_logout(self):
        # check if login gives correct response for get and gives a redirect code for post
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        data = {"username": self.u1.username, "password": "123"}
        response = self.client.post(path=reverse("login"), data=data)
        self.assertEqual(response.status_code, 302)
        # check if login gives a 200 for post (form not valid)
        data = {"username": "abc", "password": "123"}
        response = self.client.post(path=reverse("login"), data=data)
        self.assertEqual(response.status_code, 200)
        # check if logout response template is index (user got logged out)
        response = self.client.get(reverse("logout"))
        self.assertTemplateUsed(response, "classmanager/index.html")

    def test_register(self):
        # register path, returns a template always (200)
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_valid_register_user(self):
        # register-user paths
        # get returns a template always
        response = self.client.get(reverse("register-user"))
        self.assertEqual(response.status_code, 200)
        # post should create new user if valid data is given while unauthenticated
        data = self.data
        response = self.client.post(path=reverse("register-user"), data=data)
        self.assertEqual(response.status_code, 200)
        users = User.objects.filter(username="foo")
        self.assertEqual(len(users), 1)

    def test_invalid_register_user(self):
        # test registering user with passwords that do not match
        data = self.data
        data["confirmation"] = "1234"
        response = self.client.post(path=reverse("register-user"), data=data)
        self.assertIn("failure_message", response.context)
        # test registering user without first name
        data["username"] = "food"
        data["confirmation"] = "123"
        del data["first-name"]
        response = self.client.post(path=reverse("register-user"), data=data)
        self.assertIn("failure_message", response.context)
        # test registering valid user while after getting logged in
        data = {"username": self.u1.username, "password": "123"}
        self.client.post(path=reverse("login"), data=data)
        data = self.data
        response = self.client.post(path=reverse("register-user"), data=data)
        self.assertIn("failure_message", response.context)
        self.assertTemplateUsed(response, "classmanager/register.html")
        # test registering user with a username that is already taken after logging out
        self.client.get(reverse("logout"))
        data["username"] = "jcharles"
        response = self.client.post(path=reverse("register-user"), data=data)
        self.assertIn("failure_message", response.context)

    def test_valid_register_student_role(self):
        user = self.u4
        self.client.login(username=user.username, password="123")
        # register new valid student
        response = self.client.get("/register/student")
        self.assertIn("student_form", response.context)
        data = {"date_of_birth": "07/08/2001", "major": "Science", "standing": "FR", "credits": 2}
        response = self.client.post("/register/student", data=data)
        # check if it produced a success massage
        self.assertIn("success_message", response.context)

    def test_valid_register_instructor_role(self):
        self.client.login(username=self.u4.username, password="123")
        # register new valid instructor
        response = self.client.get("/register/instructor")
        self.assertIn("instructor_form", response.context)
        data = {"date_of_birth": "07/08/2001", "department": "Science"}
        response = self.client.post("/register/instructor", data=data)
        # check if it produced a success massage
        self.assertIn("success_message", response.context)

    def test_invalid_register_role(self):
        # register role with invalid form
        self.client.login(username=self.u4.username, password="123")
        response = self.client.get("/register/instructor")
        self.assertIn("instructor_form", response.context)
        data = {"date_of_birth": "07/08/2001"}
        response = self.client.post("/register/instructor", data=data)
        self.assertIn("failure_message", response.context)
        self.client.logout()
        # register student role while already having a role
        self.client.login(username=self.u2.username, password="123")
        data = {"date_of_birth": "07/08/2001", "major": "Science", "standing": "FR", "credits": 2}
        response = self.client.post("/register/student", data=data)
        self.assertIn("failure_message", response.context)

    def test_forgot_password(self):
        user = self.u4
        response = self.client.get(reverse("forgot-password"))
        self.assertTemplateUsed(response, "classmanager/forgot_password.html")
        # try valid password change
        data = {"email": user.email, "username": user.username, "password": "1299", "confirmation": "1299"}
        response = self.client.post(reverse("forgot-password"), data=data)
        self.assertIn("success_message", response.context)
        # try invalid password changes
        # invalid username
        bad_data_1 = {"email": user.email, "username": "jojo", "password": "1299", "confirmation": "1299"}
        # invalid email
        bad_data_2 = {"email": "jojo@mama.net", "username": user.username, "password": "1299", "confirmation": "1299"}
        # password and confirmation don't match
        bad_data_3 = {"email": user.email, "username": user.username, "password": "1299", "confirmation": "1234"}
        # all combinations should give failure messages
        for data in bad_data_1, bad_data_2, bad_data_3:
            response = self.client.post(reverse("forgot-password"), data=data)
            self.assertIn("failure_message", response.context)

    def test_change_name(self):
        # requesting this view should redirect if not authenticated
        response = self.client.get(reverse("change-name"))
        self.assertEqual(response.status_code, 302)
        # log in as self.u4 and send post request to change name of user (should both return code 200)
        user = self.u4
        self.client.login(username=user.username, password="123")
        response = self.client.get(reverse("change-name"))
        self.assertEqual(response.status_code, 200)
        data = {"first-name": "Timothee", "last-name": "Chalamet"}
        self.client.post(reverse("change-name"), data=data)
        self.assertEqual(response.status_code, 200)


class CourseViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create 4 dummy users (1 unassigned user, 2 students and 1 instructor) and 2 courses
        setup_objects()

    def setUp(self):
        # get users
        self.u1, self.u2, self.u3 = get_users()
        #  get last user without a role
        self.u4 = User.objects.get(username="bbaz")
        # create students and instructor
        self.s1, self.s2 = create_students()
        self.instructor = Instructor.objects.get(pk=self.u2)
        # get both dummy courses
        courses = Course.objects.all()
        self.c1, self.c2 = courses[0], courses[1]

    def test_create_course(self):
        # login with an instructor account and get page, should return course form in template
        self.client.login(username=self.u2.username, password="123")
        response = self.client.get("/create/course")
        self.assertIn("course_form", response.context)
        # make post request for new valid course, should create new course and return success message
        data = {"name": "Biology", "department": "Science", "description": "Entry level biology", "length": 12,
                "credits": 4}
        response = self.client.post("/create/course", data=data)
        self.assertTrue(len(Course.objects.filter(name="Biology", department="Science")) > 0)
        self.assertIn("success_message", response.context)
        # make post request with an invalid form
        data = {"name": "Biology", "department": "Science", "description": "Entry level biology", "length": 12}
        response = self.client.post("/create/course", data=data)
        self.assertIn("failure_message", response.context)
