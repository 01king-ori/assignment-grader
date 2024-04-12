from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'polls'  # Define app namespace

urlpatterns = [
    # User authentication URLs (handled first):
    path('register/', views.register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

   
 # Adjust template name
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password reset URLs (optional):
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    # App-specific URLs (assume authentication required):
    path('student/', views.student_view, name='student_view'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('lecturer/', views.lecturer_view, name='lecturer_view'),
    path('course/<int:course_id>/create-assignment/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/submissions/', views.view_submissions, name='view_submissions'),
]

