from django.urls import path
from .views import update_password, ProfileView,SignupView, CustomTokenObtainPairView,UserListView

urlpatterns = [
    path('update-password/', update_password),
    path('profile/',  ProfileView.as_view()),
    path('api-token-auth/', CustomTokenObtainPairView.as_view(), name='api_token_auth'),
    path('signup/', SignupView.as_view()),
    path('users/', UserListView.as_view(), name='user-list'),
]
