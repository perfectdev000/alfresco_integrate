from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pasword-reset/', auth_views.PasswordResetView.as_view(template_name='sensai/password_reset.html'), name='reset_password'),
    path('password-reset/done/', views.ResetPasswordDone.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='sensai/password_reset_confirm.html'),
    name='password_reset_confirm'),
    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='sensai/password_reset_complete.html'),
    name='password_reset_complete'),

    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='sensai/change_password.html'),
    name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='sensai/change_password_done.html'),
    name='password_change_done'),
]