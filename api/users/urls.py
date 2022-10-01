from django.urls import path
from .views import UserCreate, UserResetPassword, UserChangePassword, Me

urlpatterns = [
    path('users/', UserCreate.as_view()),
    path('me/', Me.as_view()),
    path('users/change-password/', UserChangePassword.as_view()),
    path('reset-password/', UserResetPassword.as_view()),
]
