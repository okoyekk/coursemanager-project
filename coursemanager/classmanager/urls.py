from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("forgot_password", views.forgot_password, name="forgot-password"),
    path("register", views.register, name="register"),
    path("register/user", views.register_user, name="register-user"),
    path("register/<str:role>", views.register_role, name="register-role"),
    path("create/course", views.create_course, name="create-course"),
    path("view_all_courses", views.view_all_courses, name="view-all-courses"),
    path("view_course/<int:course_id>", views.view_course, name="view-course"),
    path("join_course/<int:course_id>", views.join_course, name="join-course"),
    path("leave_course/<int:course_id>", views.leave_course, name="leave-course"),
    path("view_joined_courses", views.view_joined_courses, name="view-joined-courses"),
    path("view_created_courses", views.view_created_courses, name="view-created-courses"),
    path("create/announcement/<int:course_id>", views.create_announcement, name="create-announcement"),
    path("create/assignment/<int:course_id>", views.create_assignment, name="create-assignment"),
    path("create/submission/<int:course_id>/<int:assignment_id>", views.create_submission, name="create-submission"),
    path("create/attendance/<int:course_id>", views.create_attendance, name="create-attendance"),
    path("view/attendance/<int:course_id>", views.view_attendance, name="view-attendance"),
    path("view/all/<str:activity>/<int:course_id>", views.view_all, name="view-all"),
    path("view/submissions/<int:course_id>/<int:assignment_id>", views.view_submissions, name="view-submissions"),
    path("view/submissions/<int:course_id>", views.view_all_submissions, name="view-all-submissions"),
    path("grade/submission/<int:submission_id>", views.grade_submission, name="grade-submission"),
    path("deactivate/course/<int:course_id>", views.deactivate_course, name="deactivate-course"),
    path("grade/final/<int:course_id>", views.grade_finals, name="grade-finals"),
    path("grade/final/<int:course_id>/<int:user_id>", views.grade_final, name="grade-final"),
    path("view/final/<int:course_id>", views.view_finals, name="view-finals"),
    path("view/my_profile", views.view_my_profile, name="view-my-profile"),
    path("change/name", views.change_name, name="change-name"),
    path("contact_us", views.contact_us, name="contact_us")
]
