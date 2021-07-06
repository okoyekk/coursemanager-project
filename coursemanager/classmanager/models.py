from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)

    def get_name(self):
        return f"{self.first_name} {self.last_name}"


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
        return f"Name: {self.user.get_name()}, DoB: {self.date_of_birth}," \
               f" Major: {self.major}, Standing: {self.standing}, Credits completed: {self.credits}, " \
               f"Email: {self.user.email}"


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
        return f"Name: {self.user.get_name()}, DoB: {self.date_of_birth}," \
               f" Department: {self.department}, Email: {self.user.email}"


class Course(models.Model):
    instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE)
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

    def __str__(self):
        return f"Course Name: {self.name}, Instructor: {self.instructor.user.get_name()}"


class Enrollment(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Student: {self.student.user.get_name()} joined {self.course.name} on {self.date_joined}"
