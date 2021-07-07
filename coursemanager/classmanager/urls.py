from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register/user", views.register_user, name="register-user"),
    path("register/<str:role>", views.register_role, name="register-role"),
    path("create/course", views.create_course, name="create-course"),
    path("view_courses", views.view_courses, name="view-courses"),
    path("join_course/<int:course_id>", views.join_course, name="join-course"),
    path("contact_us", views.contact_us, name="contact_us")
]
