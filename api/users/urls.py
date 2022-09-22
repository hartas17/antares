from django.urls import path
from .views import obtain_jwt_token, UserCreate, UserResetPassword, UserChangePassword, Me

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('users/', UserCreate.as_view()),
    path('me/', Me.as_view()),
    path('users/change-password/', UserChangePassword.as_view()),
    path('reset-password/', UserResetPassword.as_view()),
]
