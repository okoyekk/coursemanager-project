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
    path("view_all_courses", views.view_all_courses, name="view-all-courses"),
    path("view_course/<int:course_id>", views.view_course, name="view-course"),
    path("join_course/<int:course_id>", views.join_course, name="join-course"),
    path("view_joined_courses", views.view_joined_courses, name="view-joined-courses"),
    path("view_created_courses", views.view_created_courses, name="view-created-courses"),
    path("create/announcement/<int:course_id>", views.create_announcement, name="create-announcement"),
    path("create/assignment/<int:course_id>", views.create_assignment, name="create-assignment"),
    path("create/submission/<int:course_id>/<int:assignment_id>", views.create_submission, name="create-submission"),
    path("create/attendance/<int:course_id>", views.create_attendance, name="create-attendance"),
    path("view/my_profile", views.view_my_profile, name="view-my-profile"),
    path("contact_us", views.contact_us, name="contact_us")
]
