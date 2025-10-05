from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.models import Relation
from posts.models import Post


User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'image',
            'profile_url',
        ]
    
    def get_profile_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('accounts_v1:profile', kwargs={'username': obj.username})
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, write_only=True)
    confirm_password = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError('Passwords do not match.')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    followers_page_url = serializers.SerializerMethodField()
    following_page_url = serializers.SerializerMethodField()

    follow_url = serializers.SerializerMethodField()
    unfollow_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'image',
            'followers_count',
            'following_count',
            'followers_page_url',
            'following_page_url',
            'follow_url',
            'unfollow_url',
        ]

    def get_followers_count(self, obj):
        return obj.get_followers_count()
    
    def get_following_count(self, obj):
        return obj.get_following_count()
    
    def get_followers_page_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('accounts_v1:followers', kwargs={'username': obj.username})
        )
    
    def get_following_page_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('accounts_v1:following', kwargs={'username': obj.username})
        )
    
    def get_follow_url(self, obj):
        request = self.context.get('request')
        if not request or request.user == obj:
            return None

        is_followed = Relation.objects.filter(from_user=request.user, to_user=obj).exists()
        if not is_followed:
            return request.build_absolute_uri(
                reverse('accounts_v1:follow', kwargs={'username': obj.username})
            )
        return None
    
    def get_unfollow_url(self, obj):
        request = self.context.get('request')
        if not request or request.user == obj:
            return None

        is_followed = Relation.objects.filter(from_user=request.user, to_user=obj).exists()
        if is_followed:
            return request.build_absolute_uri(
                reverse('accounts_v1:unfollow', kwargs={'username': obj.username})
            )
        return None


class UserInlineSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_url']
    
    def get_profile_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('accounts_v1:profile', kwargs={'username': obj.username})
        )


class PostListSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField(read_only=True)
    detail_page_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'body',
            'created_at',
            'updated_at',
            'comments_count',
            'detail_page_url',
        ]
    
    def get_comments_count(self, obj):
        return obj.get_comments_count()
    
    def get_detail_page_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('posts_v1:post_detail', kwargs={'pk': obj.pk})
        )