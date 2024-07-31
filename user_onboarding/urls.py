from django.urls import path
from user_onboarding.views import UserRegistrationView,UserLoginView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name ='registration'),
    path('login/', UserLoginView.as_view(),name='login'),
]