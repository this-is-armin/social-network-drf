from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import Relation
from posts.models import Post
from utils.permissions import (
    IsAnonymous,
    IsOwnerOrReadOnly,
    IsNotSelf,
)
from .serializers import (
    UserListSerializer,
    RegisterSerializer,
    ProfileSerializer,
    PostListSerializer,
)


User = get_user_model()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymous]


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'username'


class FollowView(APIView):
    permission_classes = [IsAuthenticated, IsNotSelf]

    def post(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if Relation.objects.filter(from_user=request.user, to_user=user).exists():
            return Response(
                {'detail': 'You are already following this user.'}, 
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        Relation.objects.create(from_user=request.user, to_user=user)
        return Response({
            'detail': 'You are now following this user.'},
            status=status.HTTP_201_CREATED,
        )


class UnfollowView(APIView):
    permission_classes = [IsAuthenticated, IsNotSelf]

    def delete(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if not relation.exists():
            return Response(
                {'detail': 'You are not following this user.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        relation.delete()
        return Response(
            {'detail': 'You have unfollowed this user.'},
            status=status.HTTP_200_OK,
        )


class FollowerListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.get_followers()


class FollowingListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.get_following()


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['body']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(user=user)