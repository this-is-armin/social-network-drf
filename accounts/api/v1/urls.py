from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),

    path('register/', views.RegisterView.as_view(), name='register'),

    path('<str:username>/', views.ProfileView.as_view(), name='profile'),

    path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    path('<str:username>/unfollow/', views.UnfollowView.as_view(), name='unfollow'),

    path('<str:username>/followers/', views.FollowerListView.as_view(), name='followers'),
    path('<str:username>/following/', views.FollowingListView.as_view(), name='following'),
    path('<str:username>/posts/', views.PostListView.as_view(), name='posts'),
]