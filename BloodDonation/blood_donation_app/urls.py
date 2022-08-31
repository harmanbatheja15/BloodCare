from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blood_donation_app import views
from account.views import ( registration_view, login_view, logout_view, dashboard_view, DeleteView )
from .views import *

urlpatterns = [
    path('', views.index, name="index"),
    path('register', registration_view, name="register"),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('find_donor', views.find_donor, name="find_donor"),
    path('find_blood_banks', views.find_blood_banks, name="find_blood_banks"),
    path('can_donate', views.can_donate, name="can_donate"),
    path('feedback', views.feedback, name="feedback"),
    path('volunteers&technicalTeam', views.volunteers_technicalTeam, name="volunteers&technicalTeam"),
    path('dashboard', dashboard_view, name="dashboard"),
    path('<int:pk>/delete', DeleteView.as_view(template_name='account/delete.html'), name="delete"),
    path('load-cities/', load_cities, name="load_cities"),

    # Password reset urls

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]