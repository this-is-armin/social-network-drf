from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='posts'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    path('<int:pk>/comments/', views.CommentListCreateView.as_view(), name='comments'),
    path('<int:post_pk>/comments/<int:comment_pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
]