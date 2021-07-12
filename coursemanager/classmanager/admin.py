from django.contrib import admin
from .models import User, Student, Instructor, Course, Enrollment,\
    Announcement, Assignment, Submission, Attendance, Grade

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Announcement)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Attendance)
admin.site.register(Grade)