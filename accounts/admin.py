from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Relation


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal Info', {'fields': ('bio', 'image',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Info', {'fields': ('bio', 'image',)}),
    )


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user', 'created_at']
    list_filter = ['from_user', 'to_user', 'created_at']
    search_fields = ['from_user__username', 'to_user__username']