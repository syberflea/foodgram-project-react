from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username')
    list_filter = ('email', 'username')


admin.site.register(User, CustomUserAdmin)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')
    search_fields = ('user', 'following')
    list_filter = ('user', 'following')
