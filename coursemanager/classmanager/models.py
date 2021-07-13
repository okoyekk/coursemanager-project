from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, timedelta


# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()


# Student model that is also a user
class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=date.today)
    MAJORS = [
        ("Math", "Math"), ("English", "English"),
        ("Science", "Science"), ("Technology", "Technology"),
        ("Law", "Law"), ("Art", "Art"),
        ("Business", "Business"), ("Health", "Health")
    ]
    STANDINGS = [
        ("FR", "Freshman"),
        ("SM", "Sophomore"),
        ("JR", "Junior"),
        ("SR", "Senior"),
        ("GR", "Graduate")
    ]
    major = models.CharField(max_length=20, choices=MAJORS, default="Undecided")
    standing = models.CharField(max_length=20, choices=STANDINGS, default="FR")
    credits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Name: {self.get_name()}, DoB: {self.date_of_birth}," \
               f" Major: {self.major}, Standing: {self.standing}, Credits completed: {self.credits}, " \
               f"Email: {self.user.email}."

    def get_name(self):
        return str(self.user)


# Instructor model that is also a user
class Instructor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=date.today)
    DEPARTMENTS = [
        ("Math", "Math"), ("English", "English"),
        ("Science", "Science"), ("Technology", "Technology"),
        ("Law", "Law"), ("Art", "Art"),
        ("Business", "Business"), ("Health", "Health")
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENTS, default="Other")

    def __str__(self):
        return f"Name: {self.get_name()}, DoB: {self.date_of_birth}," \
               f" Department: {self.department}, Email: {self.user.email}."

    def get_name(self):
        return str(self.user)


class Course(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, default=None)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    DEPARTMENTS = [
        ("Math", "Math"), ("English", "English"),
        ("Science", "Science"), ("Technology", "Technology"),
        ("Law", "Law"), ("Art", "Art"),
        ("Business", "Business"), ("Health", "Health")
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENTS, default="Other")
    description = models.TextField(max_length=1000, default=None, blank=True)
    credits = models.PositiveIntegerField(default=2)
    # course length in weeks, default = 10 weeks
    length = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"Course Name: {self.name}, Instructor: {self.instructor.get_name()}, credits: {self.credits}," \
               f" length: {self.length} weeks."


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Student: {self.student.get_name()} joined {self.course.name} on {self.date_joined}."


class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, default=None)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Announcement for '{self.course.name}': {self.text}; Posted by {self.course.instructor.get_name()}," \
               f" on {self.date_created}."


class Assignment(models.Model):
    title = models.TextField(max_length=255, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file_url = models.URLField(blank=True, max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    date_created = models.DateField(auto_now_add=True)
    # default due date would be 3 days away from today
    due_date = models.DateField(blank=False, default=date.today() + timedelta(days=3))
    points = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Assignment for '{self.course.name}': '{self.title}'; Due: {self.due_date}, points: {self.points}"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    text = models.TextField(max_length=1000)
    date_submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Submission for '{self.assignment.title}' by '{self.student.get_name()}' on {self.date_submitted}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"'{self.student.get_name()}' attended {self.course.name} in week {self.week}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"'{self.student.get_name()}' scored {self.score}% in '{self.course.name}'"
