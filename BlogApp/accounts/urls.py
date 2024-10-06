from django.urls import path
from .views import ListAllUsers, UserRegistrationView, Userlogin

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name= 'userregister'),
    path('allusers/', ListAllUsers.as_view(), name= 'all-users'),
    path('login/', Userlogin.as_view(), name= 'userlogin'),
]