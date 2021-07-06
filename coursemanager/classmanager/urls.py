from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register/user", views.register_user, name="register-user"),
    path("register/student", views.register_student, name="register-student"),
    path("register/instructor", views.register_instructor, name="register-instructor"),
    path("contact_us", views.contact_us, name="contact_us")
]
