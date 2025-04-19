from django.urls import path, include
from .views import *

urlpatterns = [
    #Main/Public Page
    path('', home, name="home"),

    #Profile URLs
    path('profile/register/', RegisterView.as_view(), name='register'),
    path('profile/login/', LoginView.as_view(), name='login'),
    path('profile/logout/', LogoutView.as_view(), name='logout'),
    path('profile/details/', ProfileView.as_view(), name="profile details"),
    path('profile/edit/', EditProfileView.as_view(), name="profile edit"),
    path('profile/delete/', DeleteProfileView.as_view(), name="profile delete"),



    # PK songs
    path('music/', user_songs, name="user songs"),
    path('music/upload/', song_create, name="song create"),
    path('music/<int:pk>/details/', song_details, name="song details"),
    path('music/<int:pk>/edit/', song_edit, name="song edit"),
    path('music/<int:pk>/delete/', song_delete, name="song delete"),
]