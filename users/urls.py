from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('user_profile/', views.update_user_view, name='update_user'),
    path('change_password/', views.change_password_view, name='change_password'),
]