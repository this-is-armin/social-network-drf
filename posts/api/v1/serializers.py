from django.urls import reverse
from rest_framework import serializers

from posts.models import Post, Comment
from accounts.api.v1.serializers import UserInlineSerializer


class CommentDisplaySerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'created_at']


class CommentActionSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)
    post_detail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'created_at', 'post_detail_url']
    
    def get_post_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('posts_v1:post_detail', kwargs={'pk': obj.post.pk})
        )


class PostListSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    detail_page_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
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


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer(read_only=True)
    comments = CommentDisplaySerializer(many=True, read_only=True)
    comments_page_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'body',
            'created_at',
            'updated_at',
            'comments_page_url',
            'comments',
        ]
    
    def get_comments_page_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('posts_v1:comments', kwargs={'pk': obj.pk})
        )