from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'body', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at', 'author']
    search_fields = ['body', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'