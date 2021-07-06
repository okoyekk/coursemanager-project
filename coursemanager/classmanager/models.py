from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


# Create your models here.
class User(AbstractUser):
    pass


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
        return f"Name: {self.user.first_name} {self.user.last_name}, DoB: {self.date_of_birth}," \
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
        return f"Name: {self.user.first_name} {self.user.last_name}, DoB: {self.date_of_birth}," \
               f" Department: {self.department}, Email: {self.user.email}"
