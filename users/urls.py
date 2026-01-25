from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (SignUpView, ActivateAccountView, ProfileSetupView, profile_view)
from . import views


urlpatterns = [
    # Built-in Login/Logout
    path('login/',
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Custom views
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(),
         name='activate'),
    path('profile-setup/', ProfileSetupView.as_view(), name='profile_setup'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('toggle-follow/<int:user_id>/', views.toggle_follow,
         name='toggle_follow'),
]