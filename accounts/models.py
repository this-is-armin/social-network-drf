from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models

from utils.validators import username_validator
from utils.paths import get_user_image_upload_path


User = settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text='Required. 150 characters or fewer. Lowercase letters, numbers and _/. only.',
        error_messages={
            'unique': 'This username already exists.',
        },   
    )
    email = models.EmailField(
        unique=True,
        verbose_name='email address',
        help_text='Required. Must be a valid and unique email address.',
        error_messages={
            'unique': 'This email address already exists.',
        },
    )
    first_name = models.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters only.',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z]+$',
                message='First name must contain only letters.',
            ),
        ],
    )
    last_name = models.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters only.',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z]+$',
                message='Last name must contain only letters.',
            ),
        ],
    )
    bio = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        blank=True, 
        null=True,
        upload_to=get_user_image_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif']),
        ],
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_followers(self):
        return CustomUser.objects.filter(following__to_user=self)
    
    def get_following(self):
        return CustomUser.objects.filter(followers__from_user=self)

    def get_followers_count(self):
        return self.followers.count()
    get_followers_count.short_description = 'Followers Count'
    
    def get_following_count(self):
        return self.following.count()
    get_following_count.short_description = 'Following Count'


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['from_user', 'to_user']
    
    def __str__(self):
        return f"{self.from_user} followed {self.to_user}"
    
    def clean(self):
        super().clean()
        if self.from_user == self.to_user:
            raise ValidationError('Users can not follow themselves.')
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)