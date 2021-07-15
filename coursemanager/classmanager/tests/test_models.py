from django.test import TestCase
from ..models import User, Student, Instructor, Course, Enrollment, \
    Announcement, Assignment, Submission, Attendance, Grade
from datetime import date, timedelta


def create_users():
    # creates 3 users(2 students and an instructor for testing purposes)
    u1 = User.objects.create(first_name="Joe", last_name="Charles", username="jcharles",
                             email="jcharles@gmail.com", is_student=True)
    u2 = User.objects.create(first_name="Ashley", last_name="Bernat", username="abernat",
                             email="abernat@hotmail.com", is_instructor=True)
    u3 = User.objects.create(first_name="Alex", last_name="Burke", username="aburke",
                             email="aburke@yahoo.com", is_student=True)
    return u1, u2, u3


def create_courses():
    # creates 3 users and 2 courses with u2 as instructor of both
    _, u2, _ = create_users()
    i1 = Instructor.objects.create(user=u2, department="Science")
    c1 = Course.objects.create(instructor=i1, name="Physics 1", department="Science", credits=4, description="")
    c2 = Course.objects.create(instructor=i1, name="Astrophysics", department="Science", credits=4, description="")
    return c1, c2


def get_users():
    # returns all 3 users
    return User.objects.get(id=1), User.objects.get(id=2), User.objects.get(id=3)


def create_students():
    # creates 2 students
    u1, _, u3 = get_users()
    s1 = Student.objects.create(user=u1, major="Math", standing="SM", credits=30)
    s2 = Student.objects.create(user=u3, major="Technology", standing="SR", credits=100)
    return s1, s2


class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_users()

    def setUp(self):
        self.u1, self.u2, self.u3 = get_users()
        self.s1, self.s2 = create_students()

    def test_is_student(self):
        self.assertTrue(self.u1.is_student)
        self.assertFalse(self.u2.is_student)
        self.assertTrue(self.u3.is_student)

    def test_student_name(self):
        s1_expected_name = f"Name: Joe Charles, DoB: {date.today()}, Major: Math, Standing: SM, Credits " \
                           f"completed: 30, Email: jcharles@gmail.com."
        s2_expected_name = f"Name: Alex Burke, DoB: {date.today()}, Major: Technology, Standing: SR, Credits " \
                           f"completed: 100, Email: aburke@yahoo.com."
        self.assertEqual(str(self.s1), s1_expected_name)
        self.assertEqual(str(self.s2), s2_expected_name)


class InstructorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_users()

    def setUp(self):
        self.u1, self.u2, self.u3 = get_users()
        self.instructor = Instructor.objects.create(user=self.u2, department="Science")

    def test_is_instructor(self):
        self.assertFalse(self.u1.is_instructor)
        self.assertTrue(self.u2.is_instructor)
        self.assertFalse(self.u3.is_instructor)

    def test_instructor_name(self):
        self.assertEqual(str(self.instructor), f"Name: Ashley Bernat, DoB: {date.today()}, Department: "
                                               f"Science, Email: abernat@hotmail.com.")


class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_courses()

    def setUp(self):
        self.c1 = Course.objects.get(id=1)
        self.c2 = Course.objects.get(id=2)
        self.instructor = Instructor.objects.get(pk=self.c1.instructor)

    def test_course_name(self):
        c1_expected_name = "Course Name: Physics 1, Instructor: Ashley Bernat, credits: 4, length: 10 weeks."
        c2_expected_name = "Course Name: Astrophysics, Instructor: Ashley Bernat, credits: 4, length: 10 weeks."
        self.assertEqual(str(self.c1), c1_expected_name)
        self.assertEqual(str(self.c2), c2_expected_name)


class EnrollmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_courses()

    def setUp(self):
        self.c1, self.c2 = Course.objects.get(id=1), Course.objects.get(id=2)
        self.u1, _, self.u3 = get_users()
        self.s1, self.s2 = create_students()

    def test_enrollment_name(self):
        e1_expected_name = f"Student: Joe Charles joined Physics 1 on {date.today()}."
        e2_expected_name = f"Student: Alex Burke joined Astrophysics on {date.today()}."
        e1 = Enrollment.objects.create(course=self.c1, student=self.s1)
        e2 = Enrollment.objects.create(course=self.c2, student=self.s2)
        self.assertEqual(str(e1), e1_expected_name)
        self.assertEqual(str(e2), e2_expected_name)


class AnnouncementModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_courses()

    def setUp(self):
        self.c1, self.c2 = Course.objects.get(id=1), Course.objects.get(id=2)
        self.instructor = Instructor.objects.get(user_id=2)

    def test_announcement_name(self):
        ann1 = Announcement.objects.create(course=self.c1, text="Hello class")
        ann2 = Announcement.objects.create(course=self.c2, text="Hi students")
        for ann in ann1, ann2:
            ann_expected_name = f"Announcement for '{ann.course.name}': {ann.text}; " \
                               f"Posted by {ann.course.instructor.get_name()}, on {ann.date_created}."
            self.assertEqual(str(ann), ann_expected_name)


class CourseFeatureModelTest(TestCase):
    # These models related and only have 1 method so breaking them up
    # into separate classes would not be efficient
    @classmethod
    def setUpTestData(cls):
        create_courses()

    def setUp(self):
        self.c1, self.c2 = Course.objects.get(id=1), Course.objects.get(id=2)
        self.instructor = Instructor.objects.get(user_id=2)
        self.s1, self.s2 = create_students()
        Enrollment.objects.create(course=self.c1, student=self.s1)
        Enrollment.objects.create(course=self.c2, student=self.s2)
        self.ass1 = Assignment.objects.create(title="Introduce yourselves!", course=self.c1)
        self.ass2 = Assignment.objects.create(title="What is your zodiac sign?", course=self.c2)

    def test_assignment_name(self):
        for ass in self.ass1, self.ass2:
            ass_expected_name = f"Assignment for '{ass.course.name}': '{ass.title}'; " \
                                f"Due: {ass.due_date}, points: {ass.points}"
            self.assertEqual(str(ass), ass_expected_name)

    def test_submission_name(self):
        sub1 = Submission.objects.create(assignment=self.ass1, student=self.s1, text="Hi, I'm Joe!")
        sub2 = Submission.objects.create(assignment=self.ass2, student=self.s2, text="Cancer")
        for sub in sub1, sub2:
            sub_expected_name = f"Submission for '{sub.assignment.title}' by '{sub.student.get_name()}'" \
                                f" on {sub.date_submitted}"
            self.assertEqual(str(sub), sub_expected_name)

    def test_attendance_name(self):
        att1 = Attendance.objects.create(student=self.s1, course=self.c1, week=1)
        att2 = Attendance.objects.create(student=self.s2, course=self.c2, week=1)
        for att in att1, att2:
            att_expected_name = f"'{att.student.get_name()}' attended {att.course.name} in week {att.week}"
            self.assertEqual(str(att), att_expected_name)

    def test_grade_name(self):
        grade1 = Grade.objects.create(student=self.s1, course=self.c1, score=97)
        grade2 = Grade.objects.create(student=self.s2, course=self.c2, score=89)
        for grade in grade1, grade2:
            grade_expected_name = f"'{grade.student.get_name()}' scored {grade.score}% in '{grade.course.name}'"
            self.assertEqual(str(grade), grade_expected_name)
