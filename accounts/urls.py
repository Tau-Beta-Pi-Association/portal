from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('register/', register_user, name='register'),
    path('verify/', verify_user, name='verify'),
    path('validate/', validate, name='validate'),
    path('login/', auth_view, name='login-view'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
]
