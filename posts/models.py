from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.get_short_body()

    def get_short_body(self):
        return (self.body[:20] + '...') if len(self.body) > 20 else self.body
    get_short_body.short_description = 'Short Body'
    
    def get_comments_count(self):
        return self.comments.count()
    get_comments_count.short_description = 'Comments Count'

    def get_comments(self):
        return self.comments.all()
    get_comments.short_description = 'Comments'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.get_short_body()

    def get_short_body(self):
        return (self.body[:20] + '...') if len(self.body) > 20 else self.body